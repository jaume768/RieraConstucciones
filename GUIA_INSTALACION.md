# 🏗️ Guía de Instalación - Constructora Riera

Esta guía te llevará paso a paso para poner en marcha el proyecto completo.

## 📋 Requisitos Previos

- Python 3.11 o superior
- PostgreSQL 15 o superior
- Node.js 18 o superior (para Tailwind CSS)
- Git (opcional)

## 🚀 Pasos de Instalación

### 1️⃣ Configurar Variables de Entorno

Copia el archivo `.env.example` a `.env`:

```powershell
copy .env.example .env
```

Edita el archivo `.env` y configura tus credenciales de PostgreSQL:

```env
DB_NAME=constructora_db
DB_USER=postgres
DB_PASSWORD=tu_password_aqui
DB_HOST=localhost
DB_PORT=5432
```

### 2️⃣ Crear Base de Datos PostgreSQL

Abre **pgAdmin** o **psql** y ejecuta:

```sql
CREATE DATABASE constructora_db;
```

Si necesitas crear el usuario:

```sql
CREATE USER postgres WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE constructora_db TO postgres;
```

### 3️⃣ Instalar Dependencias de Python

Activa el entorno virtual (ya está creado):

```powershell
.\venv\Scripts\activate
```

Las dependencias ya están instaladas. Si necesitas reinstalarlas:

```powershell
pip install -r requirements.txt
```

### 4️⃣ Aplicar Migraciones de Base de Datos

```powershell
cd src
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Crear Superusuario para el Admin

```powershell
python manage.py createsuperuser
```

Te pedirá:
- Username (nombre de usuario)
- Email
- Password (contraseña)

### 6️⃣ Configurar Tailwind CSS

Vuelve a la raíz del proyecto:

```powershell
cd ..
```

Instala las dependencias de Node.js:

```powershell
npm install
```

Compila Tailwind CSS:

```powershell
npm run build
```

Para desarrollo (modo watch, recompila automáticamente):

```powershell
npm run watch
```

### 7️⃣ Recopilar Archivos Estáticos

```powershell
cd src
python manage.py collectstatic --noinput
```

### 8️⃣ Ejecutar el Servidor de Desarrollo

```powershell
python manage.py runserver
```

El servidor estará disponible en: **http://localhost:8000**

## 🎯 Acceder al Panel de Administración

1. Ve a: **http://localhost:8000/admin**
2. Inicia sesión con el superusuario que creaste
3. Comienza a crear contenido:
   - **Páginas** (Core > Páginas)
   - **Blog Posts** (Blog y Noticias > Posts)
   - **Servicios** (Servicios > Servicios)
   - **Equipo** (Core > Equipo)
   - **Valores** (Core > Valores de la Empresa)

## 📝 Contenido Inicial Recomendado

### Crear Página "Sobre Nosotros"

1. Ve a **Core > Páginas > Añadir página**
2. Configura:
   - **Título**: "Sobre Nosotros"
   - **Slug**: "sobre-nosotros"
   - **Contenido**: Texto corporativo sobre la empresa
   - **Meta Title**: "Sobre Nosotros - Constructora Riera"
   - **Meta Description**: "Conoce nuestra historia, equipo y valores..."
   - **Publicado**: ✅

### Crear Servicios

1. Ve a **Servicios > Servicios > Añadir servicio**
2. Crea servicios como:
   - **Obra Nueva** (slug: `obra-nueva`, icon: `fa-solid fa-building`)
   - **Reformas Integrales** (slug: `reformas`, icon: `fa-solid fa-hammer`)
   - **Rehabilitaciones** (slug: `rehabilitaciones`, icon: `fa-solid fa-wrench`)

### Crear Categorías y Posts de Blog

1. **Categorías**: Ve a **Blog y Noticias > Categorías**
   - Noticias
   - Consejos
   - Proyectos

2. **Posts**: Ve a **Blog y Noticias > Posts**
   - Crea posts con imágenes destacadas
   - Asigna categorías
   - Añade etiquetas
   - Marca como **Publicado** y **Destacado**

### Añadir Equipo

1. Ve a **Core > Equipo > Añadir miembro del equipo**
2. Añade fotos, nombres, cargos y biografías

### Configurar Valores de la Empresa

1. Ve a **Core > Valores de la Empresa**
2. Añade valores como:
   - Calidad
   - Compromiso
   - Innovación
   - Sostenibilidad

## 🔧 Comandos Útiles

### Desarrollo

```powershell
# Activar entorno virtual
.\venv\Scripts\activate

