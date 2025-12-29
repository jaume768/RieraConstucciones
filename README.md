# Constructora Riera - Web Corporativa

Web corporativa moderna para empresa constructora con blog integrado, desarrollada con Django, PostgreSQL y Tailwind CSS.

## Características

- ✅ Páginas corporativas (Inicio, Sobre nosotros, Servicios, Contacto)
- ✅ Blog/Noticias con categorías y etiquetas
- ✅ Panel de administración completo
- ✅ SEO optimizado (meta tags, Open Graph, sitemap, robots.txt)
- ✅ Diseño responsive con Tailwind CSS
- ✅ Formulario de contacto con anti-spam
- ✅ PostgreSQL como base de datos

## Stack Tecnológico

- **Backend**: Django 4.2
- **Base de datos**: PostgreSQL
- **Frontend**: Django Templates + Tailwind CSS
- **Servidor**: Gunicorn + Nginx
- **Estilos**: Tailwind CSS

## Instalación y Configuración

### 1. Crear entorno virtual (Windows)

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y ajusta los valores:

```powershell
copy .env.example .env
```

Edita el archivo `.env` con tus credenciales de PostgreSQL y configuración de email.

### 4. Crear base de datos PostgreSQL

Abre pgAdmin o psql y ejecuta:

```sql
CREATE DATABASE constructora_db;
CREATE USER postgres WITH PASSWORD 'tu_password';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE constructora_db TO postgres;
```

### 5. Aplicar migraciones

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```powershell
python manage.py createsuperuser
```

### 7. Configurar Tailwind CSS

```powershell
npm install
npm run build
```

### 8. Ejecutar servidor de desarrollo

```powershell
python manage.py runserver
```

Accede a:
- Web: http://localhost:8000
- Admin: http://localhost:8000/admin

## Estructura del Proyecto

```
constructora/
├── core/              # App principal (páginas estáticas, layout)
├── blog/              # App de blog/noticias
├── services/          # App de servicios
├── constructora/      # Configuración del proyecto
├── templates/         # Plantillas Django
├── static/            # Archivos estáticos
├── media/             # Archivos subidos por usuarios
└── requirements.txt   # Dependencias Python
```

## Gestión de Contenido

Todo el contenido se gestiona desde el panel de administración de Django en `/admin`:

- **Páginas**: Gestión de contenido de páginas estáticas
- **Blog**: Crear y editar posts, categorías y etiquetas
- **Servicios**: Gestión de servicios ofrecidos
- **Equipo**: Miembros del equipo de la empresa
- **Valores**: Valores corporativos de la empresa

## SEO

El proyecto incluye:

- URLs amigables con slugs
- Meta tags dinámicos (title, description)
- Open Graph para redes sociales
- Sitemap XML automático
- Robots.txt configurado
- JSON-LD para Schema.org (Organization, Article)
- Canonical URLs

## Despliegue con Docker

```powershell
docker-compose up -d
```

## Licencia

Proyecto privado - Constructora Riera
