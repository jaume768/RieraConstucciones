# Guía de Despliegue en AWS - Constructora Riera

Esta guía te llevará paso a paso para desplegar el proyecto **rieraconstruccions.com** en una máquina EC2 de AWS.

---

## 📋 Requisitos Previos

1. **Cuenta de AWS** activa
2. **Dominio registrado**: rieraconstruccions.com
3. **Tarjeta de crédito** para AWS (necesaria aunque uses capa gratuita)
4. **Cliente SSH** (incluido en Windows 10+, macOS, Linux)

---

## 🚀 Paso 1: Crear una Instancia EC2

### 1.1 Acceder a AWS Console
1. Ve a [AWS Console](https://console.aws.amazon.com)
2. Inicia sesión con tu cuenta
3. Busca "EC2" en el buscador superior
4. Haz clic en **"Instancias"** en el menú lateral

### 1.2 Lanzar Nueva Instancia
1. Clic en **"Lanzar instancia"**
2. **Nombre**: `constructora-riera-production`

### 1.3 Configurar Imagen y Tipo
- **AMI (Sistema Operativo)**: Ubuntu Server 22.04 LTS (Free tier eligible)
- **Tipo de instancia**: 
  - Desarrollo/Pruebas: `t2.micro` o `t3.micro` (1 vCPU, 1 GB RAM) - Free tier
  - Producción recomendada: `t3.small` (2 vCPU, 2 GB RAM) - ~$15/mes
  - Producción óptima: `t3.medium` (2 vCPU, 4 GB RAM) - ~$30/mes

### 1.4 Configurar Par de Claves (Key Pair)
1. Clic en **"Crear nuevo par de claves"**
2. **Nombre**: `constructora-riera-key`
3. **Tipo**: RSA
4. **Formato**: `.pem` (para Mac/Linux) o `.ppk` (para Windows con PuTTY)
5. **Descargar** y **guardar en lugar seguro** (no podrás descargarlo después)
6. En Windows PowerShell, mover a carpeta segura:
   ```powershell
   Move-Item .\constructora-riera-key.pem ~\.ssh\
   ```

### 1.5 Configurar Grupo de Seguridad (Firewall)
1. Marcar **"Crear grupo de seguridad"**
2. **Nombre**: `constructora-security-group`
3. **Descripción**: Security group for Constructora Riera
4. Agregar las siguientes reglas de **entrada**:

| Tipo | Protocolo | Puerto | Origen | Descripción |
|------|-----------|--------|--------|-------------|
| SSH | TCP | 22 | Mi IP | Acceso SSH seguro |
| HTTP | TCP | 80 | 0.0.0.0/0 | Tráfico web |
| HTTPS | TCP | 443 | 0.0.0.0/0 | Tráfico web seguro |

⚠️ **Importante**: Selecciona "Mi IP" para SSH por seguridad

### 1.6 Configurar Almacenamiento
- **Tamaño**: 20-30 GB (suficiente para el proyecto, DB, media, backups)
- **Tipo**: gp3 (más económico y rápido)

### 1.7 Lanzar Instancia
1. Revisar configuración en el resumen
2. Clic en **"Lanzar instancia"**
3. Esperar 2-3 minutos hasta que el estado sea **"Running"**
4. **Anotar la IP pública** (ej: `54.123.45.67`)

---

## 🔌 Paso 2: Conectarse a la Instancia EC2

### 2.1 Configurar Permisos de la Clave (Solo primera vez)

**En Windows PowerShell:**
```powershell
icacls $env:USERPROFILE\.ssh\constructora-riera-key.pem /inheritance:r
icacls $env:USERPROFILE\.ssh\constructora-riera-key.pem /grant:r "$($env:USERNAME):R"
```

**En Mac/Linux:**
```bash
chmod 400 ~/.ssh/constructora-riera-key.pem
```

### 2.2 Conectar por SSH

**Reemplaza `54.123.45.67` con tu IP pública de EC2**

```bash
ssh -i ~/.ssh/constructora-riera-key.pem ubuntu@54.123.45.67
```

Si aparece un warning de autenticidad, escribe `yes` y presiona Enter.

---

## 📦 Paso 3: Instalar Dependencias en el Servidor

### 3.1 Actualizar Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 3.2 Instalar Docker
```bash
# Instalar dependencias
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Agregar repositorio oficial de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Agregar usuario al grupo docker (para no usar sudo)
sudo usermod -aG docker ubuntu

# Verificar instalación
docker --version
```

### 3.3 Instalar Docker Compose
```bash
# Descargar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Dar permisos de ejecución
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker-compose --version
```

### 3.4 Instalar Git
```bash
sudo apt install -y git
git --version
```

### 3.5 **Cerrar sesión y volver a conectar** para aplicar permisos de Docker
```bash
exit
```

Vuelve a conectarte:
```bash
ssh -i ~/.ssh/constructora-riera-key.pem ubuntu@54.123.45.67
```

---

## 🌐 Paso 4: Configurar el Dominio (DNS)

### 4.1 Configurar Registros DNS

Ve al panel de tu proveedor de dominio (ej: Namecheap, GoDaddy, Google Domains) y crea los siguientes registros:

| Tipo | Nombre | Valor | TTL |
|------|--------|-------|-----|
| A | @ | `54.123.45.67` | 300 |
| A | www | `54.123.45.67` | 300 |
| A | admin | `54.123.45.67` | 300 |

**Reemplaza** `54.123.45.67` con tu IP pública de EC2.

⏱️ **Nota**: Los cambios DNS pueden tardar 5-60 minutos en propagarse.

### 4.2 Verificar Propagación
```bash
# Desde tu computadora local
nslookup rieraconstruccions.com
nslookup www.rieraconstruccions.com
nslookup admin.rieraconstruccions.com
```

---

## 📥 Paso 5: Clonar el Proyecto en el Servidor

### 5.1 Crear Directorio y Clonar
```bash
# Crear directorio para proyectos
mkdir -p ~/apps
cd ~/apps

# Clonar repositorio (ajusta la URL según tu repo)
git clone https://github.com/TU_USUARIO/RieraConstrucciones.git
cd RieraConstrucciones
```

### 5.2 Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar archivo .env
nano .env
```

**Configuración mínima requerida para producción:**

```env
# Django Settings
SECRET_KEY=GENERA_UNA_CLAVE_SUPER_SEGURA_AQUI_CON_50_CARACTERES
DEBUG=False
ALLOWED_HOSTS=rieraconstruccions.com,www.rieraconstruccions.com,admin.rieraconstruccions.com

# Configuración de Subdominios
SESSION_COOKIE_DOMAIN=.rieraconstruccions.com
CSRF_COOKIE_DOMAIN=.rieraconstruccions.com

# Database
DB_NAME=constructora_db
DB_USER=postgres
DB_PASSWORD=TU_PASSWORD_DE_BASE_DE_DATOS_MUY_SEGURO
DB_HOST=db
DB_PORT=5432

# Email Settings (Gmail)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=rieraconstruccions@gmail.com
EMAIL_HOST_PASSWORD=TU_APP_PASSWORD_DE_GMAIL
DEFAULT_FROM_EMAIL=rieraconstruccions@gmail.com
CONTACT_EMAIL=rieraconstruccions@gmail.com

# Site Configuration
SITE_NAME=Constructora Riera
SITE_URL=https://rieraconstruccions.com
```

### 5.3 Generar SECRET_KEY Segura

```bash
# Generar clave aleatoria
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y pégalo en `SECRET_KEY=` en el archivo `.env`

### 5.4 Guardar y Salir
- Presiona `Ctrl + X`
- Presiona `Y` para confirmar
- Presiona `Enter`

---

## 🔧 Paso 6: Configurar Gmail para Envío de Emails

### 6.1 Activar Verificación en 2 Pasos
1. Ve a [Google Account Security](https://myaccount.google.com/security)
2. Activa **"Verificación en 2 pasos"**

### 6.2 Generar App Password
1. Ve a [App Passwords](https://myaccount.google.com/apppasswords)
2. Selecciona **"Correo"** y **"Otro (nombre personalizado)"**
3. Escribe: `Constructora Riera Website`
4. Clic en **"Generar"**
5. Copia el password de 16 caracteres
6. Pégalo en `EMAIL_HOST_PASSWORD` en el archivo `.env`

---

## 🐳 Paso 7: Desplegar con Docker Compose

### 7.1 Construir y Levantar Contenedores
```bash
cd ~/apps/RieraConstrucciones

# Construir imágenes
docker-compose -f docker-compose.prod.yml build

# Levantar contenedores en segundo plano
docker-compose -f docker-compose.prod.yml up -d
```

### 7.2 Ejecutar Migraciones de Base de Datos
```bash
docker-compose -f docker-compose.prod.yml exec web python src/manage.py migrate
```

### 7.3 Recolectar Archivos Estáticos
```bash
docker-compose -f docker-compose.prod.yml exec web python src/manage.py collectstatic --noinput
```

### 7.4 Crear Superusuario (Admin)
```bash
docker-compose -f docker-compose.prod.yml exec web python src/manage.py createsuperuser
```

Introduce:
- **Username**: admin (o el que prefieras)
- **Email**: rieraconstruccions@gmail.com
- **Password**: Tu contraseña segura

### 7.5 Verificar Estado de Contenedores
```bash
docker-compose -f docker-compose.prod.yml ps
```

Todos deben estar **"Up"**.

---

## 🔒 Paso 8: Configurar HTTPS con Let's Encrypt (SSL)

### 8.1 Obtener Certificado SSL Inicial

```bash
# Crear directorios para Certbot
mkdir -p ~/apps/RieraConstrucciones/certbot/conf
mkdir -p ~/apps/RieraConstrucciones/certbot/www

# Obtener certificado (reemplaza el email)
docker-compose -f docker-compose.prod.yml run --rm certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email rieraconstruccions@gmail.com \
  --agree-tos \
  --no-eff-email \
  -d rieraconstruccions.com \
  -d www.rieraconstruccions.com \
  -d admin.rieraconstruccions.com
```

### 8.2 Activar Configuración SSL en Nginx

```bash
# Hacer backup de configuración actual
cp nginx/default.conf nginx/default.conf.backup

# Usar configuración SSL
cp nginx/default-ssl.conf nginx/default.conf

# Reiniciar Nginx para aplicar HTTPS
docker-compose -f docker-compose.prod.yml restart nginx
```

### 8.3 Verificar Certificado
```bash
# Ver detalles del certificado
docker-compose -f docker-compose.prod.yml exec certbot certbot certificates
```

---

## ✅ Paso 9: Verificar el Despliegue

### 9.1 Probar URLs

Abre un navegador y verifica:

- ✅ **https://rieraconstruccions.com** - Página principal
- ✅ **https://www.rieraconstruccions.com** - Debe redirigir correctamente
- ✅ **https://rieraconstruccions.com/django-admin/** - Panel de administración Django
- ✅ **https://admin.rieraconstruccions.com/backoffice/** - Backoffice personalizado
- ✅ **https://rieraconstruccions.com/servicios/** - Página de servicios
- ✅ **https://rieraconstruccions.com/blog/** - Blog
- ✅ **https://rieraconstruccions.com/contacto/** - Formulario de contacto

### 9.2 Verificar SSL

Usa [SSL Labs](https://www.ssllabs.com/ssltest/) para verificar que el certificado SSL está correctamente configurado.

### 9.3 Ver Logs

```bash
# Ver logs de todos los contenedores
docker-compose -f docker-compose.prod.yml logs -f

# Ver logs solo de Django
docker-compose -f docker-compose.prod.yml logs -f web

# Ver logs solo de Nginx
docker-compose -f docker-compose.prod.yml logs -f nginx
```

---

## 🔧 Comandos Útiles de Mantenimiento

### Reiniciar Servicios
```bash
cd ~/apps/RieraConstrucciones

# Reiniciar todos los servicios
docker-compose -f docker-compose.prod.yml restart

# Reiniciar solo Django
docker-compose -f docker-compose.prod.yml restart web

# Reiniciar solo Nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

### Actualizar Código
```bash
cd ~/apps/RieraConstrucciones

# Descargar cambios del repositorio
git pull origin main

# Reconstruir y reiniciar
docker-compose -f docker-compose.prod.yml up -d --build

# Ejecutar migraciones si hay cambios en modelos
docker-compose -f docker-compose.prod.yml exec web python src/manage.py migrate

# Recolectar archivos estáticos
docker-compose -f docker-compose.prod.yml exec web python src/manage.py collectstatic --noinput
```

### Backup de Base de Datos
```bash
# Crear backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres constructora_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar backup
docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres constructora_db < backup_20260103.sql
```

### Limpiar Caché de Django
```bash
docker-compose -f docker-compose.prod.yml exec web python src/manage.py shell -c "from django.core.cache import cache; cache.clear(); print('Caché limpiada')"
```

### Ver Espacio en Disco
```bash
df -h
docker system df
```

### Limpiar Imágenes Docker Antiguas
```bash
docker system prune -a --volumes
```

---

## 🚨 Solución de Problemas Comunes

### Problema: "502 Bad Gateway"
```bash
# Verificar que los contenedores están corriendo
docker-compose -f docker-compose.prod.yml ps

# Ver logs de Django
docker-compose -f docker-compose.prod.yml logs web

# Reiniciar servicios
docker-compose -f docker-compose.prod.yml restart
```

### Problema: "Database connection error"
```bash
# Verificar que PostgreSQL está corriendo
docker-compose -f docker-compose.prod.yml ps db

# Ver logs de la base de datos
docker-compose -f docker-compose.prod.yml logs db

# Reiniciar base de datos
docker-compose -f docker-compose.prod.yml restart db
```

### Problema: "Static files not loading"
```bash
# Recolectar archivos estáticos nuevamente
docker-compose -f docker-compose.prod.yml exec web python src/manage.py collectstatic --noinput

# Verificar permisos
docker-compose -f docker-compose.prod.yml exec web ls -la /app/staticfiles
```

### Problema: "Certificate error" o SSL no funciona
```bash
# Renovar certificado manualmente
docker-compose -f docker-compose.prod.yml run --rm certbot renew

# Reiniciar Nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

---

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real
```bash
# Todos los servicios
docker-compose -f docker-compose.prod.yml logs -f --tail=100

# Solo errores
docker-compose -f docker-compose.prod.yml logs -f | grep -i error
```

### Verificar Uso de Recursos
```bash
# CPU y memoria de contenedores
docker stats

# Espacio en disco
df -h
du -sh ~/apps/RieraConstrucciones/*
```

---

## 🔐 Seguridad Adicional (Recomendado)

### Configurar Firewall UFW
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status
```

### Deshabilitar Login Root SSH
```bash
sudo nano /etc/ssh/sshd_config
```

Cambia:
```
PermitRootLogin no
PasswordAuthentication no
```

Reinicia SSH:
```bash
sudo systemctl restart sshd
```

### Configurar Fail2Ban (Protección contra ataques de fuerza bruta)
```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 💰 Costos Estimados AWS

### Opción 1: Free Tier (12 meses)
- **EC2 t2.micro**: Gratis
- **EBS 30 GB**: Gratis
- **Tráfico**: 15 GB/mes gratis
- **Total**: $0/mes (primeros 12 meses)

### Opción 2: Producción Básica
- **EC2 t3.small**: ~$15/mes
- **EBS 30 GB**: ~$3/mes
- **Tráfico**: ~$0.09/GB (después de 1 GB gratis)
- **Total**: ~$18-25/mes

### Opción 3: Producción Óptima
- **EC2 t3.medium**: ~$30/mes
- **EBS 50 GB**: ~$5/mes
- **RDS PostgreSQL** (opcional): ~$15-30/mes
- **CloudFront CDN** (opcional): ~$5-10/mes
- **Total**: ~$50-80/mes

---

## 📞 Soporte

Si tienes problemas durante el despliegue:

1. **Revisa los logs**: `docker-compose -f docker-compose.prod.yml logs -f`
2. **Verifica el estado**: `docker-compose -f docker-compose.prod.yml ps`
3. **Consulta la documentación**: Este archivo
4. **Contacta al desarrollador**: [Tu información de contacto]

---

## ✨ ¡Felicidades!

Tu sitio web **rieraconstruccions.com** está ahora en producción en AWS. 🎉

**URLs importantes:**
- 🌐 Sitio web: https://rieraconstruccions.com
- 🔒 Admin Django: https://rieraconstruccions.com/django-admin/
- 💼 Backoffice: https://admin.rieraconstruccions.com/backoffice/

---

**Última actualización**: Enero 2026
