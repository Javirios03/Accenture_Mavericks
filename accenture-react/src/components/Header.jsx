import { useState } from "react";

export default function Header() {
  const [open, setOpen] = useState(false);

  return (
    <header className="fixed top-0 w-full bg-black/80 backdrop-blur-lg z-50">
      <div className="max-w-7xl mx-auto flex justify-between items-center px-6 py-4">
        <h1 className="text-2xl font-bold text-purple-400">Accenture AI</h1>

        <nav className="hidden md:flex gap-8 text-lg">
          <a href="#contacto" className="hover:text-purple-300 transition">Contacto</a>
        </nav>

        <button className="md:hidden text-3xl" onClick={() => setOpen(!open)}>
          ☰
        </button>
      </div>

      {open && (
        <div className="md:hidden bg-black flex flex-col gap-4 px-6 pb-4 text-lg">
          <a href="#contacto">Contacto</a>
        </div>
      )}
    </header>
  );
}
