// VoiceAgent.jsx
import { useConversation } from "@elevenlabs/react";
import { useState, useEffect } from "react";
import AudioOrb from "./AudioOrb";
import TranscriptPanel from "./TranscriptPanel";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:5000";

export default function VoiceAgent({ onClose }) {
  const [status, setStatus] = useState("disconnected");
  const [error, setError] = useState("");
  const [messages, setMessages] = useState([]);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [audioVolume, setAudioVolume] = useState(0);

  const conversation = useConversation({
    onConnect: () => {
      console.log("Conectado al agente");
      setStatus("connected");
      setError("");
    },
    onDisconnect: () => {
      console.log("Desconectado del agente");
      setStatus("disconnected");
      setIsSpeaking(false);
    },
    onError: (error) => {
      console.error("Error:", error);
      setError(error.message);
      setStatus("error");
    },
    onMessage: (message) => {
      console.log("Mensaje recibido:", message);
      setMessages((prev) => [
        ...prev,
        {
          role: message.source || "agent",
          content: message.message || message.text || "",
          timestamp: Date.now(),
        },
      ]);
    },
    onModeChange: ({ mode }) => {
      setIsSpeaking(mode === "speaking");
    },
  });

  useEffect(() => {
    let interval;
    if (isSpeaking) {
      interval = setInterval(() => {
        setAudioVolume(Math.random() * 0.8 + 0.2);
      }, 100);
    } else {
      setAudioVolume(0);
    }
    return () => clearInterval(interval);
  }, [isSpeaking]);

  const startConversation = async () => {
    try {
      setError("");
      setStatus("connecting");

      // 1. Solicitar permisos de micrófono
      await navigator.mediaDevices.getUserMedia({ audio: true });

      // 2. Obtener signed URL del backend
      console.log("Solicitando signed URL al backend...");
      const response = await fetch(`${BACKEND_URL}/api/get-signed-url`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Error al obtener signed URL");
      }

      const { signed_url } = await response.json();
      console.log("Signed URL obtenida exitosamente");

      // 3. Iniciar conversación con la signed URL
      const conversationId = await conversation.startSession({
        signedUrl: signed_url, // ← Cambio crítico: usar signedUrl en lugar de agentId
      });

      console.log("Conversación iniciada:", conversationId);
      setMessages([
        {
          role: "system",
          content: "Conversación iniciada. ¡Habla con el asistente!",
          timestamp: Date.now(),
        },
      ]);
    } catch (err) {
      console.error("Error completo:", err);
      setError("Error al iniciar conversación: " + err.message);
      setStatus("error");
    }
  };

  const endConversation = async () => {
    await conversation.endSession();
    setMessages([]);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div className="bg-gradient-to-br from-gray-900 via-black to-purple-900/30 p-8 rounded-3xl border border-purple-600/50 max-w-4xl w-full shadow-2xl">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-4xl text-purple-300 font-bold flex items-center gap-3">
            <span className="animate-pulse">🎙️</span>
            Asistente Virtual
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors p-2 hover:bg-gray-800 rounded-lg"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-900/40 border border-red-600 rounded-xl text-red-300 flex items-start gap-3">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6 flex-shrink-0"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <div>
              <p className="font-semibold">Error</p>
              <p className="text-sm">{error}</p>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Panel izquierdo - Orbe y controles */}
          <div className="flex flex-col items-center justify-center space-y-6">
            <div className="relative">
              <AudioOrb isSpeaking={isSpeaking} volume={audioVolume} />
              <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2">
                {status === "connected" && (
                  <span
                    className={`px-4 py-2 rounded-full text-sm font-medium ${
                      isSpeaking
                        ? "bg-green-600/80 text-white animate-pulse"
                        : "bg-blue-600/80 text-white"
                    }`}
                  >
                    {isSpeaking ? "🎤 Escuchando..." : "💬 Conectado"}
                  </span>
                )}
                {status === "connecting" && (
                  <span className="px-4 py-2 rounded-full text-sm font-medium bg-yellow-600/80 text-white">
                    🔄 Conectando...
                  </span>
                )}
              </div>
            </div>

            {/* Control Buttons */}
            <div className="flex gap-4">
              {status === "disconnected" || status === "error" ? (
                <button
                  onClick={startConversation}
                  className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-xl shadow-lg font-semibold text-lg transition-all transform hover:scale-105 active:scale-95"
                >
                  ▶️ Iniciar Conversación
                </button>
              ) : (
                <button
                  onClick={endConversation}
                  className="px-8 py-4 bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 rounded-xl shadow-lg font-semibold text-lg transition-all transform hover:scale-105 active:scale-95"
                  disabled={status === "connecting"}
                >
                  ⏹️ Finalizar
                </button>
              )}
            </div>

            {/* Connection Info */}
            <div className="text-center text-sm text-gray-400 space-y-1">
              <p>
                Estado:{" "}
                <span className="text-purple-400 font-medium">{status}</span>
              </p>
              {status === "connected" && (
                <p className="text-xs">
                  Presiona el botón del micrófono y habla
                </p>
              )}
            </div>
          </div>

          {/* Panel derecho - Transcripción */}
          <div className="flex flex-col">
            <TranscriptPanel messages={messages} />

            {status === "connected" && (
              <div className="mt-4 grid grid-cols-2 gap-3">
                <div className="bg-gray-800/50 rounded-lg p-3 border border-gray-700">
                  <p className="text-xs text-gray-400">Mensajes</p>
                  <p className="text-2xl font-bold text-purple-400">
                    {messages.length}
                  </p>
                </div>
                <div className="bg-gray-800/50 rounded-lg p-3 border border-gray-700">
                  <p className="text-xs text-gray-400">Volumen</p>
                  <div className="flex items-center gap-2 mt-1">
                    <div className="flex-1 bg-gray-700 rounded-full h-2 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-purple-500 to-blue-500 h-full transition-all duration-100"
                        style={{ width: `${audioVolume * 100}%` }}
                      />
                    </div>
                    <span className="text-xs text-purple-400">
                      {Math.round(audioVolume * 100)}%
                    </span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
