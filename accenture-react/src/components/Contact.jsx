export default function Contact() {
  return (
    <section id="contacto" className="py-24 px-6 max-w-4xl mx-auto">
      <h3 className="text-4xl font-bold text-purple-300 mb-12 text-center">
        Contacto
      </h3>

      <form className="grid gap-6 bg-black p-10 rounded-2xl border border-purple-700 shadow-lg">
        <input className="p-4 rounded-lg bg-black border border-gray-700" placeholder="Nombre" />
        <input type="email" className="p-4 rounded-lg bg-black border border-gray-700" placeholder="Email" />
        <textarea className="p-4 rounded-lg bg-black border border-gray-700" placeholder="Mensaje" rows="5" />

        <button className="px-6 py-4 bg-purple-600 hover:bg-purple-700 rounded-xl font-bold shadow-lg hover:scale-105 transition">
          Enviar mensaje
        </button>
      </form>
    </section>
  );
}
