from pymongo import MongoClient

uri = "mongodb+srv://gabriellazovsky_db_user:67PdWTyuQV8tlRYR@clustermaverick.cymy94z.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

try:
    db = client["banco"]          # Base de datos "banco"
    clientes = db["clientes"]     # Colección "clientes"

    # ---------- INSERTAR ----------
    nuevo_cliente = {
        "dni": "12345678A",
        "nombre": "Javier",
        "apellido": "Gonzalez",
        "saldo": 1500.50,
        "cuentas": [
            {"tipo": "Ahorro", "numero": "ES12 3456 7890 1234", "saldo": 1200},
            {"tipo": "Corriente", "numero": "ES98 7654 3210 9876", "saldo": 300.5}
        ]
    }

    resultado = clientes.insert_one(nuevo_cliente)
    print("Cliente insertado con ID:", resultado.inserted_id)

    # ---------- LEER (FIND ONE) ----------
    cliente = clientes.find_one({"dni": "12345678A"})
    print("\nCliente encontrado:")
    print(cliente)

    # ---------- LEER TODOS LOS CLIENTES ----------
    print("\nTodos los clientes en la base de datos:")
    for c in clientes.find():
        print(c)

except Exception as e:
    print("Error:", e)
finally:
    client.close()
