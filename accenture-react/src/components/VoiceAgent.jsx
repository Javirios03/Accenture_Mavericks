import { useConversation } from "@elevenlabs/react";
import { useState } from "react";

export default function VoiceAgent({ onClose }) {
  const [status, setStatus] = useState("disconnected");
  const [error, setError] = useState("");

  const conversation = useConversation({
    onConnect: () => {
      console.log("Conectado al agente");
      setStatus("connected");
    },
    onDisconnect: () => {
      console.log("Desconectado del agente");
      setStatus("disconnected");
    },
    onError: (error) => {
      console.error("Error:", error);
      setError(error.message);
    },
    onMessage: (message) => {
      console.log("Mensaje recibido:", message);
    },
  });

  const startConversation = async () => {
    try {
      // Solicitar permisos de micrófono primero
      await navigator.mediaDevices.getUserMedia({ audio: true });

      // Iniciar conversación con el agente
      const conversationId = await conversation.startSession({
        agentId: import.meta.env.VITE_ELEVENLABS_AGENT_ID,
        connectionType: "webrtc", // o 'websocket'
      });

      console.log("Conversación iniciada:", conversationId);
    } catch (err) {
      setError("Error al iniciar conversación: " + err.message);
    }
  };

  const endConversation = async () => {
    await conversation.endSession();
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-6">
      <div className="bg-black p-10 rounded-2xl border border-purple-600 max-w-lg text-center">
        <h3 className="text-3xl mb-4 text-purple-300 font-bold">
          Asistente Virtual
        </h3>

        {error && (
          <div className="mb-4 p-3 bg-red-900/30 border border-red-600 rounded text-red-300">
            {error}
          </div>
        )}

        <div className="mb-6">
          {status === "disconnected" ? (
            <button
              onClick={startConversation}
              className="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-xl shadow-lg"
            >
              Iniciar Conversación
            </button>
          ) : (
            <div>
              <p className="text-green-400 mb-4">🎤 Conversación activa</p>
              <button
                onClick={endConversation}
                className="px-6 py-3 bg-red-600 hover:bg-red-700 rounded-xl shadow-lg"
              >
                Finalizar
              </button>
            </div>
          )}
        </div>

        <button
          onClick={onClose}
          className="px-6 py-3 bg-gray-600 hover:bg-gray-700 rounded-xl shadow-lg"
        >
          Cerrar
        </button>
      </div>
    </div>
  );
}
