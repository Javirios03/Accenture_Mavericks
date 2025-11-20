# mortgage_api.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from leerdb import obtener_clientes, entrenar_modelo, answer_mortage, FEATURES
import os

app = Flask(__name__)
CORS(app)  # Permitir llamadas desde ElevenLabs

# Variables globales
modelo = None
clientes_data = []

def inicializar_modelo():
    """Entrena el modelo al iniciar el servidor"""
    global modelo, clientes_data
    print("🔄 Cargando clientes desde MongoDB...")
    clientes_data = obtener_clientes()
    print(f"✅ {len(clientes_data)} clientes recuperados")
    
    if len(clientes_data) > 0:
        print("🔄 Entrenando modelo...")
        modelo = entrenar_modelo(clientes_data)
        print("✅ Modelo entrenado y listo")
    else:
        print("⚠️ No hay clientes suficientes para entrenar")

@app.route('/predict-mortgage', methods=['POST'])
def predict_mortgage():
    """
    Endpoint para que ElevenLabs llame y obtenga predicción
    
    Espera JSON con los datos del cliente:
    {
        "ahorro_aportado": 3000,
        "financiacion_necesaria": 150000,
        "valor_vivienda": 153000,
        "plazo_anios": 25,
        "ingresos_mensuales": 3500,
        "gastos_mensuales": 1200,
        "edad": 35,
        "antiguedad_laboral": 8,
        "credit_score": 720
    }
    """
    try:
        data = request.json
        
        if modelo is None:
            return jsonify({
                "error": "Modelo no disponible",
                "message": "El modelo no se ha podido entrenar. Verifica los datos en MongoDB."
            }), 500
        
        # Calcular campos derivados
        ltv = data.get("financiacion_necesaria", 0) / data.get("valor_vivienda", 1)
        dti = data.get("gastos_mensuales", 0) / data.get("ingresos_mensuales", 1)
        
        # Construir diccionario completo
        cliente_dict = {
            "ahorro_aportado": data.get("ahorro_aportado"),
            "financiacion_necesaria": data.get("financiacion_necesaria"),
            "valor_vivienda": data.get("valor_vivienda"),
            "ltv": round(ltv, 3),
            "plazo_anios": data.get("plazo_anios"),
            "ingresos_mensuales": data.get("ingresos_mensuales"),
            "gastos_mensuales": data.get("gastos_mensuales"),
            "dti": round(dti, 3),
            "edad": data.get("edad"),
            "antiguedad_laboral": data.get("antiguedad_laboral"),
            "credit_score": data.get("credit_score")
        }
        
        # Validar que tenemos todos los campos
        missing = [f for f in FEATURES if cliente_dict.get(f) is None]
        if missing:
            return jsonify({
                "error": "Faltan campos requeridos",
                "missing_fields": missing
            }), 400
        
        # Hacer predicción
        tipo_interes = answer_mortage(cliente_dict, modelo)
        
        return jsonify({
            "tipo_interes_predicho": tipo_interes,
            "ltv_calculado": f"{ltv:.2%}",
            "dti_calculado": f"{dti:.2%}",
            "mensaje": f"Para esta hipoteca, el tipo de interés estimado es del {tipo_interes}"
        })
        
    except Exception as e:
        print(f"❌ Error en predicción: {str(e)}")
        return jsonify({
            "error": "Error interno",
            "message": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "modelo_cargado": modelo is not None,
        "num_clientes": len(clientes_data)
    })

if __name__ == '__main__':
    # Entrenar modelo al iniciar
    inicializar_modelo()
    
    # Iniciar servidor
    port = int(os.environ.get('PORT', 5001))
    print(f"🚀 Servidor corriendo en puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
