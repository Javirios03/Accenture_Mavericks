# Accenture_Mavericks

## README - Ejemplo de Conexión y Operaciones con MongoDB en Python

Este script muestra cómo conectarse a una base de datos MongoDB usando `pymongo`, insertar un documento y leer datos de la colección.

---

## 📌 Requisitos

1. Python 3 instalado.
2. Instalar la librerías necesarias:

   ```bash
   pip install -r requirements.txt
   ```

3. Tener acceso al clúster de MongoDB Atlas con la URI correspondiente.

---

## 📂 Descripción del Código

El script realiza las siguientes operaciones:

### 1. Conexión a MongoDB

Se usa `MongoClient` con la URI proporcionada:

```python
client = MongoClient(uri)
```

2. Selección de base de datos y colección
   db = client["banco"]
   clientes = db["clientes"]

3. Insertar un cliente nuevo

resultado = clientes.insert_one(nuevo_cliente)
print("Cliente insertado con ID:", resultado.inserted_id)

5. Leer todos los clientes

for c in clientes.find():
print(c)

▶️ Cómo ejecutar

python ejemplodb.py

### 2. Ejecución del Frontend

Primero, asegúrate de tener Node.js y npm instalados (en caso contrario, descárgalos desde https://nodejs.org/). Luego, navega al directorio del frontend:
cd frontend

Instala las dependencias necesarias:
npm install

Inicia la aplicación React:
npm run dev

La aplicación debería abrirse automáticamente en tu navegador. Si no es así, abre http://localhost:5173 en tu navegador.
