from django.db import models
from django.utils.text import slugify
from parler.models import TranslatableModel, TranslatedFields
from ckeditor_uploader.fields import RichTextUploadingField


class Service(TranslatableModel):
    # Campos NO traducibles (comunes a todos los idiomas)
    slug = models.SlugField('Slug', max_length=200, unique=True)
    icon = models.CharField('Icono CSS', max_length=100, blank=True, help_text='Clase CSS del icono (ej: fa-solid fa-hammer)')
    image = models.ImageField('Imagen', upload_to='services/', blank=True, null=True)
    order = models.PositiveIntegerField('Orden', default=0, help_text='Orden de visualización')
    is_active = models.BooleanField('Activo', default=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    
    # Campos TRADUCIBLES (uno por cada idioma)
    translations = TranslatedFields(
        title=models.CharField('Título', max_length=200),
        short_description=models.TextField('Descripción corta', max_length=200, help_text='Para el listado de servicios'),
        description=RichTextUploadingField('Descripción completa'),
        meta_title=models.CharField('Meta Title (SEO)', max_length=70, blank=True),
        meta_description=models.TextField('Meta Description (SEO)', max_length=160, blank=True),
    )
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['order']
    
    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or f'Service {self.pk}'
    
    def get_meta_title(self):
        meta = self.safe_translation_getter('meta_title', any_language=False)
        if meta:
            return meta
        return self.safe_translation_getter('title', any_language=True)
    
    def get_meta_description(self):
        meta = self.safe_translation_getter('meta_description', any_language=False)
        if meta:
            return meta
        return self.safe_translation_getter('short_description', any_language=True)
    
    def save(self, *args, **kwargs):
        if not self.slug and self.has_translation():
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
