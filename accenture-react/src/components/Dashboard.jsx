export default function Dashboard() {
return (
<div className="p-10 text-white bg-black min-h-screen animate-fadeIn">
<h1 className="text-4xl font-bold mb-8 text-purple-300">Panel del Call Center IA</h1>


<div className="grid md:grid-cols-3 gap-6">
<div className="p-6 bg-zinc-900 rounded-xl border border-purple-800 shadow-lg">
<h3 className="text-xl text-purple-300 mb-2">Llamadas activas</h3>
<p className="text-4xl font-bold">12</p>
</div>


<div className="p-6 bg-zinc-900 rounded-xl border border-purple-800 shadow-lg">
<h3 className="text-xl text-purple-300 mb-2">Tiempo medio</h3>
<p className="text-4xl font-bold">3:42</p>
</div>


<div className="p-6 bg-zinc-900 rounded-xl border border-purple-800 shadow-lg">
<h3 className="text-xl text-purple-300 mb-2">Satisfacción</h3>
<p className="text-4xl font-bold">92%</p>
</div>
</div>
</div>
);
}