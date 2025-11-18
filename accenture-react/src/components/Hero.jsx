export default function Hero({ openModal }) {
return (
<section className="min-h-[90vh] flex items-center justify-center text-center px-6 bg-gradient-to-br from-purple-900 via-black to-black animate-fadeIn">
<div className="max-w-4xl">
<h2 className="text-6xl font-extrabold text-purple-300 mb-6 drop-shadow-xl">
Agentes de IA para Call Centers
</h2>


<p className="text-xl text-gray-300 mb-8 leading-relaxed">
Soluciones corporativas con IA, analítica avanzada y respuestas en tiempo real.
</p>


<button
onClick={openModal}
className="px-10 py-4 bg-purple-600 hover:bg-purple-700 text-lg rounded-xl shadow-xl hover:shadow-purple-500/50 hover:scale-105 transition-all duration-300"
>
Ver demo
</button>
</div>
</section>
);
}