import streamlit as st
import requests
import base64

API_URL_TEXT = "http://localhost:8000/ask"
API_URL_VOICE = "http://localhost:8000/ask-voice"

# --- UI ---

st.set_page_config(page_title="Asistente Bancario", layout="centered")

st.title("🏦 Asistente Inteligente – Call Center Bancario")
st.write("Haz una pregunta por **texto** o **voz** y te redirigiremos al departamento correcto.")

# --- Tabs ---
tab1, tab2 = st.tabs(["✍️ Pregunta por texto", "🎤 Pregunta por voz"])

# ------------------------------------------------------------
# TAB 1 - TEXTO
# ------------------------------------------------------------

with tab1:
    st.subheader("Consulta por texto")

    user_text = st.text_area("Escribe aquí tu pregunta:", height=150)

    if st.button("Enviar pregunta", key="send_text"):
        if not user_text.strip():
            st.warning("Por favor escribe una pregunta.")
        else:
            with st.spinner("Procesando..."):
                response = requests.post(
                    API_URL_TEXT,
                    json={"text": user_text}
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success(f"🟢 **Departamento detectado:** {data.get('department', 'Desconocido')}")
                    st.info(data.get("answer", "Sin respuesta."))
                else:
                    st.error("❌ Error en el servidor.")


# ------------------------------------------------------------
# TAB 2 - VOZ
# ------------------------------------------------------------

with tab2:
    st.subheader("Consulta por voz")

    audio_file = st.file_uploader(
        "Sube un archivo de audio (wav, mp3):",
        type=["wav", "mp3"]
    )

    if st.button("Enviar audio", key="send_audio"):
        if audio_file is None:
            st.warning("Por favor sube un archivo de audio.")
        else:
            with st.spinner("Procesando audio..."):

                audio_bytes = audio_file.read()
                encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")

                response = requests.post(
                    API_URL_VOICE,
                    json={"audio_base64": encoded_audio}
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success(f"🟢 **Departamento detectado:** {data.get('department', 'Desconocido')}")
                    st.write(f"🔊 **Transcripción:** {data.get('transcription', '')}")
                    st.info(data.get("answer", "Sin respuesta."))
                else:
                    st.error("❌ Error en el servidor.")
