# 🏦 CallMe - AI-Powered Voice Agent for Banking

> Sistema inteligente de asistente virtual conversacional para call centers bancarios, con agentes especializados en hipotecas y atención al cliente.

## 📋 Descripción

CallMe es una solución de IA conversacional que integra:

- **Agente Principal (Recepcionista Virtual)**: Clasifica y redirige consultas
- **Carlos (Agente de Hipotecas)**: Proporciona condiciones personalizadas usando ML predictivo
- **Ana (Atención al Cliente)**: Resuelve dudas generales y preguntas frecuentes

**Tecnologías clave:**

- Frontend: React + Vite + TailwindCSS
- Backend: Flask + Python
- IA Conversacional: ElevenLabs
- ML: XGBoost para predicción de tipos de interés
- Base de Datos: MongoDB

---

## 🚀 Quick Start

### Prerrequisitos

- **Node.js** (v18+) y **npm**
- **Python** (v3.9+)
- **MongoDB** (cuenta Atlas o local)
- **Cuenta ElevenLabs** (con API key)

### 📦 Instalación

1. Clona el repositorio

```bash
git clone https://github.com/Javirios03/Accenture_Mavericks.git
cd Accenture_Mavericks
```

2. Configura las variables de entorno

Crea un archivo `.env` en el directorio raíz con las siguientes variables:

```
ELEVENLABS_AGENT_ID=your_agent_id_here
ELEVENLABS_API_KEY=your_api_key_here
```

Obtén tu API key desde tu cuenta de ElevenLabs, para el agente específico (o contáctanos para obtener acceso a nuestro agente, temporalmente).

3. Instala dependencias:

**Python Backend:**

```bash
pip install -r requirements.txt
```

**Node.js Frontend:**

```bash
cd accenture_react
npm install
```

## Configuración de la Base de Datos

### Paso 1: Crear la base de datos con usuarios sintéticos

Utiliza el script `crea_bbdd.py` para generar una base de datos MongoDB con usuarios sintéticos.

```bash
python crea_bbdd.py
```

Esto creará una base de datos llamada `banco` con una colección `clientes`, con 20 clientes ficticios.

### Paso 2: Entrenar el modelo de ML

Ejecuta el script `train_Modelo_hipotecas.py` para entrenar el modelo de predicción de tipos de interés hipotecarios.

```bash
python train_Modelo_hipotecas.py
```

Esto entrenatrá un modelo XGBoost que predice tipos de interés basándose en:

- Valor de la vivienda
- Financiación solicitada
- Ingresos mensuales
- Credit Score
- Otros factores relevantes

### Paso 3: Generar predicciones para la base de conocimientos

Ejecuta el script `generar_predicciones.py` para generar predicciones de tipos de interés para cada cliente en la base de datos.

```bash
python generar_predicciones.py
```

Esto genera un archivo `predicciones_hipotecas.json` con las condiciones de hipoteca para cada cliente.

## 🏃‍♂️ Ejecutar la Demo

### Terminal 1: Iniciar el Backend Flask

```bash
python backend_agent.py
```

Este permite la obtención de _signed_url_ para los audios generados por los agentes de ElevenLabs.

### Terminal 2: Iniciar el Frontend React

```bash
cd accenture_react
npm run dev
```

Abre tu navegador en `http://localhost:5173` para interactuar con CallMe.

## 📚 Uso de la Demo

1. Abre el navegador en `http://localhost:5173`.
2. Haz clic en "Ver demo" para iniciar una conversación con el agente principal.
3. Permite el acceso al micrófono para enviar consultas de voz.
4. Habla con el asistente:
   - Para consultar sobre hipotecas, menciona cualquier consulta relacionada con hipotecas.
   - El agente te pedirá tu DNI para verificación
   - Luego, se procederá a la verificación, mediante una pregunta personal
     - Por ahora, es necesario incluir en la base de conocimientos del subagente de hipotecas un archivo de texto con los datos del cliente (DNI, nombre, pregunta de verificación y respuesta), si bien en futuras versiones se automatizará este proceso mediante conexión a la base de datos.
5. El agente de hipotecas (Carlos) te proporcionará condiciones personalizadas basadas en tu perfil.

## 🛠️ Personalización

Para personalizar los agentes, es necesario modificar el flujo de trabajo en la propia web de ElevenLabs, ajustando los prompts y comportamientos según las necesidades específicas.
Consulta la documentación de ElevenLabs para más detalles: [ElevenLabs Documentation](https://docs.elevenlabs.io/)

## Estructura del Proyecto

```
Accenture_Mavericks/
├── accenture_react/          # Frontend React
├── backend_agent.py          # Backend Flask para manejo de agentes
├── crea_bbdd.py              # Script para crear base de datos MongoDB con usuarios sintéticos
├── train_Modelo_hipotecas.py # Script para entrenar el modelo de ML
├── generar_predicciones.py   # Script para generar predicciones de hipotecas
├── requirements.txt          # Dependencias de Python
├── README.md                 # Documentación del proyecto
└── .env.example.txt          # Ejemplo de archivo de variables de entorno
```

## Autores

- Francisco Javier Ríos - [GitHub](https://github.com/Javirios03)
- Gabriel Lazovsky - [GitHub](https://github.com/gabriellazovsky)
- Pablo González - [GitHub](https://github.com/PGM15)
- Javier Mendoza - [GitHub](https://github.com/JavierMendozaGuerrero)

## Licencia

Este proyecto está bajo la Licencia Apache 2.0. Consulta el archivo LICENSE para más detalles.

## Agradecimientos

Agradecemos a Accenture por la oportunidad de participar en el Hackathon Mavericks 2025 y su apoyo durante el desarrollo de este proyecto.
