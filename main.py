from pymongo import MongoClient

uri = "mongodb+srv://gabriellazovsky_db_user:67PdWTyuQV8tlRYR@clustermaverick.cymy94z.mongodb.net/?appName=ClusterMaverick"

client = MongoClient(uri)

try:
    db = client["admin"]
    db.command({"ping": 1})
    print("Pinged your deployment. You successfully connected to MongoDB!")
finally:
    client.close()
