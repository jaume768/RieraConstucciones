# 🐳 COMANDOS DOCKER PARA MULTIIDIOMA

## 📋 Tu Setup Docker Actual
```
CONTAINER ID   IMAGE                     COMMAND                  PORTS                    NAMES
153ad0732106   nginx:alpine              ...                      0.0.0.0:80->80/tcp       constructora_nginx
ba93c7e94c66   rieraconstrucciones-web   ...                      0.0.0.0:8000->8000/tcp   constructora_web
7fc24dad2bda   postgres:15-alpine        ...                      0.0.0.0:5432->5432/tcp   constructora_db
```

**Contenedores:**
- `constructora_web` → Django + Gunicorn
- `constructora_nginx` → Nginx (proxy)
- `constructora_db` → PostgreSQL

---

## 🚀 PASO 1: Reconstruir Contenedor Web

```powershell
# Detener contenedores
docker-compose down

# Reconstruir SOLO el contenedor web (con nuevos cambios)
docker-compose build web

# O si usas docker-compose.prod.yml:
docker-compose -f docker-compose.prod.yml build web

# Levantar todo de nuevo
docker-compose up -d
```

**¿Por qué?** Porque has agregado `django-parler` a `requirements.txt` y modificado código Python.

---

## 🔄 PASO 2: Hacer Migraciones de Base de Datos

### **Opción A: Con docker-compose exec (Contenedor corriendo)**

```powershell
# Crear archivos de migración
docker-compose exec web python src/manage.py makemigrations

# Aplicar migraciones
docker-compose exec web python src/manage.py migrate

# Ver migraciones aplicadas
docker-compose exec web python src/manage.py showmigrations
```

### **Opción B: Con docker-compose run (Contenedor apagado)**

```powershell
# Si el contenedor está parado
docker-compose run --rm web python src/manage.py makemigrations
docker-compose run --rm web python src/manage.py migrate
```

### **Tu caso específico (nombres actuales):**

```powershell
# Usando el nombre real del contenedor
docker exec constructora_web python src/manage.py makemigrations
docker exec constructora_web python src/manage.py migrate
```

---

## 📦 PASO 3: Migrar Datos Existentes a Parler

```powershell
# Ejecutar script de migración de datos
docker exec constructora_web python migrate_to_parler.py

# O si está en otra ubicación:
docker exec constructora_web python /app/migrate_to_parler.py
```

**Esto copia:**
- Servicios actuales → Traducción español
- Posts actuales → Traducción español
- Páginas actuales → Traducción español

---

## 🌍 PASO 4: Generar Archivos de Traducción (.po)

### **4.1 Crear carpetas de idiomas**

```powershell
# Catalán
docker exec constructora_web python src/manage.py makemessages -l ca

# Inglés
docker exec constructora_web python src/manage.py makemessages -l en

# Alemán
docker exec constructora_web python src/manage.py makemessages -l de

# Todos a la vez
docker exec constructora_web sh -c "cd src && python manage.py makemessages -l ca && python manage.py makemessages -l en && python manage.py makemessages -l de"
```

**Esto crea:**
```
locale/
├── ca/LC_MESSAGES/django.po
├── en/LC_MESSAGES/django.po
└── de/LC_MESSAGES/django.po
```

### **4.2 Extraer archivos .po del contenedor (para editarlos en local)**

```powershell
# Copiar carpeta locale del contenedor a tu máquina
docker cp constructora_web:/app/locale ./locale

# O si locale está en src:
docker cp constructora_web:/app/src/locale ./locale
```

### **4.3 Editar archivos .po en tu máquina**

Con **Notepad++**, **VS Code** o **Poedit**:

```po
# locale/ca/LC_MESSAGES/django.po

#: templates/core/home.html:49
msgid "Calidad Garantizada"
msgstr "Qualitat Garantida"  ← TRADUCIR AQUÍ

#: templates/core/home.html:60
msgid "Pedir Presupuesto"
msgstr "Demanar Pressupost"  ← TRADUCIR AQUÍ
```

### **4.4 Copiar archivos .po editados de vuelta al contenedor**

```powershell
# Copiar de vuelta al contenedor
docker cp ./locale constructora_web:/app/

# O si locale está en src:
docker cp ./locale constructora_web:/app/src/
```

---

## 📝 PASO 5: Compilar Traducciones

```powershell
# Compilar archivos .po → .mo (binarios que Django lee)
docker exec constructora_web python src/manage.py compilemessages

# Verificar que se compilaron
docker exec constructora_web ls -la locale/ca/LC_MESSAGES/
docker exec constructora_web ls -la locale/en/LC_MESSAGES/
docker exec constructora_web ls -la locale/de/LC_MESSAGES/
```

**Deberías ver:**
- `django.po` (editable)
- `django.mo` (compilado)

---

## 🔄 PASO 6: Reiniciar Servicios

```powershell
# Reiniciar solo web (más rápido)
docker-compose restart web

# O reiniciar todo
docker-compose restart

# Ver logs para verificar
docker-compose logs -f web
```

---

## 🧪 PASO 7: Verificar que Funciona

### **7.1 Verificar admin con pestañas**

```powershell
# Abrir navegador
http://localhost/django-admin/

# O en producción
https://admin.rieraconstruccions.com/django-admin/
```

