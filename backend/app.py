import os
import pathlib
import re
import csv
import time
import io
from collections import defaultdict
from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient, TEXT
from bson import ObjectId

# === Chargement du .env ===
BASE_DIR = pathlib.Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# === Connexion MongoDB ===
MONGO_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
MONGO_DB = os.environ.get("MONGODB_DB", "monprojet")
MONGO_COLLECTION = os.environ.get("MONGODB_COLLECTION", "Projet")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
col = db[MONGO_COLLECTION]

print(f"[DEBUG] Connected to MongoDB: {MONGO_URI}, db={MONGO_DB}, col={MONGO_COLLECTION}")
print(f"[DEBUG] Total documents in collection: {col.count_documents({})}")

# === CACHE EN MÉMOIRE POUR LES STATS ===

"""
Petit système de cache en mémoire pour stocker temporairement
les statistiques coûteuses à calculer. Réduit la charge
sur MongoDB et accélère les appels répétés.
"""

STATS_CACHE = {}  # { key: {"value": ..., "ts": timestamp} }
def get_cached(key, ttl_seconds, compute_fn):
    now = time.time()
    entry = STATS_CACHE.get(key)
    if entry and (now - entry["ts"] < ttl_seconds):
        return entry["value"]

    value = compute_fn()
    STATS_CACHE[key] = {"value": value, "ts": now}
    return value

def invalidate_stats_cache():
    STATS_CACHE.clear()
    print("[DEBUG] STATS_CACHE invalidated")

# === Helpers ===

"""
Formate le champ Allergens pour l’affichage dans le frontend.
Convertit une liste d’allergènes en texte propre,
ou 'None' si aucun allergène n’est présent.
"""

def format_allergens_for_front(doc):
    val = doc.get("Allergens")

    # Nouveau format : liste
    if isinstance(val, list):
        cleaned = [
            str(a).strip()
            for a in val
            if str(a).strip() and str(a).strip().lower() != "none"
        ]
        if not cleaned:
            return "None"
        return ", ".join(sorted(cleaned))

    # Ancien format : string
    txt = (val or "").strip()
    if not txt or txt.lower() == "none":
        return "None"
    parts = [
        p.strip()
        for p in txt.split(",")
        if p.strip() and p.strip().lower() != "none"
    ]
    if not parts:
        return "None"
    return ", ".join(sorted(parts))

"""
Transforme un document MongoDB en un format cohérent
pour le frontend (renomme les champs, convertit les ID, etc.).
"""
def normalize(doc):
    return {
        "id": str(doc.get("_id")),
        "Food Product":    doc.get("Food_product", "") or "",
        "Supplier":        doc.get("Prefix", "") or "",
        "Main Ingredient": doc.get("Main_ingredient", "") or "",
        "Sweetener":       doc.get("Sweetener", "") or "",
        "Fat/Oil":         doc.get("Fat/Oil", "") or "",
        "Seasoning":       doc.get("Seasoning", "") or "",
        "Allergens":       format_allergens_for_front(doc),
        "Suffix":          doc.get("Suffix", "") or "",
    }


"""
Nettoie et normalise la valeur du champ Allergens.
Accepte une string ou une liste, et retourne toujours
une liste propre d’allergènes valides.
"""
def parse_allergens(value):
    if not value:
        return []

    if isinstance(value, list):
        return [
            str(v).strip()
            for v in value
            if str(v).strip() and str(v).strip().lower() != "none"
        ]
    txt = str(value).strip()
    if not txt or txt.lower() == "none":
        return []
    parts = [p.strip() for p in txt.split(",")]
    return [p for p in parts if p and p.lower() != "none"]


"""
Construit une requête Mongo à partir des filtres du frontend
"""
def build_query(args):
    clauses = []

    # recherche texte simple (regex)
    search = (args.get("search") or "").strip()
    if search:
        regex = {"$regex": re.escape(search), "$options": "i"}
        clauses.append({
            "$or": [
                {"Food_product": regex},
                {"Main_ingredient": regex},
                {"Sweetener": regex},
                {"Seasoning": regex},
                {"Fat/Oil": regex},
                {"Prefix": regex},
                {"Suffix": regex},
                # Pour les anciens docs string (rare après migration)
                {"Allergens": regex},
            ]
        })

    # filtres exacts
    mapping = {
        "supplier": "Prefix",
        "suffix": "Suffix",
        "main": "Main_ingredient",
        "sweet": "Sweetener",
        "fat": "Fat/Oil",
        "season": "Seasoning",
    }
    for param, field in mapping.items():
        val = (args.get(param) or "").strip()
        if val:
            clauses.append({field: val})

    # allergènes à éviter => Allergens ne doit contenir AUCUN des termes
    avoid_param = (args.get("avoid") or "").strip()
    if avoid_param:
        terms = [t.strip() for t in avoid_param.split(",") if t.strip()]
        if terms:
            # Si Allergens est une liste -> $nin
            clauses.append({"Allergens": {"$nin": terms}})

    # allergènes à inclure => Allergens doit contenir AU MOINS un des termes
    include_param = (args.get("include") or "").strip()
    if include_param:
        terms = [t.strip() for t in include_param.split(",") if t.strip()]
        if terms:
            clauses.append({"Allergens": {"$in": terms}})

    if not clauses:
        return {}
    if len(clauses) == 1:
        return clauses[0]
    return {"$and": clauses}


