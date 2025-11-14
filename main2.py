from pymongo import MongoClient

uri = "mongodb+srv://gabriellazovsky_db_user:67PdWTyuQV8tlRYR@clustermaverick.cymy94z.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

try:
    # Prueba básica: listar las bases de datos
    print("Conectando...")
    print(client.list_database_names())   # <--- si ves una lista, funciona
    print("Conexión OK")
except Exception as e:
    print("Error:", e)
finally:
    client.close()
