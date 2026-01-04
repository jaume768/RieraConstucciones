"""
Script para migrar datos existentes a django-parler.
Ejecutar DESPUÉS de hacer las migraciones:
    python manage.py makemigrations
    python manage.py migrate
    python src/manage.py shell < migrate_to_parler.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'constructora.settings')
django.setup()

from services.models import Service
from blog.models import Post, Category, Tag
from core.models import Page, TeamMember, CompanyValue

def migrate_services():
    print("Migrando servicios...")
    # Los datos ya están en la tabla principal
    # django-parler los moverá automáticamente a las tablas de traducción
    # Solo necesitamos asegurar que cada registro tenga al menos una traducción en español
    for service in Service.objects.all():
        if not service.has_translation('es'):
            print(f"  - Creando traducción ES para: {service.slug}")
            service.set_current_language('es')
            service.save()
    print(f"✓ {Service.objects.count()} servicios migrados")

def migrate_blog():
    print("Migrando blog...")
    for category in Category.objects.all():
        if not category.has_translation('es'):
            print(f"  - Creando traducción ES para categoría: {category.slug}")
            category.set_current_language('es')
            category.save()
    
    for tag in Tag.objects.all():
        if not tag.has_translation('es'):
            print(f"  - Creando traducción ES para tag: {tag.slug}")
            tag.set_current_language('es')
            tag.save()
    
    for post in Post.objects.all():
        if not post.has_translation('es'):
            print(f"  - Creando traducción ES para post: {post.slug}")
            post.set_current_language('es')
            post.save()
    
    print(f"✓ {Category.objects.count()} categorías, {Tag.objects.count()} tags, {Post.objects.count()} posts migrados")

def migrate_core():
    print("Migrando core...")
    for page in Page.objects.all():
        if not page.has_translation('es'):
            print(f"  - Creando traducción ES para página: {page.slug}")
            page.set_current_language('es')
            page.save()
    
    for member in TeamMember.objects.all():
        if not member.has_translation('es'):
            print(f"  - Creando traducción ES para miembro: {member.name}")
            member.set_current_language('es')
            member.save()
    
    for value in CompanyValue.objects.all():
        if not value.has_translation('es'):
            print(f"  - Creando traducción ES para valor")
            value.set_current_language('es')
            value.save()
    
    print(f"✓ {Page.objects.count()} páginas, {TeamMember.objects.count()} miembros, {CompanyValue.objects.count()} valores migrados")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("MIGRACIÓN DE DATOS A DJANGO-PARLER")
    print("="*60 + "\n")
    
    try:
        migrate_services()
        migrate_blog()
        migrate_core()
        
        print("\n" + "="*60)
        print("✓ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("="*60 + "\n")
        print("Próximos pasos:")
        print("1. Ir al admin de Django")
        print("2. Editar cada servicio/post/página")
        print("3. Click en las pestañas [CA] [EN] [DE] para agregar traducciones")
        print("\n")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
