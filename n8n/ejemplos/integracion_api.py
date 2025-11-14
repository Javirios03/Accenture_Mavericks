#!/usr/bin/env python3
"""
Ejemplo de integración entre tu API FastAPI/Flask y n8n

Este script muestra cómo puedes:
1. Enviar consultas desde tu aplicación actual a n8n
2. Recibir webhooks desde n8n para procesar resultados
3. Usar n8n como capa de orquestación intermedia
"""

import requests
import json
from typing import Dict, Any

# ============================================
# Configuración
# ============================================

N8N_BASE_URL = "http://localhost:5678"
N8N_WEBHOOK_CONSULTA = f"{N8N_BASE_URL}/webhook/consulta-bancaria"
N8N_WEBHOOK_AUDIO = f"{N8N_BASE_URL}/webhook/procesar-audio"

# ============================================
# Funciones de Integración
# ============================================

def enviar_consulta_texto_a_n8n(texto: str, usuario_id: str = None) -> Dict[str, Any]:
    """
    Envía una consulta de texto a n8n para su procesamiento
    
    Args:
        texto: La pregunta o consulta del usuario
        usuario_id: ID del usuario que hace la consulta (opcional)
    
    Returns:
        Dict con la respuesta de n8n
    """
    try:
        payload = {
            "pregunta": texto,
            "usuario_id": usuario_id,
            "timestamp": "2025-11-14T18:00:00Z"
        }
        
        response = requests.post(
            N8N_WEBHOOK_CONSULTA,
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        return {
            "error": True,
            "mensaje": f"Error al comunicarse con n8n: {str(e)}",
            "departamento": "Error"
        }


def enviar_audio_a_n8n(audio_base64: str, usuario_id: str = None) -> Dict[str, Any]:
    """
    Envía audio codificado en base64 a n8n para transcripción y procesamiento
    
    Args:
        audio_base64: Audio codificado en base64
        usuario_id: ID del usuario (opcional)
    
    Returns:
        Dict con transcripción y respuesta
    """
    try:
        payload = {
            "audio_base64": audio_base64,
            "usuario_id": usuario_id
        }
        
        response = requests.post(
            N8N_WEBHOOK_AUDIO,
            json=payload,
            timeout=60  # Más tiempo para audio
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        return {
            "error": True,
            "mensaje": f"Error al procesar audio: {str(e)}"
        }


def consultar_estado_workflow(execution_id: str) -> Dict[str, Any]:
    """
    Consulta el estado de una ejecución de workflow en n8n
    
    Args:
        execution_id: ID de la ejecución a consultar
    
    Returns:
        Dict con el estado de la ejecución
    """
    try:
        # Requiere configurar credenciales API en n8n
        url = f"{N8N_BASE_URL}/api/v1/executions/{execution_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


# ============================================
# Ejemplos de Uso
# ============================================

if __name__ == "__main__":
    print("\n" + "="*50)
    print("Ejemplos de Integración con n8n")
    print("="*50 + "\n")
    
    # Ejemplo 1: Consulta de saldo
    print("💰 Ejemplo 1: Consulta de Saldo")
    resultado = enviar_consulta_texto_a_n8n(
        texto="¿Cuál es mi saldo actual?",
        usuario_id="user_123"
    )
    print(f"Respuesta: {json.dumps(resultado, indent=2, ensure_ascii=False)}\n")
    
    # Ejemplo 2: Consulta de préstamos
    print("🏦 Ejemplo 2: Información de Préstamos")
    resultado = enviar_consulta_texto_a_n8n(
        texto="Quiero información sobre préstamos hipotecarios",
        usuario_id="user_456"
    )
    print(f"Respuesta: {json.dumps(resultado, indent=2, ensure_ascii=False)}\n")
    
    # Ejemplo 3: Consulta genérica
    print("❓ Ejemplo 3: Consulta Genérica")
    resultado = enviar_consulta_texto_a_n8n(
        texto="¿Qué horarios tienen?",
        usuario_id="user_789"
    )
    print(f"Respuesta: {json.dumps(resultado, indent=2, ensure_ascii=False)}\n")
    
    print("\n" + "="*50)
    print("✅ Ejemplos completados")
    print("="*50 + "\n")
    
    print("\n💡 Notas:")
    print("- Asegúrate de que n8n esté corriendo: docker-compose up -d")
    print("- Los webhooks deben estar activos en n8n")
    print("- Importa el workflow de ejemplo desde n8n/workflows/")
