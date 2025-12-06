import os
import pathlib
from dotenv import load_dotenv
from pymongo import MongoClient, TEXT

BASE_DIR = pathlib.Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

MONGO_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
MONGO_DB = os.environ.get("MONGODB_DB", "monprojet")
MONGO_COLLECTION = os.environ.get("MONGODB_COLLECTION", "Projet")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
col = db[MONGO_COLLECTION]

print(f"Connected to {MONGO_URI}, db={MONGO_DB}, col={MONGO_COLLECTION}")

# Index simples
col.create_index("Food_product")
col.create_index("Prefix")
col.create_index("Main_ingredient")
col.create_index("Sweetener")
col.create_index("Fat/Oil")
col.create_index("Seasoning")
col.create_index("Suffix")
col.create_index("Allergens")

"""""
Ces index accélèrent les filtres les plus utilisés dans l’API :
- Food_product (nom du produit)
- Prefix (fournisseur)
- Main_ingredient
- Sweetener
- Fat/Oil
- Seasoning
- Suffix
- Allergens (stockés sous forme de liste)
MongoDB n’a plus besoin de parcourir toute la collection 
pour répondre aux requêtes de filtrage
"""

# Index texte global pour la recherche
col.create_index([
    ("Food_product", TEXT),
    ("Main_ingredient", TEXT),
    ("Sweetener", TEXT),
    ("Seasoning", TEXT),
    ("Fat/Oil", TEXT),
    ("Prefix", TEXT),
    ("Suffix", TEXT),
], name="text_global")

print("Indexes created.")

"""
--------------------
Permet la recherche textuelle multi-champs (via `$text`) sur :
Food_product, Main_ingredient, Sweetener, Seasoning, Fat/Oil, Prefix, Suffix.
Utile pour la barre de recherche générale, car il accélère les recherches
en plein texte sur plusieurs champs en même temps.

"""