# === API PRODUITS (CRUD + pagination) ===
"""
Retourne une liste paginée des produits avec filtres, recherche
et tri. Utilisé par le frontend pour afficher les cartes produits.
"""

@app.get("/api/products")
def get_products():
    """
    Liste paginée des produits, avec filtres et tri.
    """
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 12))
    except ValueError:
        page, size = 1, 12

    page = max(page, 1)
    size = max(min(size, 200), 1)

    query = build_query(request.args)

    sort_param = request.args.get("sort", "name")
    if sort_param == "ingredient":
        sort_field = "Main_ingredient"
    else:
        sort_field = "Food_product"

    total = col.count_documents(query)
    skip = (page - 1) * size

    cursor = (
        col.find(query)
        .sort(sort_field, 1)
        .skip(skip)
        .limit(size)
    )

    items = [normalize(d) for d in cursor]

    print(f"[DEBUG] /api/products page={page} size={size} skip={skip} total={total} query={query}")

    return jsonify({
        "items": items,
        "page": page,
        "size": size,
        "total": total,
        "has_prev": page > 1,
        "has_next": skip + size < total,
    })



"""
Crée un nouveau produit dans la base après avoir nettoyé
et converti les allergènes envoyés.
Invalide le cache des statistiques.
"""

@app.post("/api/products")
def create_product():
    data = request.json or {}

    raw_allergens = (data.get("Allergens") or "").strip()
    if not raw_allergens or raw_allergens.lower() == "none":
        allergens_list = []
    else:
        allergens_list = [
            a.strip()
            for a in raw_allergens.split(",")
            if a.strip() and a.strip().lower() != "none"
        ]

    doc = {
        "Food_product":    data.get("Food Product", ""),
        "Prefix":          data.get("Supplier", ""),
        "Main_ingredient": data.get("Main Ingredient", ""),
        "Sweetener":       data.get("Sweetener", ""),
        "Fat/Oil":         data.get("Fat/Oil", ""),
        "Seasoning":       data.get("Seasoning", ""),
        "Allergens":       allergens_list,   # LISTE
        "Suffix":          data.get("Suffix", ""),
    }
    res = col.insert_one(doc)
    created = col.find_one({"_id": res.inserted_id})
    invalidate_stats_cache()
    return jsonify(normalize(created)), 201



"""MAJ produit existant. Les allergènes sont normalisés et le cache statistiques est vidé. """
@app.put("/api/products/<id>")
def update_product(id):
    try:
        oid = ObjectId(id)
    except Exception:
        return jsonify({"error": "Invalid id"}), 400

    data = request.json or {}

    raw_allergens = (data.get("Allergens") or "").strip()
    if not raw_allergens or raw_allergens.lower() == "none":
        allergens_list = []
    else:
        allergens_list = [
            a.strip()
            for a in raw_allergens.split(",")
            if a.strip() and a.strip().lower() != "none"
        ]

    update = {
        "Food_product":    data.get("Food Product", ""),
        "Prefix":          data.get("Supplier", ""),
        "Main_ingredient": data.get("Main Ingredient", ""),
        "Sweetener":       data.get("Sweetener", ""),
        "Fat/Oil":         data.get("Fat/Oil", ""),
        "Seasoning":       data.get("Seasoning", ""),
        "Allergens":       allergens_list,
        "Suffix":          data.get("Suffix", ""),
    }
    col.update_one({"_id": oid}, {"$set": update})

    invalidate_stats_cache()

    doc = col.find_one({"_id": oid})
    if not doc:
        return jsonify({"error": "Not found"}), 404
    return jsonify(normalize(doc))


"""Supprime un produit de la base. Invalide aussi le cache des stats.."""

