export default function Modal({ close }) {
  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-6">
      <div className="bg-black p-10 rounded-2xl border border-purple-600 max-w-lg text-center">
        <h3 className="text-3xl mb-4 text-purple-300 font-bold">Demo</h3>
        <p className="text-gray-300 mb-6">Aquí iría una demo del agente de IA.</p>

        <button
          onClick={close}
          className="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-xl shadow-lg"
        >
          Cerrar
        </button>
      </div>
    </div>
  );
}
