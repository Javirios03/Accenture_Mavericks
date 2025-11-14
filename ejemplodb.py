from pymongo import MongoClient, errors
import random
import string

# Conexión a MongoDB
uri = "mongodb+srv://gabriellazovsky_db_user:67PdWTyuQV8tlRYR@clustermaverick.cymy94z.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

def generar_usuario(nombre, apellido, existentes):
    """Genera un nombre de usuario único."""
    base = (nombre[0] + apellido).lower()
    usuario = base
    i = 1
    while usuario in existentes:
        usuario = f"{base}{i}"
        i += 1
    existentes.add(usuario)
    return usuario

def generar_contraseña(longitud=10):
    """Genera una contraseña aleatoria."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(longitud))

try:
    db = client["banco"]
    clientes = db["clientes"]

    # Crear índice único en nombredeusuario
    clientes.create_index("nombredeusuario", unique=True, sparse=True)

    # Para controlar usuarios ya existentes
    usuarios_existentes = set(c['nombredeusuario'] for c in clientes.find({"nombredeusuario": {"$exists": True}}))

    # ---------- GENERAR MÚLTIPLES CLIENTES ----------
    nombres = ["Javier", "Laura", "Carlos", "Ana", "Miguel"]
    apellidos = ["Gonzalez", "Perez", "Lopez", "Martinez", "Ramirez"]

    for i in range(10):  # Generar 10 clientes de ejemplo
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)

        nuevo_cliente = {
            "dni": f"{random.randint(10000000,99999999)}{random.choice(string.ascii_uppercase)}",
            "nombre": nombre,
            "apellido": apellido,
            "nombredeusuario": generar_usuario(nombre, apellido, usuarios_existentes),
            "contraseña": generar_contraseña(),
            "interes_hipoteca": round(random.uniform(2.0, 5.0), 2),
            "ahorro_aportado": round(random.uniform(500.0, 5000.0), 2),
            "financiacion_necesaria": round(random.uniform(1000.0, 10000.0), 2),
            "saldo": round(random.uniform(100.0, 10000.0), 2),
            "cuentas": [
                {"tipo": "Ahorro", "numero": f"ES{random.randint(10**11, 10**12-1)}", "saldo": round(random.uniform(100.0, 5000.0), 2)},
                {"tipo": "Corriente", "numero": f"ES{random.randint(10**11, 10**12-1)}", "saldo": round(random.uniform(50.0, 3000.0), 2)}
            ]
        }

        try:
            resultado = clientes.insert_one(nuevo_cliente)
            print(f"Cliente insertado: {nuevo_cliente['nombredeusuario']} con ID {resultado.inserted_id}")
        except errors.DuplicateKeyError:
            print(f"El usuario {nuevo_cliente['nombredeusuario']} ya existe. Se omite.")

except Exception as e:
    print("Error:", e)
finally:
    client.close()
