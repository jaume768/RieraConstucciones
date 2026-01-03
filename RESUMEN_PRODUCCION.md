# Resumen de Configuración para Producción

## ✅ Archivos Actualizados

### 1. **Dominio Configurado**
- Dominio: **rieraconstruccions.com**
- Subdominios: **www.rieraconstruccions.com**, **admin.rieraconstruccions.com**

### 2. **Archivos Modificados**

#### `src/constructora/settings.py`
- ✅ ALLOWED_HOSTS actualizado con el nuevo dominio
- ✅ SITE_URL: `https://rieraconstruccions.com`
- ✅ Emails actualizados a `rieraconstruccions@gmail.com`

#### `nginx/default.conf`
- ✅ Server names actualizados al nuevo dominio
- ✅ Configuración HTTP (puerto 80)

#### `nginx/default-ssl.conf` (Nuevo)
- ✅ Configuración HTTPS con SSL/TLS
- ✅ Redirección HTTP → HTTPS
- ✅ Certificados Let's Encrypt

#### `.env.example`
- ✅ Configuración de producción
- ✅ DEBUG=False
- ✅ Dominio y subdominios configurados
- ✅ Email SMTP de Gmail

#### `docker-compose.prod.yml` (Nuevo)
- ✅ Configuración optimizada para producción
- ✅ Gunicorn con múltiples workers
- ✅ Certbot para SSL
- ✅ Restart policies configuradas

### 3. **Templates Actualizados**
- ✅ `templates/base.html` - Footer con nuevos datos de contacto
- ✅ `templates/core/home.html` - Teléfono, email y dirección actualizados
- ✅ `templates/core/contact.html` - Información de contacto actualizada

---

## 📋 Datos de Contacto Actualizados

| Campo | Valor |
|-------|-------|
| **Teléfono** | +34 689 890 246 |
| **Email** | rieraconstruccions@gmail.com |
| **Dirección** | Poligono 6 Parcela 154 - Ctra. Manacor/Son Carrió 07500 - Manacor |
| **Dominio** | rieraconstruccions.com |

---

## 🚀 Archivos de Despliegue Creados

### 1. **DEPLOY_AWS.md**
Guía completa paso a paso para desplegar en AWS EC2:
- ✅ Crear instancia EC2
- ✅ Configurar seguridad y firewall
- ✅ Instalar Docker y dependencias
- ✅ Configurar dominio DNS
- ✅ Configurar HTTPS con Let's Encrypt
- ✅ Comandos de mantenimiento
- ✅ Solución de problemas
- ✅ Estimación de costos

### 2. **deploy.sh**
Script automatizado de despliegue que:
- ✅ Descarga últimos cambios del repositorio
- ✅ Construye imágenes Docker
- ✅ Ejecuta migraciones
- ✅ Recolecta archivos estáticos
- ✅ Limpia caché
- ✅ Verifica estado

---

## 🔧 Pasos para Desplegar

### Opción 1: Despliegue Manual (Siguiendo la guía)
```bash
# Leer la guía completa
cat DEPLOY_AWS.md
```

### Opción 2: Despliegue Rápido (Con script)
```bash
# En el servidor AWS después de clonar el proyecto
chmod +x deploy.sh
./deploy.sh
```

---

## ⚙️ Configuración Requerida Antes del Despliegue

### 1. **Archivo .env**
Copiar y configurar:
```bash
cp .env.example .env
nano .env
```

Variables críticas a configurar:
- `SECRET_KEY` - Generar una clave segura única
- `DEBUG=False` - Importante para producción
- `DB_PASSWORD` - Password seguro para PostgreSQL
- `EMAIL_HOST_PASSWORD` - App password de Gmail

### 2. **DNS del Dominio**
Configurar en el panel del proveedor:
```
Tipo A: @ → IP_DE_TU_EC2
Tipo A: www → IP_DE_TU_EC2
Tipo A: admin → IP_DE_TU_EC2
```

### 3. **Gmail App Password**
1. Activar verificación en 2 pasos en Gmail
2. Generar App Password en: https://myaccount.google.com/apppasswords
3. Usar ese password en `EMAIL_HOST_PASSWORD`

