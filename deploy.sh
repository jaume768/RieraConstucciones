#!/bin/bash

# Script de despliegue para Constructora Riera
# Uso: ./deploy.sh

set -e

echo "🚀 Iniciando despliegue de Constructora Riera..."

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.prod.yml" ]; then
    echo -e "${RED}❌ Error: docker-compose.prod.yml no encontrado${NC}"
    echo "Por favor ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Verificar que existe el archivo .env
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Error: Archivo .env no encontrado${NC}"
    echo "Por favor copia .env.example a .env y configúralo:"
    echo "  cp .env.example .env"
    echo "  nano .env"
    exit 1
fi

# Descargar últimos cambios
echo -e "${YELLOW}📥 Descargando últimos cambios...${NC}"
git pull origin main || echo -e "${YELLOW}⚠️  No se pudo hacer git pull (puede que no estés en un repo)${NC}"

# Detener contenedores actuales
echo -e "${YELLOW}🛑 Deteniendo contenedores actuales...${NC}"
docker-compose -f docker-compose.prod.yml down

# Construir imágenes
echo -e "${YELLOW}🔨 Construyendo imágenes Docker...${NC}"
docker-compose -f docker-compose.prod.yml build

# Levantar contenedores
echo -e "${YELLOW}🚀 Levantando contenedores...${NC}"
docker-compose -f docker-compose.prod.yml up -d

# Esperar a que la base de datos esté lista
echo -e "${YELLOW}⏳ Esperando a que la base de datos esté lista...${NC}"
sleep 10

# Ejecutar migraciones
echo -e "${YELLOW}🔄 Ejecutando migraciones de base de datos...${NC}"
docker-compose -f docker-compose.prod.yml exec -T web python src/manage.py migrate --noinput

# Recolectar archivos estáticos
echo -e "${YELLOW}📦 Recolectando archivos estáticos...${NC}"
docker-compose -f docker-compose.prod.yml exec -T web python src/manage.py collectstatic --noinput

# Limpiar caché
echo -e "${YELLOW}🧹 Limpiando caché...${NC}"
docker-compose -f docker-compose.prod.yml exec -T web python src/manage.py shell -c "from django.core.cache import cache; cache.clear(); print('Caché limpiada')" || true

# Verificar estado de contenedores
echo -e "${YELLOW}🔍 Verificando estado de contenedores...${NC}"
docker-compose -f docker-compose.prod.yml ps

# Verificar logs recientes
echo -e "${YELLOW}📋 Últimos logs de Django:${NC}"
docker-compose -f docker-compose.prod.yml logs --tail=20 web

echo -e "${GREEN}✅ ¡Despliegue completado exitosamente!${NC}"
echo ""
echo "🌐 URLs disponibles:"
echo "   - https://rieraconstruccions.com"
echo "   - https://rieraconstruccions.com/django-admin/"
echo "   - https://admin.rieraconstruccions.com/backoffice/"
echo ""
echo "📊 Ver logs en tiempo real:"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "🔄 Reiniciar servicios:"
echo "   docker-compose -f docker-compose.prod.yml restart"
