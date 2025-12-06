import os
import pathlib
from dotenv import load_dotenv
from pymongo import MongoClient

BASE_DIR = pathlib.Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

MONGO_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
MONGO_DB = os.environ.get("MONGODB_DB", "monprojet")
MONGO_COLLECTION = os.environ.get("MONGODB_COLLECTION", "Projet")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
col = db[MONGO_COLLECTION]

def migrate_fast():
    """
    Migration côté serveur :
    - Si Allergens est une string -> on convertit en liste propre.
    - Sinon (déjà liste, null, etc.) -> on laisse tel quel.
    """
    result = col.update_many(
        {},   # on traite tous les documents avec une condition
        [
            {
                "$set": {
                    "Allergens": {
                        "$cond": [
                            #  si "string"
                            {"$eq": [ {"$type": "$Allergens"}, "string" ]},

                            #  on transforme
                            {
                                "$filter": {
                                    "input": {
                                        "$map": {
                                            "input": { "$split": ["$Allergens", ","] },
                                            "as": "a",
                                            "in": { "$trim": { "input": "$$a" } }
                                        }
                                    },
                                    "as": "x",
                                    "cond": {
                                        "$and": [
                                            { "$ne": ["$$x", ""] },
                                            {
                                                "$ne": [
                                                    { "$toLower": "$$x" },
                                                    "none"
                                                ]
                                            }
                                        ]
                                    }
                                }
                            },

                            #  on garde la valeur telle quelle (liste, null, etc.)
                            "$Allergens"
                        ]
                    }
                }
            }
        ]
    )

    print(f"Matched documents : {result.matched_count}")
    print(f"Modified documents: {result.modified_count}")

if __name__ == "__main__":
    migrate_fast()

"""
Ce script convertit, directement côté MongoDB, les champs 'Allergens' au format string
en listes nettoyées, sans toucher aux documents où 'Allergens' est déjà une liste.
Il utilise update_many + pipeline d’agrégation, beaucoup plus rapide qu'une boucle Python.
"""
