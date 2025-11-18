import { useState } from "react";
import Header from "./components/Header";
import Hero from "./components/Hero";
import Contact from "./components/Contact";
import Modal from "./components/Modal";

export default function App() {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <>
      <Header />
      <Hero openModal={() => setModalOpen(true)} />
      <Contact />

      <footer className="py-10 text-center bg-black border-t border-purple-800 text-gray-400">
        © 2025 Accenture — Soluciones de IA para Call Centers
      </footer>

      {modalOpen && <Modal close={() => setModalOpen(false)} />}
    </>
  );
}
