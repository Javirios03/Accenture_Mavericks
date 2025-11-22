# añadir_usuario.py
from pymongo import MongoClient
import random

# Conexión a MongoDB
uri = "mongodb+srv://javierriosmontes_db_user:FKxFGWWMhsZMCycb@accenturecluster.zfw78s2.mongodb.net/?appName=AccentureCluster"
client = MongoClient(uri)
db = client["banco"]
clientes = db["clientes"]

# Datos de Francisco Javier Ríos
ahorro_aportado = round(random.uniform(5000.0, 15000.0), 2)
financiacion_necesaria = round(random.uniform(100000.0, 250000.0), 2)
valor_vivienda = round(ahorro_aportado + financiacion_necesaria, 2)

ingresos_mensuales = round(random.uniform(2500.0, 5000.0), 2)
gastos_mensuales = round(random.uniform(800.0, 1500.0), 2)

dti = round(gastos_mensuales / ingresos_mensuales, 3) if ingresos_mensuales > 0 else 0.0
ltv = round(financiacion_necesaria / valor_vivienda, 3)

plazo_anios = random.choice([20, 25, 30])
edad = 25  # O tu edad real
antiguedad_laboral = random.randint(2, 5)
credit_score = random.randint(650, 800)

nuevo_cliente = {
    "dni": "12345678A",
    "nombre": "Francisco Javier",
    "apellido": "Ríos",
    "nombredeusuario": "friosrios",
    "contraseña": "Password123!",

    # VARIABLES PARA EL MODELO
    "interes_hipoteca": round(random.uniform(2.5, 4.5), 2),  # Temporal, se recalculará
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
    "saldo": round(random.uniform(5000.0, 20000.0), 2),
    "cuentas": [
        {
            "tipo": "Ahorro",
            "numero": f"ES{random.randint(10**11, 10**12 - 1)}",
            "saldo": round(random.uniform(3000.0, 10000.0), 2)
        },
        {
            "tipo": "Corriente",
            "numero": f"ES{random.randint(10**11, 10**12 - 1)}",
            "saldo": round(random.uniform(1000.0, 5000.0), 2)
        }
    ]
}

try:
    # Verificar si ya existe
    existente = clientes.find_one({"dni": "12345678A"})
    if existente:
        print("⚠️ El usuario ya existe. Actualizando...")
        clientes.update_one({"dni": "12345678A"}, {"$set": nuevo_cliente})
        print("✅ Usuario actualizado")
    else:
        resultado = clientes.insert_one(nuevo_cliente)
        print(f"✅ Usuario Francisco Javier Ríos insertado con ID: {resultado.inserted_id}")
    
    print("\n📋 Datos del usuario:")
    print(f"DNI: {nuevo_cliente['dni']}")
    print(f"Nombre: {nuevo_cliente['nombre']} {nuevo_cliente['apellido']}")
    print(f"Financiación necesaria: {nuevo_cliente['financiacion_necesaria']}€")
    print(f"Valor vivienda: {nuevo_cliente['valor_vivienda']}€")
    print(f"Plazo: {nuevo_cliente['plazo_anios']} años")
    print(f"Ingresos mensuales: {nuevo_cliente['ingresos_mensuales']}€")
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    client.close()
