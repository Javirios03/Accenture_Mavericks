import { createContext, useState } from "react";


export const UIContext = createContext();


export function UIProvider({ children }) {
const [modalOpen, setModalOpen] = useState(false);


return (
<UIContext.Provider value={{ modalOpen, setModalOpen }}>
{children}
</UIContext.Provider>
);
}