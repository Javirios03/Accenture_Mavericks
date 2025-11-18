import { useContext } from "react";
import { UIContext } from "../context/UIContext";


export function useModal() {
const { modalOpen, setModalOpen } = useContext(UIContext);
return {
modalOpen,
open: () => setModalOpen(true),
close: () => setModalOpen(false),
};
}