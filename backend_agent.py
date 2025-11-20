# backend_agent.py - VERSIÓN CORREGIDA
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Permitir llamadas desde React

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
ELEVENLABS_AGENT_ID = os.getenv('ELEVENLABS_AGENT_ID')

@app.route('/api/get-signed-url', methods=['POST'])
def get_signed_url():
    """
    Genera una URL firmada para que el cliente pueda conectarse al agente
    sin necesidad de autenticación directa.
    """
    
    if not ELEVENLABS_API_KEY:
        return jsonify({'error': 'API key not configured'}), 500
    
    if not ELEVENLABS_AGENT_ID:
        return jsonify({'error': 'Agent ID not configured'}), 500
    
    try:
        # ✅ CORRECCIÓN: Usar GET con query parameters
        url = f"https://api.elevenlabs.io/v1/convai/conversation/get-signed-url?agent_id={ELEVENLABS_AGENT_ID}"
        
        headers = {
            'xi-api-key': ELEVENLABS_API_KEY
        }
        
        # ✅ CORRECCIÓN: Cambiar de POST a GET
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                'signed_url': data.get('signed_url'),
                'agent_id': ELEVENLABS_AGENT_ID
            }), 200
        else:
            print(f"❌ Error from ElevenLabs: {response.status_code} - {response.text}")
            return jsonify({
                'error': 'Failed to get signed URL',
                'status_code': response.status_code,
                'details': response.text
            }), response.status_code
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'api_key_configured': bool(ELEVENLABS_API_KEY),
        'agent_id_configured': bool(ELEVENLABS_AGENT_ID)
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("=" * 50)
    print("🚀 Backend Agent Server Starting...")
    print("=" * 50)
    print(f"📡 Port: {port}")
    print(f"🔑 API Key configured: {bool(ELEVENLABS_API_KEY)}")
    print(f"🤖 Agent ID configured: {bool(ELEVENLABS_AGENT_ID)}")
    if ELEVENLABS_API_KEY:
        print(f"🔐 API Key preview: {ELEVENLABS_API_KEY[:8]}...{ELEVENLABS_API_KEY[-4:]}")
    if ELEVENLABS_AGENT_ID:
        print(f"🆔 Agent ID preview: {ELEVENLABS_AGENT_ID[:8]}...{ELEVENLABS_AGENT_ID[-4:]}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=True)
