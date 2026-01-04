# 🌍 Guía de Multiidioma - Riera Construcciones

## 📋 Idiomas Soportados

- 🇪🇸 **Español** (es) - Idioma por defecto
- 🇪🇸 **Català** (ca)
- 🇬🇧 **English** (en)
- 🇩🇪 **Deutsch** (de)

---

## 🎯 Cómo Funciona el Backoffice

### **Sistema de Pestañas por Idioma**

Cuando edites un **Servicio**, **Post del Blog** o cualquier contenido traducible, verás pestañas en la parte superior del formulario:

```
┌─────────────────────────────────────────────┐
│  [ ES ] [ CA ] [ EN ] [ DE ]  ← Pestañas   │
├─────────────────────────────────────────────┤
│  📝 Español (Idioma actual)                 │
│                                             │
│  Título: _____________________________      │
│  Descripción corta: ___________________     │
│  Contenido: __________________________      │
│  Meta Title SEO: _____________________      │
│  Meta Description SEO: ________________     │
│                                             │
│  [ Guardar ]                                │
└─────────────────────────────────────────────┘
```

### **Flujo de Trabajo Completo**

#### **1. Crear Contenido Nuevo (Español - Obligatorio)**

1. Ve a **Servicios** o **Posts** en el admin
2. Click en **"Añadir servicio"** o **"Añadir post"**
3. La pestaña **[ES]** estará activa por defecto
4. Rellena **TODOS** los campos en español:
   - Título
   - Slug (se genera automáticamente)
   - Descripción corta
   - Contenido completo
   - Meta Title SEO
   - Meta Description SEO
   - Imagen (común para todos los idiomas)
   - Icono (común para todos los idiomas)
5. Click en **"Guardar y continuar editando"**

#### **2. Agregar Traducción al Catalán**

1. Click en la pestaña **[CA]**
2. Verás el formulario VACÍO (es normal)
3. Traduce TODOS los campos al catalán:
   - Título → Títol
   - Descripción corta → Descripció curta
   - Contenido → Contingut
   - Meta Title SEO → Meta Títol
   - Meta Description SEO → Meta Descripció
4. Click en **"Guardar y continuar editando"**

#### **3. Agregar Traducción al Inglés**

1. Click en la pestaña **[EN]**
2. Traduce todos los campos al inglés
3. Click en **"Guardar y continuar editando"**

#### **4. Agregar Traducción al Alemán**

1. Click en la pestaña **[DE]**
2. Traduce todos los campos al alemán
3. Click en **"Guardar"**

### **⚠️ Importante: Fallback a Español**

- Si un idioma NO tiene traducción, el sistema mostrará el contenido en **español** automáticamente
- Ejemplo: Si un servicio solo está en español y catalán, cuando un alemán visite la web verá el contenido en español
- **Recomendación**: Completa al menos **español** y **catalán** para todos los contenidos (tu mercado principal)

---

## 🚀 Instrucciones de Despliegue

### **Paso 1: Instalar Dependencias**

```bash
pip install -r requirements.txt
```

### **Paso 2: Crear Migraciones**

```bash
cd src
python manage.py makemigrations
python manage.py migrate
```

### **Paso 3: Migrar Datos Existentes**

Si ya tienes servicios, posts o páginas creadas:

```bash
python migrate_to_parler.py
```

Este script copiará todos los datos existentes a las tablas de traducción en español.

### **Paso 4: Crear Carpetas de Traducción**

```bash
cd src
python manage.py makemessages -l ca
python manage.py makemessages -l en
python manage.py makemessages -l de
python manage.py compilemessages
```

### **Paso 5: Traducir Textos Estáticos**

Los textos como "Inicio", "Nosotros", "Servicios", "Contacto" se traducen editando los archivos `.po` en:

```
locale/
├── ca/
│   └── LC_MESSAGES/
│       └── django.po  ← Traducciones al catalán
├── en/
│   └── LC_MESSAGES/
│       └── django.po  ← Traducciones al inglés
└── de/
    └── LC_MESSAGES/
        └── django.po  ← Traducciones al alemán
```

Después de editar, ejecutar:

```bash
python manage.py compilemessages
```

---

## 🌐 Cómo Funciona en la Web

### **URLs por Idioma**

- **Español**: `https://rieraconstruccions.com/` (sin prefijo)
- **Catalán**: `https://rieraconstruccions.com/ca/`
- **Inglés**: `https://rieraconstruccions.com/en/`
- **Alemán**: `https://rieraconstruccions.com/de/`

