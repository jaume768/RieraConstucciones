# 🚀 PASOS PARA COMPLETAR MULTIIDIOMA

## ✅ YA ESTÁ HECHO (No tocar)
- Modelos migrados a TranslatableModel
- Admin con pestañas por idioma
- Settings.py configurado
- URLs con i18n_patterns
- Messages traducibles en views.py
- Templates principales parcialmente traducidos

---

## 📝 PASOS QUE DEBES HACER

### **PASO 1: Completar Traducciones en Templates** (30-60 min)

Necesitas agregar `{% trans %}` a textos hardcodeados en estos archivos:

**1.1 Footer en `templates/base.html`** (líneas 125-156)
```django
{% load i18n %}

{# Cambiar: #}
<h4>Enlaces</h4>  ❌
{# Por: #}
<h4>{% trans "Enlaces" %}</h4>  ✅
```

**1.2 `templates/core/about.html`** (Todo el archivo)
- Título principal
- Secciones de equipo y valores
- Textos descriptivos

**1.3 `templates/services/services_list.html`**
- Título "Todos Nuestros Servicios"
- Botón "Ver Detalle"
- Mensaje "No hay servicios"

**1.4 `templates/services/service_detail.html`**
- Botón "Volver a Servicios"
- Botón "Solicitar Presupuesto"

**1.5 `templates/blog/blog_list.html`**
- Título "Blog y Noticias"
- Filtros "Todas las Categorías"
- Botón "Leer Más"

**1.6 `templates/blog/blog_detail.html`**
- "Artículos Relacionados"
- "Compartir en redes"
- Botones de navegación

**Ejemplo de cómo hacerlo:**
```django
{# 1. Agregar load al inicio del archivo #}
{% load i18n %}

{# 2. Envolver textos con {% trans %} #}
<button>Contactar</button>
↓
<button>{% trans "Contactar" %}</button>

{# 3. Para textos con HTML o variables, usar {% blocktrans %} #}
<p>Tenemos {{ count }} servicios</p>
↓
<p>{% blocktrans count=count %}Tenemos {{ count }} servicios{% endblocktrans %}</p>
```

---

### **PASO 2: Generar Archivos de Traducción** (5 min)

```bash
# En local (Windows)
cd C:\Users\jaume\OneDrive\Imágenes\Escritorio\Proyectos\RieraConstrucciones\src

# Generar archivos .po
python manage.py makemessages -l ca
python manage.py makemessages -l en
python manage.py makemessages -l de
```

Esto creará:
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

---

### **PASO 3: Traducir los Archivos .po** (2-4 horas)

**Opción A: Manual con Editor**
1. Instalar: https://poedit.net/
2. Abrir cada archivo `.po`
3. Traducir cada string
4. Guardar

**Opción B: Con DeepL (Recomendado)**
1. Abrir `locale/ca/LC_MESSAGES/django.po` con notepad
2. Buscar líneas con `msgid` y `msgstr ""`
3. Copiar texto español → Pegar en https://deepl.com
4. Copiar traducción → Pegar en `msgstr ""`

**Ejemplo:**
```po
# locale/ca/LC_MESSAGES/django.po
msgid "Calidad Garantizada"
msgstr "Qualitat Garantida"

msgid "Pedir Presupuesto"
msgstr "Demanar Pressupost"

msgid "Nuestros Servicios"
msgstr "Els Nostres Serveis"
```

```po
# locale/en/LC_MESSAGES/django.po
msgid "Calidad Garantizada"
msgstr "Guaranteed Quality"

msgid "Pedir Presupuesto"
msgstr "Request Quote"

msgid "Nuestros Servicios"
msgstr "Our Services"
```

```po
# locale/de/LC_MESSAGES/django.po
msgid "Calidad Garantizada"
msgstr "Garantierte Qualität"

msgid "Pedir Presupuesto"
msgstr "Angebot Anfordern"

msgid "Nuestros Servicios"
msgstr "Unsere Dienstleistungen"
```