@app.delete("/api/products/<id>")
def delete_product(id):
    try:
        oid = ObjectId(id)
    except Exception:
        return jsonify({"error": "Invalid id"}), 400

    res = col.delete_one({"_id": oid})
    invalidate_stats_cache()
    if not res.deleted_count:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"status": "deleted"})


# === IMPORT / EXPORT CSV ===
@app.post("/api/import/csv")
def import_csv():
    """
    Import de données au format CSV.
    Utilisation typique via Postman ou curl.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "No selected file"}), 400

    stream = io.StringIO(f.stream.read().decode("utf-8"))
    reader = csv.DictReader(stream)

    docs = []
    for row in reader:
        raw_allergens = (
            row.get("Allergens")
            or row.get("Allergen")
            or ""
        ).strip()
        if not raw_allergens or raw_allergens.lower() == "none":
            allergens_list = []
        else:
            allergens_list = [
                a.strip()
                for a in raw_allergens.split(",")
                if a.strip() and a.strip().lower() != "none"
            ]

        docs.append({
            "Food_product":    row.get("Food Product") or row.get("Food_product", ""),
            "Prefix":          row.get("Supplier") or row.get("Prefix", ""),
            "Main_ingredient": row.get("Main Ingredient") or row.get("Main_ingredient", ""),
            "Sweetener":       row.get("Sweetener", ""),
            "Fat/Oil":         row.get("Fat/Oil", ""),
            "Seasoning":       row.get("Seasoning", ""),
            "Allergens":       allergens_list,
            "Suffix":          row.get("Suffix", ""),
        })

    if not docs:
        return jsonify({"inserted": 0})

    res = col.insert_many(docs)
    invalidate_stats_cache()
    return jsonify({"inserted": len(res.inserted_ids)})


@app.get("/api/export/csv")
def export_csv():
    """
    Exporte les produits (avec les mêmes filtres que /api/products) au format CSV.
    """
    query = build_query(request.args)
    cursor = col.find(query).sort("Food_product", 1)

    def generate():
        header = [
            "Food Product",
            "Supplier",
            "Main Ingredient",
            "Sweetener",
            "Fat/Oil",
            "Seasoning",
            "Allergens",
            "Suffix",
        ]
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(header)
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        for doc in cursor:
            n = normalize(doc)
            writer.writerow([
                n["Food Product"],
                n["Supplier"],
                n["Main Ingredient"],
                n["Sweetener"],
                n["Fat/Oil"],
                n["Seasoning"],
                n["Allergens"],
                n["Suffix"],
            ])
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    filename = "see_allergens_export.csv"
    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


# === STATS / INDEXES GLOBAUX ===

"""
Génère des statistiques globales (listes distinctes, compteurs).
Utilise un cache de 10 minutes pour éviter de recalculer
l’ensemble des données trop souvent.
"""

@app.get("/api/stats/indexes")
def stats_indexes():
    print("[DEBUG] /api/stats/indexes called")

    def compute_indexes():
        def simple_index(field):
            pipeline = [
                {"$group": {"_id": f"${field}", "count": {"$sum": 1}}},
                {"$sort": {"count": -1, "_id": 1}},
            ]
            res = []
            for d in col.aggregate(pipeline):
                label = (d["_id"] or "").strip() or "—"
                res.append({"label": label, "count": d["count"]})
            return res

        # Allergènes
        pipeline_allergens = [
            {"$project": {
                "A": {
                    "$cond": [
                        {"$isArray": "$Allergens"},
                        "$Allergens",
                        {
                            "$cond": [
                                {"$and": [
                                    {"$ne": ["$Allergens", None]},
                                    {"$ne": ["$Allergens", ""]},
                                ]},
                                {"$split": ["$Allergens", ","]},
                                [],
                            ]
                        }
                    ]
                }
            }},
            {"$unwind": "$A"},
            {"$set": {"A": {"$trim": {"input": "$A"}}}},
            {"$match": {"A": {"$ne": "", "$ne": "None"}}},
            {"$group": {"_id": "$A", "count": {"$sum": 1}}},
            {"$sort": {"count": -1, "_id": 1}},
        ]
        allergens = [
            {"label": d["_id"], "count": d["count"]}
            for d in col.aggregate(pipeline_allergens)
        ]
        print(f"[DEBUG] allergens distinct = {len(allergens)}")

        main = simple_index("Main_ingredient")
        sweet = simple_index("Sweetener")
        fat = simple_index("Fat/Oil")
        season = simple_index("Seasoning")
        suppliers = simple_index("Prefix")
        suffixes = simple_index("Suffix")

        # Safe vs contains (None vs autres)
        free = list(col.aggregate([
            {"$project": {
                "hasAllergens": {
                    "$cond": [
                        {"$isArray": "$Allergens"},
                        {"$gt": [{"$size": "$Allergens"}, 0]},
                        {
                            "$not": {
                                "$regexMatch": {
                                    "input": {"$ifNull": ["$Allergens", "None"]},
                                    "regex": "^none$",
                                    "options": "i",
                                }
                            }
                        }
                    ]
                }
            }},
            {"$group": {
                "_id": {
                    "$cond": ["$hasAllergens", "contains", "none"]
                },
                "count": {"$sum": 1},
            }}
        ]))

        print(f"[DEBUG] freeFrom = {free}")

        return {
            "total": col.count_documents({}),
            "allergens": allergens,
            "main": main,
            "sweet": sweet,
            "fat": fat,
            "season": season,
            "suppliers": suppliers,
            "suffixes": suffixes,
            "freeFrom": [
                {"label": d["_id"], "count": d["count"]}
                for d in free
            ],
        }

    data = get_cached("indexes", ttl_seconds=3000, compute_fn=compute_indexes)
    return jsonify(data)


# === STATS ANALYTIQUES (charts, co-occur, etc.) ===
"""
Calcule des statistiques analytiques plus complexes :
co-occurrences d’allergènes, top ingrédients, graphes.
Résultats également mis en cache pour 50 minutes.
"""

@app.get("/api/stats/analytics")
def stats_analytics():
    print("[DEBUG] /api/stats/analytics called")

    def compute_analytics():
        allergen_counts = defaultdict(int)
        main_counts = defaultdict(int)
        sweet_counts = defaultdict(int)
        fat_counts = defaultdict(int)
        by_main = defaultdict(lambda: defaultdict(int))
        node_counts = defaultdict(int)
        edge_counts = defaultdict(int)

        cursor = col.find(
            {},
            {
                "_id": 0,
                "Main_ingredient": 1,
                "Sweetener": 1,
                "Fat/Oil": 1,
                "Seasoning": 1,
                "Allergens": 1,
            },
        )

        for doc in cursor:
            main = (doc.get("Main_ingredient") or "—").strip() or "—"
            sweet = (doc.get("Sweetener") or "—").strip() or "—"
            fat = (doc.get("Fat/Oil") or "—").strip() or "—"

            main_counts[main] += 1
            sweet_counts[sweet] += 1
            fat_counts[fat] += 1

            allergens = parse_allergens(doc.get("Allergens"))
            if not allergens:
                continue

            for a in allergens:
                allergen_counts[a] += 1
                node_counts[a] += 1
                by_main[main][a] += 1

            uniq = sorted(set(allergens))
            for i in range(len(uniq)):
                for j in range(i + 1, len(uniq)):
                    pair = (uniq[i], uniq[j])
                    edge_counts[pair] += 1

        def to_sorted_list(dct, top=None):
            items = sorted(dct.items(), key=lambda kv: (-kv[1], kv[0]))
            if top is not None:
                items = items[:top]
            return [{"label": k, "count": v} for k, v in items]

        top_allergens = to_sorted_list(allergen_counts, top=10)
        top_mains = to_sorted_list(main_counts, top=10)
        sweet_list = to_sorted_list(sweet_counts, top=10)
        fat_list = to_sorted_list(fat_counts, top=10)

        by_main_out = {}
        for main, a_counts in by_main.items():
            by_main_out[main] = {
                "total": sum(a_counts.values()),
                "allergens": to_sorted_list(a_counts, top=15),
            }

        nodes = to_sorted_list(node_counts)
        edges_items = sorted(edge_counts.items(), key=lambda kv: -kv[1])[:300]
        edges = [
            {"source": a, "target": b, "count": c}
            for (a, b), c in edges_items
        ]

        return {
            "topAllergens": top_allergens,
            "topMains": top_mains,
            "sweetCounts": sweet_list,
            "fatCounts": fat_list,
            "byMain": by_main_out,
            "cooc": {
                "nodes": [{"id": n["label"], "count": n["count"]} for n in nodes],
                "edges": edges,
            },
        }

    data = get_cached("analytics", ttl_seconds=3000, compute_fn=compute_analytics)
    return jsonify(data)


# === FRONTEND STATIC  ===
FRONTEND_DIR = pathlib.Path(__file__).parent

@app.route("/")
def serve_root():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)


if __name__ == "__main__":
    debug_flag = bool(int(os.getenv("FLASK_DEBUG", "1")))
    app.run(host="0.0.0.0", port=5000, debug=debug_flag)