---

## 🔐 Seguridad Configurada

### En Django
- ✅ DEBUG=False en producción
- ✅ SECRET_KEY segura
- ✅ ALLOWED_HOSTS restrictivo
- ✅ HTTPS habilitado
- ✅ Security headers en Nginx

### En AWS
- ✅ Security group con puertos específicos
- ✅ SSH solo desde IP conocida
- ✅ Firewall UFW configurado
- ✅ SSL/TLS con Let's Encrypt

---

## 📊 Monitoreo

### Ver logs
```bash
# Todos los servicios
docker-compose -f docker-compose.prod.yml logs -f

# Solo Django
docker-compose -f docker-compose.prod.yml logs -f web

# Solo errores
docker-compose -f docker-compose.prod.yml logs -f | grep -i error
```

### Estado de contenedores
```bash
docker-compose -f docker-compose.prod.yml ps
docker stats
```

---

## 🔄 Comandos Útiles Post-Despliegue

### Actualizar código
```bash
cd ~/apps/RieraConstrucciones
./deploy.sh
```

### Crear superusuario
```bash
docker-compose -f docker-compose.prod.yml exec web python src/manage.py createsuperuser
```

### Backup de base de datos
```bash
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres constructora_db > backup.sql
```

### Reiniciar servicios
```bash
docker-compose -f docker-compose.prod.yml restart
```

### Limpiar caché
```bash
docker-compose -f docker-compose.prod.yml exec web python src/manage.py shell -c "from django.core.cache import cache; cache.clear()"
```

---

## 🌐 URLs en Producción

Una vez desplegado, estas serán las URLs:

- **Sitio principal**: https://rieraconstruccions.com
- **Con www**: https://www.rieraconstruccions.com
- **Admin Django**: https://rieraconstruccions.com/django-admin/
- **Backoffice**: https://admin.rieraconstruccions.com/backoffice/
- **Servicios**: https://rieraconstruccions.com/servicios/
- **Blog**: https://rieraconstruccions.com/blog/
- **Contacto**: https://rieraconstruccions.com/contacto/
- **Sitemap**: https://rieraconstruccions.com/sitemap.xml
- **Robots**: https://rieraconstruccions.com/robots.txt

---

## 💰 Costos Estimados (AWS)

### Free Tier (12 meses)
- EC2 t2.micro: **Gratis**
- 30 GB almacenamiento: **Gratis**
- Total: **$0/mes**

### Producción Básica
- EC2 t3.small: **~$15/mes**
- 30 GB almacenamiento: **~$3/mes**
- Total: **~$18/mes**

### Producción Óptima
- EC2 t3.medium: **~$30/mes**
- 50 GB almacenamiento: **~$5/mes**
- Total: **~$35/mes**

---

## ✅ Checklist Pre-Despliegue

- [ ] Cuenta AWS creada y verificada
- [ ] Dominio rieraconstruccions.com registrado
- [ ] Instancia EC2 creada y corriendo
- [ ] DNS configurado apuntando a la IP de EC2
- [ ] Archivo .env configurado con todas las variables
- [ ] SECRET_KEY única generada
- [ ] Gmail App Password generado
- [ ] Código subido al repositorio Git
- [ ] SSH key guardada de forma segura

## ✅ Checklist Post-Despliegue

- [ ] Contenedores corriendo (`docker-compose ps`)
- [ ] HTTPS funcionando correctamente
- [ ] Admin accesible
- [ ] Formulario de contacto enviando emails
- [ ] Archivos estáticos cargando
- [ ] Imágenes del media folder visibles
- [ ] Sitemap y robots.txt accesibles
- [ ] SSL con A+ en SSL Labs
- [ ] Backups configurados
- [ ] Monitoreo activo

---

## 🆘 Soporte

Si encuentras problemas:

1. Revisa los logs: `docker-compose -f docker-compose.prod.yml logs -f`
2. Consulta la sección de "Solución de Problemas" en `DEPLOY_AWS.md`
3. Verifica el estado de los contenedores
4. Revisa que el archivo .env esté correctamente configurado

---

**Proyecto preparado y listo para despliegue en producción** ✨

Última actualización: Enero 2026