# Ejecutar servidor de desarrollo
cd src
python manage.py runserver

# Compilar CSS (en otra terminal)
npm run watch
```

### Migraciones

```powershell
cd src
python manage.py makemigrations
python manage.py migrate
```

### Crear Nuevo Superusuario

```powershell
cd src
python manage.py createsuperuser
```

### Limpiar Base de Datos (CUIDADO: Borra todo)

```powershell
cd src
python manage.py flush
```

## 🐳 Despliegue con Docker (Opcional)

Si prefieres usar Docker:

```powershell
docker-compose up -d
```

Esto levantará:
- Base de datos PostgreSQL (puerto 5432)
- Aplicación Django (puerto 8000)
- Nginx (puerto 80)

### Ejecutar Migraciones en Docker

```powershell
docker-compose exec web python src/manage.py migrate
docker-compose exec web python src/manage.py createsuperuser
```

## 🌐 Estructura de URLs

- **Home**: http://localhost:8000/
- **Sobre Nosotros**: http://localhost:8000/sobre-nosotros/
- **Servicios**: http://localhost:8000/servicios/
- **Servicio Detalle**: http://localhost:8000/servicios/obra-nueva/
- **Blog**: http://localhost:8000/blog/
- **Post Detalle**: http://localhost:8000/blog/titulo-del-post/
- **Contacto**: http://localhost:8000/contacto/
- **Admin**: http://localhost:8000/admin/
- **Sitemap**: http://localhost:8000/sitemap.xml
- **Robots**: http://localhost:8000/robots.txt

## 📧 Configuración de Email

Para que el formulario de contacto envíe emails reales, configura en `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
DEFAULT_FROM_EMAIL=info@constructora.com
CONTACT_EMAIL=destino@constructora.com
```

**Nota para Gmail**: Necesitas generar una "contraseña de aplicación" en tu cuenta de Google.

## 🎨 Personalización de Diseño

Los colores principales se configuran en `tailwind.config.js`:

```javascript
colors: {
  primary: {
    500: '#0ea5e9',  // Color principal
    600: '#0284c7',  // Color hover
    // ...
  },
}
```

Después de cambiar colores, recompila:

```powershell
npm run build
```

## 🔍 SEO - Archivos Importantes

- **Sitemap XML**: Generado automáticamente en `/sitemap.xml`
- **Robots.txt**: Configurado en `templates/robots.txt`
- **Meta Tags**: Implementados en todos los templates
- **Open Graph**: Configurado para redes sociales
- **JSON-LD**: Schema.org para Organization y Article

## ⚠️ Solución de Problemas

### Error de Conexión a PostgreSQL

```
django.db.utils.OperationalError: could not connect to server
```

**Solución**: Verifica que PostgreSQL esté corriendo y las credenciales en `.env` sean correctas.

### Error con Tailwind CSS

```
Error: Cannot find module 'tailwindcss'
```

**Solución**: 
```powershell
npm install
```

### Error de Importación de Apps

```
ModuleNotFoundError: No module named 'core'
```

**Solución**: Asegúrate de estar en la carpeta `src` cuando ejecutas `python manage.py runserver`.

## 📚 Recursos Adicionales

- [Documentación Django](https://docs.djangoproject.com/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [PostgreSQL](https://www.postgresql.org/docs/)

## 🆘 Soporte

Si encuentras algún problema, revisa:
1. Las credenciales de base de datos en `.env`
2. Que PostgreSQL esté corriendo
3. Que el entorno virtual esté activado
4. Los logs del servidor en la terminal

¡Listo! Tu web corporativa está configurada y lista para usar. 🎉
