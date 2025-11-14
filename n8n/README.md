# 🔄 n8n Orchestrator - Accenture Mavericks

Este directorio contiene la configuración de **n8n** como orquestador para automatizar y gestionar workflows del proyecto de asistente bancario.

## 📋 ¿Qué es n8n?

n8n es una herramienta de automatización de workflows de código abierto que permite:
- Crear flujos de trabajo visuales sin código (low-code)
- Integrar múltiples servicios y APIs
- Orquestar procesos complejos
- Ejecutar automaciones basadas en eventos o programaciones

## 🚀 Inicio Rápido

### Requisitos Previos
- Docker y Docker Compose instalados
- Puerto 5678 disponible (interfaz web de n8n)
- Puerto 27017 disponible (MongoDB)

### 1. Configuración Inicial

```bash
# Navegar al directorio n8n
cd n8n/

# Copiar el archivo de variables de entorno
cp .env.example .env

# Editar las credenciales (IMPORTANTE: cambiar las contraseñas)
nano .env  # o usar tu editor preferido
```

### 2. Levantar los Servicios

```bash
# Iniciar n8n, PostgreSQL y MongoDB
docker-compose up -d

# Ver los logs
docker-compose logs -f n8n
```

### 3. Acceder a n8n

Abre tu navegador y ve a: **http://localhost:5678**

- **Usuario por defecto:** admin
- **Contraseña por defecto:** changeme (¡cámbiala en el archivo .env!)

## 📁 Estructura de Carpetas

```
n8n/
├── docker-compose.yml      # Configuración de servicios Docker
├── .env.example            # Variables de entorno de ejemplo
├── .env                    # Variables de entorno (NO subir a Git)
├── README.md               # Esta documentación
├── workflows/              # Workflows de n8n exportados
│   └── ejemplo_banco.json  # Workflow de ejemplo
└── backup/                 # Backups automáticos
```

## 🔧 Servicios Incluidos

### 1. **n8n** (Puerto 5678)
- Interfaz web de automatización
- Ejecución de workflows
- API REST para integraciones

### 2. **PostgreSQL** (Interno)
- Base de datos para n8n
- Almacena workflows, credenciales y ejecuciones

### 3. **MongoDB** (Puerto 27017)
- Base de datos de tu aplicación bancaria
- Conectada a n8n para operaciones CRUD

## 💡 Casos de Uso para el Proyecto Bancario

### 1. **Procesamiento de Consultas de Clientes**
```
Webhook → Clasificar Departamento → Consultar MongoDB → Enviar Respuesta
```

### 2. **Automatización de Llamadas**
```
Audio → Transcripción (Whisper API) → Análisis NLP → Enrutamiento
```

### 3. **Sincronización de Datos**
```
Scheduler → Consultar API → Actualizar MongoDB → Notificar Equipo
```

### 4. **Análisis y Reportes**
```
Cron Diario → Extraer Métricas MongoDB → Generar Reporte → Enviar Email
```

## 🎯 Primeros Pasos - Workflow de Ejemplo

### Importar el Workflow de Ejemplo

1. Accede a n8n (http://localhost:5678)
2. Ve a **Workflows** → **Import from File**
3. Selecciona `workflows/ejemplo_banco.json`
4. El workflow incluye:
   - Webhook para recibir consultas
   - Nodo HTTP para llamar a tu API
   - Nodo MongoDB para consultas directas
   - Lógica de enrutamiento por departamento

### Crear tu Primer Workflow

1. Click en **Create New Workflow**
2. Arrastra un nodo **Webhook**
3. Configura la URL del webhook
4. Añade nodos según tu flujo
5. Prueba con el botón **Execute Workflow**

## 🔗 Integración con tu Aplicación Actual

### Opción 1: Llamar a n8n desde tu API

```python
import requests

# En tu app.py o main.py
def procesar_con_n8n(datos):
    webhook_url = "http://localhost:5678/webhook/consulta-bancaria"
    response = requests.post(webhook_url, json=datos)
    return response.json()
```

### Opción 2: n8n llama a tu API existente

```
En n8n:
Webhook → HTTP Request (http://localhost:8000/ask) → Procesar Respuesta
```

### Opción 3: Acceso directo a MongoDB

```
En n8n:
Trigger → MongoDB (consulta directa) → Lógica de Negocio → Respuesta
```

## 📊 Monitorización

### Ver Logs
```bash
# Logs de n8n
docker-compose logs -f n8n

# Logs de MongoDB
docker-compose logs -f mongo

# Logs de todos los servicios
docker-compose logs -f
```

### Estado de los Servicios
```bash
docker-compose ps
```

### Estadísticas de Ejecución
- Dentro de n8n: **Executions** → Ver historial completo

## 🛠️ Comandos Útiles

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Reiniciar n8n
docker-compose restart n8n

# Backup de workflows
docker-compose exec n8n n8n export:workflow --all --output=/home/node/backup/

# Limpiar todo (CUIDADO: borra datos)
docker-compose down -v
```

## 🔐 Seguridad

### Variables de Entorno Importantes

**En producción, SIEMPRE cambiar:**
- `N8N_USER` y `N8N_PASSWORD`
- `POSTGRES_PASSWORD`
- `MONGO_URI` (si usas MongoDB Atlas)

### Archivo .gitignore

Asegúrate de que `.env` está en el `.gitignore` para no exponer credenciales.

## 🧪 Testing y Desarrollo

### Probar Webhooks Localmente

```bash
curl -X POST http://localhost:5678/webhook-test/consulta \
  -H "Content-Type: application/json" \
  -d '{"pregunta": "¿Cuál es mi saldo?", "usuario_id": "123"}'
```

### Conectar con tu App.py

```python
# Ejemplo de integración en app.py
import requests

def consulta_via_n8n(texto_usuario):
    try:
        response = requests.post(
            "http://localhost:5678/webhook/banco",
            json={"texto": texto_usuario},
            timeout=30
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}
```

## 📚 Recursos Adicionales

- [Documentación Oficial de n8n](https://docs.n8n.io/)
- [n8n Community](https://community.n8n.io/)
- [Library de Workflows](https://n8n.io/workflows/)
- [MongoDB Node Documentation](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.mongodb/)

## 🤝 Contribuir

Para añadir nuevos workflows:
1. Créalos en la interfaz de n8n
2. Expórtalos: **Workflow Menu** → **Download**
3. Guárdalos en `workflows/` con un nombre descriptivo
4. Documenta su propósito en este README

## ❓ Troubleshooting

### n8n no arranca
```bash
# Verificar puertos en uso
sudo netstat -tulpn | grep 5678

# Ver logs detallados
docker-compose logs n8n
```

### MongoDB no conecta
```bash
# Verificar que MongoDB está corriendo
docker-compose ps mongo

# Probar conexión
docker-compose exec mongo mongosh --eval "db.adminCommand('ping')"
```

### Error de permisos
```bash
# Dar permisos a las carpetas
sudo chown -R 1000:1000 ./workflows ./backup
```

---

**¡Listo para empezar a automatizar! 🚀**
