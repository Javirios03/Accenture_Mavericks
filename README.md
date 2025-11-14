# Accenture_Mavericks

## README - Ejemplo de Conexión y Operaciones con MongoDB en Python

Este script muestra cómo conectarse a una base de datos MongoDB usando `pymongo`, insertar un documento y leer datos de la colección.

---

## 📌 Requisitos

1. Python 3 instalado.
2. Instalar la librería necesaria:
pip install pymongo

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