### **Ejemplos de URLs**

| Página | Español | Catalán | Inglés | Alemán |
|--------|---------|---------|--------|--------|
| Inicio | `/` | `/ca/` | `/en/` | `/de/` |
| Servicios | `/servicios/` | `/ca/servicios/` | `/en/servicios/` | `/de/servicios/` |
| Blog | `/blog/` | `/ca/blog/` | `/en/blog/` | `/de/blog/` |
| Contacto | `/contacto/` | `/ca/contacto/` | `/en/contacto/` | `/de/contacto/` |

### **Selector de Idioma**

En la esquina superior derecha del menú verás:

```
[ 🌐 ES ▼ ]
```

Al hacer hover se despliega:

```
┌──────────────┐
│ Español   ✓  │
│ Català       │
│ English      │
│ Deutsch      │
└──────────────┘
```

---

## 📊 Estado de Traducciones

### **Modelos Traducibles**

✅ **Service** (Servicios)
- title, short_description, description, meta_title, meta_description

✅ **Post** (Blog)
- title, summary, content, meta_title, meta_description

✅ **Category** (Categorías del Blog)
- name, description

✅ **Tag** (Etiquetas del Blog)
- name

✅ **Page** (Páginas Estáticas)
- title, content, meta_title, meta_description

✅ **TeamMember** (Equipo)
- position, bio

✅ **CompanyValue** (Valores de la Empresa)
- title, description

### **Campos NO Traducibles (Comunes a todos los idiomas)**

- `slug` - URL única
- `image` / `photo` - Imágenes
- `icon` - Iconos
- `order` - Orden de visualización
- `is_active` / `is_published` - Estado
- `created_at` / `updated_at` - Fechas
- `email` / `linkedin` - Contactos
- `author` - Autor del post
- `category` / `tags` - Relaciones

---

## 🎨 Templates con Traducciones

Los textos estáticos en templates se traducen con:

```django
{% load i18n %}

<h1>{% trans "Nuestros Servicios" %}</h1>
<p>{% trans "Contacta con nosotros" %}</p>

{# Para textos con variables: #}
{% blocktrans %}Bienvenido {{ user.name }}{% endblocktrans %}
```

---

## 💡 Tips y Mejores Prácticas

### **1. Prioriza Español y Catalán**

Para tu mercado local (Mallorca), estos son los más importantes. Inglés y alemán son secundarios para turistas.

### **2. Usa DeepL para Traducir**

- DeepL tiene mejor calidad que Google Translate
- Copia el texto español → Pega en DeepL → Copia traducción
- **Siempre revisa** las traducciones automáticas

### **3. Traduce Meta Tags SEO**

Los meta_title y meta_description son cruciales para SEO multiidioma:
- **Español**: "Construcción y Reformas en Mallorca"
- **Catalán**: "Construcció i Reformes a Mallorca"
- **Inglés**: "Construction and Renovations in Mallorca"
- **Alemán**: "Bau und Renovierungen auf Mallorca"

### **4. URLs NO se Traducen**

El slug es el mismo para todos los idiomas:
- ❌ INCORRECTO: `/en/construction-services/` vs `/es/servicios-construccion/`
- ✅ CORRECTO: `/en/servicios-construccion/` (mismo slug)

### **5. Contenido Dinámico desde Admin**

- Servicios, Posts, Páginas → Se traducen desde el admin con pestañas
- Textos fijos (menú, footer, botones) → Se traducen en archivos `.po`

---

## 🔧 Troubleshooting

### **"No veo las pestañas de idioma"**

Verifica que `TranslatableAdmin` esté en el admin:
```python
from parler.admin import TranslatableAdmin

class ServiceAdmin(TranslatableAdmin):
    pass
```

### **"El contenido no cambia de idioma"**

1. Verifica que el modelo tenga `translations = TranslatedFields(...)`
2. Ejecuta `python manage.py migrate`
3. Borra la caché: `python manage.py shell` → `from django.core.cache import cache` → `cache.clear()`

### **"Error al guardar traducción"**

Asegúrate de rellenar al menos el campo `title` en la traducción. Algunos campos son obligatorios.

---

## 📞 Soporte

Si tienes dudas:
1. Revisa esta guía
2. Consulta la documentación de django-parler: https://django-parler.readthedocs.io/
3. Pregunta al desarrollador

---

**¡Éxito con tu proyecto multiidioma! 🚀**
