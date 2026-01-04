from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Page, TeamMember, CompanyValue, ContactMessage


@admin.register(Page)
class PageAdmin(TranslatableAdmin):
    list_display = ['title', 'slug', 'is_published', 'updated_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['translations__title', 'translations__content']
    
    fieldsets = (
        ('Contenido Principal', {
            'fields': ('title', 'slug', 'content', 'is_published')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'og_image'),
            'classes': ('collapse',)
        }),
    )
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}


@admin.register(TeamMember)
class TeamMemberAdmin(TranslatableAdmin):
    list_display = ['name', 'position', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'translations__position']
    list_editable = ['order']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'position', 'photo', 'bio')
        }),
        ('Contacto y Redes', {
            'fields': ('email', 'linkedin')
        }),
        ('Configuración', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(CompanyValue)
class CompanyValueAdmin(TranslatableAdmin):
    list_display = ['title', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['translations__title', 'translations__description']
    list_editable = ['order']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['name', 'email', 'phone', 'message', 'created_at']
    list_editable = ['is_read']
    
    def has_add_permission(self, request):
        return False
