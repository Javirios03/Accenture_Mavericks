# clientes_a_diccionarios.py
from pymongo import MongoClient

# Conexión a MongoDB
uri = "mongodb+srv://gabriellazovsky_db_user:67PdWTyuQV8tlRYR@clustermaverick.cymy94z.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

def obtener_clientes():
    """Devuelve una lista de diccionarios con todos los clientes."""
    try:
        db = client["banco"]
        clientes = db["clientes"]

        # Obtener todos los documentos como diccionarios
        lista_clientes = list(clientes.find({}, {"_id": 0}))  # Se excluye el _id si no se necesita
        return lista_clientes

    except Exception as e:
        print("Error al obtener clientes:", e)
        return []
    finally:
        client.close()

if __name__ == "__main__":
    clientes = obtener_clientes()
    for cliente in clientes:
        print(cliente)  # Aquí se puede hacer cualquier bucle o procesamiento
