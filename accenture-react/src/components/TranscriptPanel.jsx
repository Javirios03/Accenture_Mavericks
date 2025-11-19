import { useEffect, useRef } from "react";

export default function TranscriptPanel({ messages }) {
  const scrollRef = useRef(null);

  useEffect(() => {
    // Auto-scroll al último mensaje
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="w-full bg-gray-900/50 rounded-xl border border-purple-500/30 p-4 backdrop-blur-sm">
      <h4 className="text-purple-300 font-semibold mb-3 flex items-center gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-5 w-5"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
            clipRule="evenodd"
          />
        </svg>
        Transcripción en tiempo real
      </h4>

      <div
        ref={scrollRef}
        className="h-64 overflow-y-auto space-y-3 pr-2 scrollbar-thin scrollbar-thumb-purple-600 scrollbar-track-gray-800"
      >
        {messages.length === 0 ? (
          <p className="text-gray-500 italic text-center mt-8">
            Esperando conversación...
          </p>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={idx}
              className={`p-3 rounded-lg ${
                msg.role === "user"
                  ? "bg-blue-900/30 border-l-4 border-blue-500"
                  : "bg-purple-900/30 border-l-4 border-purple-500"
              }`}
            >
              <div className="text-xs text-gray-400 mb-1 font-medium">
                {msg.role === "user" ? "👤 Usuario" : "🤖 Asistente"}
              </div>
              <div className="text-sm text-gray-200">{msg.content}</div>
              <div className="text-xs text-gray-500 mt-1">
                {new Date(msg.timestamp).toLocaleTimeString("es-ES")}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