1. Login
2. Click en "Servicios"
3. Editar un servicio
4. **Deberías ver pestañas: [ES] [CA] [EN] [DE]**

### **7.2 Verificar selector de idioma**

```
http://localhost/
http://localhost/ca/
http://localhost/en/
http://localhost/de/
```

Verificar que el menú cambia de idioma.

---

## 📚 COMANDOS ÚTILES ADICIONALES

### **Ver estructura de archivos en contenedor**

```powershell
# Listar archivos en contenedor
docker exec constructora_web ls -la /app/

# Ver contenido de locale
docker exec constructora_web find /app -name "*.po"
```

### **Acceder al shell del contenedor**

```powershell
# Bash interactivo
docker exec -it constructora_web /bin/bash

# O sh si no tiene bash
docker exec -it constructora_web /bin/sh

# Dentro del contenedor puedes ejecutar:
cd src
python manage.py shell
>>> from services.models import Service
>>> Service.objects.all()
```

### **Ver logs en tiempo real**

```powershell
# Logs de web
docker-compose logs -f web

# Logs de nginx
docker-compose logs -f nginx

# Logs de todos
docker-compose logs -f
```

### **Limpiar cache de Django**

```powershell
docker exec constructora_web python src/manage.py shell -c "from django.core.cache import cache; cache.clear(); print('Cache cleared')"
```

### **Crear superusuario (si necesitas)**

```powershell
docker exec -it constructora_web python src/manage.py createsuperuser
```

---

## 🔥 SECUENCIA COMPLETA (Copy-Paste)

```powershell
# 1. Reconstruir con nuevas dependencias
docker-compose down
docker-compose build web
docker-compose up -d

# 2. Hacer migraciones
docker exec constructora_web python src/manage.py makemigrations
docker exec constructora_web python src/manage.py migrate

# 3. Migrar datos existentes
docker exec constructora_web python migrate_to_parler.py

# 4. Generar archivos de traducción
docker exec constructora_web sh -c "cd src && python manage.py makemessages -l ca && python manage.py makemessages -l en && python manage.py makemessages -l de"

# 5. Copiar .po para editar en local
docker cp constructora_web:/app/src/locale ./locale

# ⏸️  PAUSA: Edita los archivos .po en tu máquina

# 6. Copiar .po editados de vuelta
docker cp ./locale constructora_web:/app/src/

# 7. Compilar traducciones
docker exec constructora_web python src/manage.py compilemessages

# 8. Reiniciar
docker-compose restart web

# 9. Verificar logs
docker-compose logs -f web
```

---

## ⚠️ Troubleshooting

### **Error: "No module named 'parler'"**

```powershell
# Rebuild del contenedor
docker-compose build web --no-cache
docker-compose up -d
```

### **Error: Migraciones en conflicto**

```powershell
# Ver estado de migraciones
docker exec constructora_web python src/manage.py showmigrations

# Hacer fake de migraciones si es necesario
docker exec constructora_web python src/manage.py migrate --fake services 0001
docker exec constructora_web python src/manage.py migrate
```

### **Error: "Permission denied" al copiar archivos**

```powershell
# Ver permisos
docker exec constructora_web ls -la /app/

# Cambiar owner (si es necesario)
docker exec constructora_web chown -R app:app /app/locale
```

### **Los textos no cambian de idioma**

```powershell
# 1. Verificar que .mo existe
docker exec constructora_web ls -la src/locale/ca/LC_MESSAGES/

# 2. Recompilar
docker exec constructora_web python src/manage.py compilemessages

# 3. Limpiar cache
docker exec constructora_web python src/manage.py shell -c "from django.core.cache import cache; cache.clear()"

# 4. Reiniciar
docker-compose restart web
```

---

## 📊 Checklist de Verificación

```
[ ] requirements.txt tiene django-parler==2.3
[ ] docker-compose build web ejecutado
[ ] docker-compose up -d ejecutado
[ ] makemigrations ejecutado sin errores
[ ] migrate ejecutado sin errores
[ ] migrate_to_parler.py ejecutado
[ ] makemessages -l ca ejecutado
[ ] makemessages -l en ejecutado
[ ] makemessages -l de ejecutado
[ ] Archivos .po copiados y editados
[ ] Archivos .po copiados de vuelta al contenedor
[ ] compilemessages ejecutado
[ ] Contenedor reiniciado
[ ] Admin muestra pestañas [ES] [CA] [EN] [DE]
[ ] URLs /ca/, /en/, /de/ funcionan
[ ] Selector de idioma en menú funciona
```

---

## 🎯 Resumen Ejecutivo

**Para hacer migraciones en Docker:**
```powershell
docker exec constructora_web python src/manage.py makemigrations
docker exec constructora_web python src/manage.py migrate
```

**Para generar traducciones:**
```powershell
docker exec constructora_web sh -c "cd src && python manage.py makemessages -l ca"
docker cp constructora_web:/app/src/locale ./locale
# Editar .po en local
docker cp ./locale constructora_web:/app/src/
docker exec constructora_web python src/manage.py compilemessages
docker-compose restart web
```

---

¡Éxito con tu despliegue multiidioma! 🚀
