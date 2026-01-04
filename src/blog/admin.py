from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    search_fields = ['translations__name']
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    search_fields = ['translations__name']
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(TranslatableAdmin):
    list_display = ['title', 'category', 'author', 'is_published', 'is_featured', 'published_at', 'views']
    list_filter = ['is_published', 'is_featured', 'category', 'created_at', 'published_at']
    search_fields = ['translations__title', 'translations__summary']
    filter_horizontal = ['tags']
    list_editable = ['is_published', 'is_featured']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Contenido Principal', {
            'fields': ('title', 'slug', 'summary', 'content', 'featured_image')
        }),
        ('Clasificación', {
            'fields': ('category', 'tags', 'author')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Publicación', {
            'fields': ('is_published', 'is_featured', 'published_at')
        }),
        ('Estadísticas', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
    )
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
