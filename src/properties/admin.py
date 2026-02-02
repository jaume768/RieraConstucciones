from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ['image', 'order', 'is_primary']


@admin.register(Property)
class PropertyAdmin(TranslatableAdmin):
    list_display = ['get_title', 'property_type', 'price', 'location', 'bedrooms', 'bathrooms', 'is_sold', 'is_featured', 'updated_at']
    list_filter = ['property_type', 'is_sold', 'is_featured', 'location', 'bedrooms']
    search_fields = ['translations__title', 'translations__short_description', 'location']
    list_editable = ['is_featured', 'is_sold']
    inlines = [PropertyImageInline]
    
    fieldsets = (
        ('Contenido', {
            'fields': ('title', 'slug', 'short_description', 'description', 'features')
        }),
        ('Características Técnicas', {
            'fields': ('property_type', 'price', 'surface_area', 'bedrooms', 'bathrooms')
        }),
        ('Ubicación', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Publicación', {
            'fields': ('is_sold', 'is_featured')
        }),
    )
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}
    
    def get_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True) or f'Propiedad {obj.pk}'
    get_title.short_description = 'Título'


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'image', 'order', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    list_editable = ['order', 'is_primary']
    search_fields = ['property__translations__title']
