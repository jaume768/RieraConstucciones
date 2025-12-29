from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Service(models.Model):
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField('Slug', max_length=200, unique=True)
    short_description = models.TextField('Descripción corta', max_length=200, help_text='Para el listado de servicios')
    description = RichTextField('Descripción completa')
    icon = models.CharField('Icono CSS', max_length=100, blank=True, help_text='Clase CSS del icono (ej: fa-solid fa-hammer)')
    image = models.ImageField('Imagen', upload_to='services/', blank=True, null=True)
    
    meta_title = models.CharField('Meta Title (SEO)', max_length=70, blank=True)
    meta_description = models.TextField('Meta Description (SEO)', max_length=160, blank=True)
    
    order = models.PositiveIntegerField('Orden', default=0, help_text='Orden de visualización')
    is_active = models.BooleanField('Activo', default=True)
    
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def get_meta_title(self):
        return self.meta_title if self.meta_title else self.title
    
    def get_meta_description(self):
        if self.meta_description:
            return self.meta_description
        return self.short_description
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
