#!/bin/bash

# ============================================
# Script de Inicio Rápido para n8n
# Accenture Mavericks - Proyecto Bancario
# ============================================

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "============================================"
echo "  n8n Quick Start - Accenture Mavericks"
echo "============================================"
echo -e "${NC}"

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no está instalado${NC}"
    echo "Por favor, instala Docker Desktop desde: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose no está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✔ Docker y Docker Compose detectados${NC}\n"

# Navegar al directorio n8n
cd "$(dirname "$0")"

# Verificar si existe .env
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Archivo .env no encontrado${NC}"
    echo "Creando .env desde .env.example..."
    cp .env.example .env
    echo -e "${GREEN}✔ Archivo .env creado${NC}"
    echo -e "${YELLOW}⚠️  IMPORTANTE: Edita .env y cambia las contraseñas por defecto${NC}\n"
else
    echo -e "${GREEN}✔ Archivo .env encontrado${NC}\n"
fi

# Crear directorios necesarios
mkdir -p workflows backup
echo -e "${GREEN}✔ Directorios creados${NC}\n"

# Iniciar servicios
echo -e "${BLUE}🚀 Iniciando servicios...${NC}"
docker-compose up -d

echo ""
echo -e "${YELLOW}Esperando a que los servicios estén listos...${NC}"
sleep 10

# Verificar estado
echo ""
echo -e "${BLUE}Estado de los servicios:${NC}"
docker-compose ps

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  ✅ n8n está listo para usar${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo -e "${BLUE}Accede a n8n en:${NC} http://localhost:5678"
echo ""
echo -e "${YELLOW}Credenciales por defecto:${NC}"
echo "  Usuario: admin"
echo "  Contraseña: changeme"
echo ""
echo -e "${RED}⚠️  IMPORTANTE: Cambia las credenciales en el archivo .env${NC}"
echo ""
echo -e "${BLUE}Comandos útiles:${NC}"
echo "  Ver logs:      docker-compose logs -f n8n"
echo "  Detener:       docker-compose down"
echo "  Reiniciar:     docker-compose restart"
echo ""
echo -e "${BLUE}Siguiente paso:${NC}"
echo "  1. Abre http://localhost:5678 en tu navegador"
echo "  2. Inicia sesión con las credenciales"
echo "  3. Importa el workflow de ejemplo desde workflows/ejemplo_banco.json"
echo ""
echo -e "${GREEN}🚀 ¡Listo para automatizar!${NC}"
echo ""
