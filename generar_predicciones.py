# generar_predicciones.py - VERSIÓN COMPLETA Y REALISTA
from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
import json
from datetime import datetime, timedelta
import random

# Conexión a MongoDB
uri = "mongodb+srv://javierriosmontes_db_user:FKxFGWWMhsZMCycb@accenturecluster.zfw78s2.mongodb.net/?appName=AccentureCluster"
client = MongoClient(uri)

FEATURES = [
    "ahorro_aportado",
    "financiacion_necesaria",
    "valor_vivienda",
    "ltv",
    "plazo_anios",
    "ingresos_mensuales",
    "gastos_mensuales",
    "dti",
    "edad",
    "antiguedad_laboral",
    "credit_score",
]

TARGET = "interes_hipoteca"

def obtener_clientes():
    """Obtiene todos los clientes de MongoDB"""
    try:
        db = client["banco"]
        clientes = db["clientes"]
        lista_clientes = list(clientes.find({}, {"_id": 0}))
        return lista_clientes
    except Exception as e:
        print(f"❌ Error al obtener clientes: {e}")
        return []

def entrenar_modelo(clientes_dicts):
    """Entrena el modelo XGBoost"""
    df = pd.DataFrame(clientes_dicts)
    df = df.dropna(subset=FEATURES + [TARGET])

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("model", XGBRegressor(
                n_estimators=300,
                learning_rate=0.05,
                max_depth=4,
                subsample=0.8,
                colsample_bytree=0.8,
                objective="reg:squarederror",
                n_jobs=-1,
                tree_method="hist",
            ))
        ]
    )

    pipeline.fit(X_train, y_train)
    return pipeline

def predecir_para_cliente(cliente_dict, modelo):
    """Predice el tipo de interés para un cliente"""
    x = [[cliente_dict[f] for f in FEATURES]]
    tipo_pred = modelo.predict(x)[0]
    return round(float(tipo_pred), 2)

def calcular_cuota_mensual(capital, tasa_anual, plazo_anios):
    """Calcula la cuota mensual usando la fórmula de amortización francesa"""
    tasa_mensual = tasa_anual / 100 / 12
    num_pagos = plazo_anios * 12
    
    if tasa_mensual == 0:
        return capital / num_pagos
    
    cuota = capital * (tasa_mensual * (1 + tasa_mensual)**num_pagos) / ((1 + tasa_mensual)**num_pagos - 1)
    return round(cuota, 2)

def calcular_condiciones_completas(cliente, tipo_interes):
    """Calcula todas las condiciones de la hipoteca"""
    
    # Datos básicos
    financiacion = cliente.get('financiacion_necesaria', 0)
    plazo_anios = cliente.get('plazo_anios', 25)
    valor_vivienda = cliente.get('valor_vivienda', 0)
    ahorro = cliente.get('ahorro_aportado', 0)
    ingresos = cliente.get('ingresos_mensuales', 0)
    ltv = cliente.get('ltv', 0)
    dti = cliente.get('dti', 0)
    
    # Cálculos financieros
    cuota_mensual = calcular_cuota_mensual(financiacion, tipo_interes, plazo_anios)
    total_pagos = cuota_mensual * plazo_anios * 12
    total_intereses = total_pagos - financiacion
    esfuerzo_mensual = (cuota_mensual / ingresos * 100) if ingresos > 0 else 0
    
    # Gastos adicionales (típicos en España)
    comision_apertura = financiacion * random.uniform(0.005, 0.01)  # 0.5% - 1%
    gastos_notaria = random.uniform(600, 1200)
    gastos_registro = random.uniform(400, 800)
    tasacion = random.uniform(250, 400)
    gestoria = random.uniform(300, 600)
    total_gastos_iniciales = comision_apertura + gastos_notaria + gastos_registro + tasacion + gestoria
    
    # Tipo de préstamo (basado en score y LTV)
    credit_score = cliente.get('credit_score', 700)
    if credit_score > 750 and ltv < 0.7:
        tipo_prestamo = "Fijo"
        periodo_revision = None
    elif credit_score > 700:
        tipo_prestamo = "Mixto (5 años fijo)"
        periodo_revision = "5 años"
    else:
        tipo_prestamo = "Variable (Euribor + 1.2%)"
        periodo_revision = "Anual"
    
    # Comisiones
    comision_amortizacion_anticipada = random.choice(["0%", "0.5% parcial / 1% total", "Sin penalización"])
    
    # Productos vinculados
    vinculacion = []
    if tipo_interes < 3.0:
        vinculacion.extend(["Domiciliación de nómina", "Seguro de hogar", "Seguro de vida"])
    elif tipo_interes < 3.5:
        vinculacion.extend(["Domiciliación de nómina", "Seguro de hogar"])
    else:
        vinculacion.append("Domiciliación de nómina")
    
    # Estado y fechas
    estados = ["Pre-aprobado", "Aprobado", "En estudio"]
    estado = random.choice(estados)
    fecha_solicitud = datetime.now() - timedelta(days=random.randint(5, 30))
    fecha_validez = datetime.now() + timedelta(days=random.randint(30, 90))
    
    return {
        # Información financiera principal
        "tipo_interes": f"{tipo_interes}%",
        "tipo_prestamo": tipo_prestamo,
        "periodo_revision": periodo_revision,
        "plazo_anios": plazo_anios,
        "financiacion_necesaria": f"{financiacion:,.2f}€",
        "valor_vivienda": f"{valor_vivienda:,.2f}€",
        "ahorro_aportado": f"{ahorro:,.2f}€",
        
        # Cuotas y pagos
        "cuota_mensual": f"{cuota_mensual:,.2f}€",
        "total_a_pagar": f"{total_pagos:,.2f}€",
        "total_intereses": f"{total_intereses:,.2f}€",
        
        # Ratios
        "ltv": f"{ltv * 100:.2f}%",
        "dti": f"{dti * 100:.2f}%",
        "esfuerzo_mensual": f"{esfuerzo_mensual:.2f}%",
        
        # Comisiones y gastos
        "comision_apertura": f"{comision_apertura:,.2f}€",
        "comision_amortizacion_anticipada": comision_amortizacion_anticipada,
        "gastos_iniciales": {
            "notaria": f"{gastos_notaria:,.2f}€",
            "registro": f"{gastos_registro:,.2f}€",
            "tasacion": f"{tasacion:,.2f}€",
            "gestoria": f"{gestoria:,.2f}€",
            "total": f"{total_gastos_iniciales:,.2f}€"
        },
        
        # Vinculación
        "productos_vinculados": vinculacion,
        
        # Estado
        "estado": estado,
        "fecha_solicitud": fecha_solicitud.strftime("%d/%m/%Y"),
        "valido_hasta": fecha_validez.strftime("%d/%m/%Y"),
        
        # Información del cliente
        "ingresos_mensuales": f"{ingresos:,.2f}€"
    }

