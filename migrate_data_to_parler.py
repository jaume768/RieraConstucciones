#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, '/app/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'constructora.settings')
django.setup()

from services.models import Service
from blog.models import Post, Category, Tag
from core.models import Page, TeamMember, CompanyValue

print("Iniciando migración de datos a español...")

# Migrar servicios
count = 0
for service in Service.objects.all():
    service.set_current_language('es', initialize=True)
    service.save()
    count += 1
print(f"✅ {count} servicios migrados")

# Migrar posts
count = 0
for post in Post.objects.all():
    post.set_current_language('es', initialize=True)
    post.save()
    count += 1
print(f"✅ {count} posts migrados")

# Migrar categorías
count = 0
for cat in Category.objects.all():
    cat.set_current_language('es', initialize=True)
    cat.save()
    count += 1
print(f"✅ {count} categorías migradas")

# Migrar tags
count = 0
for tag in Tag.objects.all():
    tag.set_current_language('es', initialize=True)
    tag.save()
    count += 1
print(f"✅ {count} tags migrados")

# Migrar páginas
count = 0
for page in Page.objects.all():
    page.set_current_language('es', initialize=True)
    page.save()
    count += 1
print(f"✅ {count} páginas migradas")

# Migrar miembros del equipo
count = 0
for member in TeamMember.objects.all():
    member.set_current_language('es', initialize=True)
    member.save()
    count += 1
print(f"✅ {count} miembros del equipo migrados")

# Migrar valores de la empresa
count = 0
for value in CompanyValue.objects.all():
    value.set_current_language('es', initialize=True)
    value.save()
    count += 1
print(f"✅ {count} valores de empresa migrados")

print("\n🎉 ¡Migración completada exitosamente!")
