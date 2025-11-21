from pymongo import MongoClient, errors
import random
import string

# Conexión a MongoDB
uri = "mongodb+srv://javierriosmontes_db_user:FKxFGWWMhsZMCycb@accenturecluster.zfw78s2.mongodb.net/?appName=AccentureCluster"
client = MongoClient(uri)

def generar_usuario(nombre, apellido, existentes):
    base = (nombre[0] + apellido).lower()
    usuario = base
    i = 1
    while usuario in existentes:
        usuario = f"{base}{i}"
        i += 1
    existentes.add(usuario)
    return usuario

def generar_contraseña(longitud=10):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(longitud))

try:
    db = client["banco"]
    clientes = db["clientes"]

    # Crear índice único en nombredeusuario
    clientes.create_index("nombredeusuario", unique=True, sparse=True)

    usuarios_existentes = set(
        c['nombredeusuario'] for c in clientes.find({"nombredeusuario": {"$exists": True}})
    )

    nombres = ["Javier", "Laura", "Carlos", "Ana", "Miguel"]
    apellidos = ["Gonzalez", "Perez", "Lopez", "Martinez", "Ramirez"]

    for i in range(10):
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)

        ahorro_aportado = round(random.uniform(500.0, 5000.0), 2)
        financiacion_necesaria = round(random.uniform(1000.0, 10000.0), 2)
        valor_vivienda = round(ahorro_aportado + financiacion_necesaria, 2)

        ingresos_mensuales = round(random.uniform(1200.0, 6000.0), 2)
        gastos_mensuales = round(random.uniform(300.0, 2000.0), 2)

        dti = round(gastos_mensuales / ingresos_mensuales, 3) if ingresos_mensuales > 0 else 0.0
        ltv = round(financiacion_necesaria / valor_vivienda, 3)

        plazo_anios = random.choice([10, 15, 20, 25, 30])
        edad = random.randint(21, 70)
        antiguedad_laboral = random.randint(0, 30)
        credit_score = random.randint(300, 850)

        nuevo_cliente = {
            "dni": f"{random.randint(10000000, 99999999)}{random.choice(string.ascii_uppercase)}",
            "nombre": nombre,
            "apellido": apellido,
            "nombredeusuario": generar_usuario(nombre, apellido, usuarios_existentes),
            "contraseña": generar_contraseña(),

            # VARIABLES PARA EL MODELO
            "interes_hipoteca": round(random.uniform(2.0, 5.0), 2),
            "ahorro_aportado": ahorro_aportado,
            "financiacion_necesaria": financiacion_necesaria,
            "valor_vivienda": valor_vivienda,
            "ltv": ltv,
            "plazo_anios": plazo_anios,
            "ingresos_mensuales": ingresos_mensuales,
            "gastos_mensuales": gastos_mensuales,
            "dti": dti,
            "edad": edad,
            "antiguedad_laboral": antiguedad_laboral,
            "credit_score": credit_score,

            # Información bancaria extra
            "saldo": round(random.uniform(100.0, 10000.0), 2),
            "cuentas": [
                {
                    "tipo": "Ahorro",
                    "numero": f"ES{random.randint(10**11, 10**12 - 1)}",
                    "saldo": round(random.uniform(100.0, 5000.0), 2)
                },
                {
                    "tipo": "Corriente",
                    "numero": f"ES{random.randint(10**11, 10**12 - 1)}",
                    "saldo": round(random.uniform(50.0, 3000.0), 2)
                }
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
