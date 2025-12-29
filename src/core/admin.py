from django.contrib import admin
from .models import Page, TeamMember, CompanyValue, ContactMessage


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_published', 'updated_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Contenido Principal', {
            'fields': ('title', 'slug', 'content', 'is_published')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'og_image'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'position']
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
class CompanyValueAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
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
