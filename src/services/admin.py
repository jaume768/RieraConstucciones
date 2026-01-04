from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Service


@admin.register(Service)
class ServiceAdmin(TranslatableAdmin):
    list_display = ['title', 'order', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['translations__title', 'translations__short_description']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Contenido Principal', {
            'fields': ('title', 'slug', 'short_description', 'description', 'icon', 'image')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Configuración', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}