---

### **PASO 4: Compilar Traducciones** (1 min)

```bash
cd src
python manage.py compilemessages
```

Esto genera archivos `.mo` (binarios) que Django lee.

---

### **PASO 5: Migrar Base de Datos** (5 min)

```bash
cd src

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones  
python manage.py migrate

# Migrar datos existentes a traducción español
python ../migrate_to_parler.py
```

---

### **PASO 6: Probar en Local** (10 min)

```bash
python manage.py runserver
```

1. Ir a: http://localhost:8000
2. Probar selector de idioma en menú
3. Verificar que textos cambian
4. Ir al admin: http://localhost:8000/django-admin/
5. Editar un servicio → Ver pestañas [ES] [CA] [EN] [DE]
6. Agregar traducciones catalán en pestaña [CA]

---

### **PASO 7: Desplegar en AWS** (15 min)

```bash
# 1. Subir cambios
git add .
git commit -m "Sistema multiidioma completo"
git push

# 2. En el servidor AWS
ssh admin@tu-ip-aws

cd ~/RieraConstucciones
git pull

# 3. Reconstruir contenedor
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build web
docker-compose -f docker-compose.prod.yml up -d

# 4. Migrar base de datos
docker-compose -f docker-compose.prod.yml exec web python src/manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python migrate_to_parler.py

# 5. Compilar traducciones (si editaste .po en servidor)
docker-compose -f docker-compose.prod.yml exec web python src/manage.py compilemessages

# 6. Reiniciar
docker-compose -f docker-compose.prod.yml restart
```

---

### **PASO 8: Traducir Contenido en Admin** (1-2 horas)

1. Ir a: https://admin.rieraconstruccions.com/django-admin/
2. Entrar con tu usuario
3. Click en "Servicios"
4. Editar cada servicio:
   - Pestaña [ES] → Ya está (español)
   - Pestaña [CA] → Traducir al catalán
   - Pestaña [EN] → Traducir al inglés (opcional)
   - Pestaña [DE] → Traducir al alemán (opcional)
5. Repetir para:
   - Posts del blog
   - Páginas estáticas
   - Miembros del equipo
   - Valores de la empresa

**Tip:** Empieza solo con español y catalán para tu mercado local.

---

## 📊 Checklist Final

```
[ ] Paso 1: Traducir templates con {% trans %}
[ ] Paso 2: Generar archivos .po
[ ] Paso 3: Traducir archivos .po (CA, EN, DE)
[ ] Paso 4: Compilar traducciones
[ ] Paso 5: Migrar base de datos
[ ] Paso 6: Probar en local
[ ] Paso 7: Desplegar en AWS
[ ] Paso 8: Traducir contenido en admin
[ ] Paso 9: Probar URLs: /ca/, /en/, /de/
[ ] Paso 10: Verificar SEO con meta tags por idioma
```

---

## 🆘 Troubleshooting

**"No veo las pestañas de idioma en el admin"**
→ Verifica que el admin use `TranslatableAdmin` (ya está hecho)

**"Los textos no cambian de idioma"**
→ Ejecuta `python manage.py compilemessages`
→ Reinicia el servidor

**"Error al guardar traducción"**
→ Debes rellenar al menos el campo título en cada idioma

**"El selector de idioma no aparece"**
→ Verifica que base.html tenga `{% load i18n %}`
→ Verifica que el middleware LocaleMiddleware esté en settings

---

## 💰 Presupuesto de Tiempo

| Tarea | Tiempo |
|-------|--------|
| Completar templates | 1h |
| Generar .po | 5min |
| Traducir .po (ES→CA) | 1h |
| Traducir .po (ES→EN) | 1h |
| Traducir .po (ES→DE) | 1h |
| Migrar y probar | 30min |
| Traducir contenido admin | 2h |
| **TOTAL** | **~7 horas** |

**Recomendación:** Empieza con español y catalán solamente (4 horas).

---

¡Éxito! 🚀
