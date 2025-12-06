import time
import statistics
import requests
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

# ================================
# CONFIG GLOBALE
# ================================

BASE_URL = "http://127.0.0.1:5000"

# Juste un label pour tes résultats (taille de la BDD, dump, etc.)
DB_SIZE_LABEL = "1Go_11.8M_docs"

# Fichiers CSV de sortie
DETAIL_OUTPUT_FILE = "bench_all_results.csv"      # une ligne par requête
SUMMARY_OUTPUT_FILE = "bench_all_summary.csv"     # une ligne par (scénario, conc)

"""
Chaque scénario contient :
- path        : l’URL relative
- requests    : nombre total de requêtes à envoyer
- concurrency : liste de niveaux de concurrence à tester
"""
SCENARIOS = {
    # --- Effet du pageSize ---
    "products_size_12": {
        "path": "/api/products?page=1&size=12",
        "requests": 50,
        "concurrency": [1, 5, 10, 20],
    },
    "products_size_48": {
        "path": "/api/products?page=1&size=48",
        "requests": 50,
        "concurrency": [1, 5, 10, 20],
    },
    "products_size_200": {
        "path": "/api/products?page=1&size=200",
        "requests": 50,
        "concurrency": [1, 5, 10, 20],
    },

    # --- Recherche texte (impact index texte) ---
    "products_search": {
        "path": "/api/products?page=1&size=12&search=Milk",
        "requests": 10,          # plus lourd → moins de requêtes
        "concurrency": [1, 3],
    },

    # --- Stats avec cache applicatif ---
    "stats_indexes": {
        "path": "/api/stats/indexes",
        "requests": 20,
        "concurrency": [1, 5],
    },
    "stats_analytics": {
        "path": "/api/stats/analytics",
        "requests": 3,           # très lourd
        "concurrency": [1],
    },
}

# Scénarios qui utilisent le cache applicatif côté serveur
CACHE_SCENARIOS = {"stats_indexes", "stats_analytics"}


# ================================
# HELPERS
# ================================

def do_request(url: str):
    """Envoie UNE requête HTTP GET et renvoie (latence_ms, status_code)."""
    t0 = time.perf_counter()
    try:
        r = requests.get(url)
        dt_ms = (time.perf_counter() - t0) * 1000.0
        return dt_ms, r.status_code
    except Exception:
        # On considère une exception comme une grosse latence + erreur
        dt_ms = (time.perf_counter() - t0) * 1000.0
        return dt_ms, 0  # 0 = code d’erreur custom


def p95(times):
    """Calcule le percentile 95 avec une approximation si peu de points."""
    if not times:
        return 0.0
    if len(times) < 20:
        return max(times)
    return statistics.quantiles(times, n=20)[18]


def run_scenario(name: str, config: dict, detail_writer, summary_writer):
    """
    Lance toutes les requêtes d’un scénario pour chaque niveau de concurrence,
    enregistre chaque requête dans le CSV détaillé, et ajoute un résumé
    (latence moyenne, P95, erreurs, throughput) dans le CSV de synthèse.
    """
    path = config["path"]
    total_requests = config["requests"]
    conc_levels = config["concurrency"]

    url = BASE_URL + path
    cache_aware = name in CACHE_SCENARIOS

    for idx_conc, conc in enumerate(conc_levels):
        # Pour les scénarios de cache, on considère :
        # - premier niveau de concurrence = cache "cold"
        # - les suivants = cache "warm"
        cache_state = "cold" if (cache_aware and idx_conc == 0) else "warm"

        print(
            f"\n=== Scénario: {name} | Concurrence: {conc} | "
            f"Requêtes: {total_requests} | Cache: {cache_state} ==="
        )

        times = []
        status_codes = []

        # Mesure de la durée totale du batch (pour le throughput)
        batch_start = time.perf_counter()

        # Envoi des requêtes en parallèle
        with ThreadPoolExecutor(max_workers=conc) as executor:
            futures = [
                executor.submit(do_request, url)
                for _ in range(total_requests)
            ]

            for i, fut in enumerate(as_completed(futures)):
                lat_ms, status = fut.result()
                times.append(lat_ms)
                status_codes.append(status)

                # Écriture ligne par ligne dans le CSV détaillé
                detail_writer.writerow([
                    DB_SIZE_LABEL,
                    name,
                    path,
                    conc,
                    cache_state,
                    i,
                    f"{lat_ms:.2f}",
                    status,
                ])

        batch_duration = time.perf_counter() - batch_start
        throughput = total_requests / batch_duration if batch_duration > 0 else 0.0

        # Stats récap
        errors = sum(1 for s in status_codes if s != 200)
        if times:
            avg = statistics.mean(times)
            p95_val = p95(times)
        else:
            avg = p95_val = 0.0

        print(f"  -> Moyenne : {avg:.2f} ms")
        print(f"  -> P95     : {p95_val:.2f} ms")
        print(f"  -> Erreurs : {errors}/{len(status_codes)}")
        print(f"  -> Throughput : {throughput:.2f} req/s")

        # Ligne de synthèse pour ce (scénario, concurrence)
        summary_writer.writerow([
            DB_SIZE_LABEL,
            name,
            path,
            conc,
            cache_state,
            total_requests,
            f"{batch_duration:.4f}",
            f"{throughput:.2f}",
            f"{avg:.2f}",
            f"{p95_val:.2f}",
            errors,
        ])


def main():
    print(f"Base URL: {BASE_URL}")
    print(f"Résultats détaillés dans : {DETAIL_OUTPUT_FILE}")
    print(f"Résumé dans : {SUMMARY_OUTPUT_FILE}")

    with open(DETAIL_OUTPUT_FILE, "w", newline="") as f_detail, \
         open(SUMMARY_OUTPUT_FILE, "w", newline="") as f_summary:

        detail_writer = csv.writer(f_detail)
        summary_writer = csv.writer(f_summary)

        # CSV détaillé : une ligne par requête
        detail_writer.writerow([
            "db_size",
            "scenario",
            "endpoint",
            "concurrency",
            "cache_state",   # cold / warm (pour stats_* surtout)
            "run_index",
            "latency_ms",
            "status_code",
        ])

        # CSV de synthèse : une ligne par (scénario, concurrence)
        summary_writer.writerow([
            "db_size",
            "scenario",
            "endpoint",
            "concurrency",
            "cache_state",
            "total_requests",
            "batch_duration_s",
            "throughput_rps",
            "avg_latency_ms",
            "p95_latency_ms",
            "errors",
        ])

        for name, cfg in SCENARIOS.items():
            run_scenario(name, cfg, detail_writer, summary_writer)

    print("\nTous les scénarios ont été exécutés.")


if __name__ == "__main__":
    main()