if __name__ == "__main__":
    print("=" * 70)
    print("🏦 GENERANDO PREDICCIONES COMPLETAS DE HIPOTECAS")
    print("=" * 70)
    
    # 1. Obtener clientes
    print("\n1️⃣ Obteniendo clientes de MongoDB...")
    clientes = obtener_clientes()
    print(f"   ✅ {len(clientes)} clientes recuperados")
    
    if len(clientes) == 0:
        print("   ❌ No hay clientes en la base de datos")
        exit(1)
    
    # 2. Entrenar modelo
    print("\n2️⃣ Entrenando modelo de predicción...")
    modelo = entrenar_modelo(clientes)
    print("   ✅ Modelo entrenado")
    
    # 3. Generar predicciones para cada cliente
    print("\n3️⃣ Generando predicciones completas para cada cliente...")
    predicciones = []
    
    for cliente in clientes:
        nombre_completo = f"{cliente.get('nombre', '')} {cliente.get('apellido', '')}".strip()
        dni = cliente.get('dni', 'N/A')
        
        try:
            tipo_interes = predecir_para_cliente(cliente, modelo)
            condiciones = calcular_condiciones_completas(cliente, tipo_interes)
            
            prediccion = {
                "nombre_completo": nombre_completo,
                "nombre": cliente.get('nombre', ''),
                "apellido": cliente.get('apellido', ''),
                "dni": dni,
                "condiciones_hipoteca": condiciones,
                "resumen": (
                    f"Hipoteca para {nombre_completo} (DNI: {dni}): "
                    f"Tipo {condiciones['tipo_interes']} {condiciones['tipo_prestamo']}, "
                    f"cuota mensual de {condiciones['cuota_mensual']}, "
                    f"plazo de {condiciones['plazo_anios']} años. "
                    f"Estado: {condiciones['estado']}."
                )
            }
            
            predicciones.append(prediccion)
            print(f"   ✅ {nombre_completo}: {tipo_interes}% - Cuota: {condiciones['cuota_mensual']}")
            
        except Exception as e:
            print(f"   ⚠️ Error con {nombre_completo}: {e}")
    
    # 4. Guardar en JSON
    print(f"\n4️⃣ Guardando {len(predicciones)} predicciones en JSON...")
    
    output = {
        "descripcion": "Base de conocimientos completa con condiciones de hipoteca predichas para clientes bancarios",
        "generado_el": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "total_clientes": len(predicciones),
        "clientes": predicciones
    }
    
    with open("predicciones_hipotecas.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print("   ✅ Archivo guardado: predicciones_hipotecas.json")
    
    # 5. Mostrar resumen detallado
    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("=" * 70)
    print(f"\n📊 Resumen:")
    print(f"   • Total de clientes procesados: {len(predicciones)}")
    print(f"   • Archivo generado: predicciones_hipotecas.json")
    
    if predicciones:
        print(f"\n📋 Ejemplo de predicción completa:")
        ejemplo = predicciones[0]
        cond = ejemplo['condiciones_hipoteca']
        print(f"   Nombre: {ejemplo['nombre_completo']}")
        print(f"   DNI: {ejemplo['dni']}")
        print(f"   Tipo de interés: {cond['tipo_interes']}")
        print(f"   Tipo de préstamo: {cond['tipo_prestamo']}")
        print(f"   Cuota mensual: {cond['cuota_mensual']}")
        print(f"   Total a pagar: {cond['total_a_pagar']}")
        print(f"   Estado: {cond['estado']}")
    
    print("\n🎯 Siguiente paso:")
    print("   1. Abre 'predicciones_hipotecas.json'")
    print("   2. Copia todo el contenido")
    print("   3. Pégalo en la base de conocimientos de tu agente en ElevenLabs")
    print("=" * 70)
    
    client.close()
