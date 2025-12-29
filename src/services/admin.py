from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'short_description', 'description']
    prepopulated_fields = {'slug': ('title',)}
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
