from pymongo import MongoClient, errors
import bcrypt

uri = "mongodb+srv://gabriellazovsky_db_user:67PdWTyuQV8tlRYR@clustermaverick.cymy94z.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

try:
    db = client["banco"]
    clientes = db["clientes"]

    # Crear índice único en nombredeusuario (si no existe)
    clientes.create_index("nombredeusuario", unique=True)

    # ---------- HASH de la contraseña ----------
    contraseña_plana = "MiClaveSegura123"
    contraseña_hash = bcrypt.hashpw(contraseña_plana.encode("utf-8"), bcrypt.gensalt())

    # ---------- INSERTAR ----------
    nuevo_cliente = {
        "dni": "12345678A",
        "nombre": "Javier",
        "apellido": "Gonzalez",
        "nombredeusuario": "javierg",
        "contraseña": contraseña_hash,        # contraseña encriptada
        "saldo": 1500.50,
        "ahorro_aportado": 3.5,               # Ahorro aportado
        "financiacion_necesaria": 3.5,        # Financiación necesaria
        "cuentas": [
            {"tipo": "Ahorro", "numero": "ES12 3456 7890 1234", "saldo": 1200},
            {"tipo": "Corriente", "numero": "ES98 7654 3210 9876", "saldo": 300.5}
        ]
    }

    try:
        resultado = clientes.insert_one(nuevo_cliente)
        print("Cliente insertado con ID:", resultado.inserted_id)
    except errors.DuplicateKeyError:
        print("Error: El nombredeusuario ya existe.")

    # ---------- LEER (FIND ONE) ----------
    cliente = clientes.find_one({"nombredeusuario": "javierg"})
    print("\nCliente encontrado:")
    # Para mostrar la contraseña en formato legible, decodificamos a string (opcional)
    if cliente:
        cliente["contraseña"] = cliente["contraseña"].decode("utf-8")
    print(cliente)

    # ---------- LEER TODOS LOS CLIENTES ----------
    print("\nTodos los clientes en la base de datos:")
    for c in clientes.find():
        c["contraseña"] = c["contraseña"].decode("utf-8")
        print(c)

except Exception as e:
    print("Error:", e)
finally:
    client.close()
