from django.db import models
from django.utils.text import slugify
from parler.models import TranslatableModel, TranslatedFields
from ckeditor.fields import RichTextField


class Page(TranslatableModel):
    slug = models.SlugField('Slug', max_length=200, unique=True)
    og_image = models.ImageField('Imagen Open Graph', upload_to='og_images/', blank=True, null=True)
    is_published = models.BooleanField('Publicado', default=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    
    translations = TranslatedFields(
        title=models.CharField('Título', max_length=200),
        content=RichTextField('Contenido'),
        meta_title=models.CharField('Meta Title (SEO)', max_length=70, blank=True),
        meta_description=models.TextField('Meta Description (SEO)', max_length=160, blank=True),
    )
    
    class Meta:
        verbose_name = 'Página'
        verbose_name_plural = 'Páginas'
    
    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or f'Page {self.pk}'
    
    def get_meta_title(self):
        meta = self.safe_translation_getter('meta_title', any_language=False)
        if meta:
            return meta
        return self.safe_translation_getter('title', any_language=True)
    
    def get_meta_description(self):
        meta = self.safe_translation_getter('meta_description', any_language=False)
        if meta:
            return meta
        content = self.safe_translation_getter('content', any_language=True)
        return content[:160] if content else ''
    
    def save(self, *args, **kwargs):
        if not self.slug and self.has_translation():
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class TeamMember(TranslatableModel):
    name = models.CharField('Nombre completo', max_length=200)
    photo = models.ImageField('Foto', upload_to='team/', blank=True, null=True)
    email = models.EmailField('Email', blank=True)
    linkedin = models.URLField('LinkedIn', blank=True)
    order = models.PositiveIntegerField('Orden', default=0, help_text='Orden de visualización en la página')
    is_active = models.BooleanField('Activo', default=True)
    
    translations = TranslatedFields(
        position=models.CharField('Cargo/Posición', max_length=200),
        bio=models.TextField('Biografía', blank=True),
    )
    
    class Meta:
        verbose_name = 'Miembro del Equipo'
        verbose_name_plural = 'Equipo'
        ordering = ['order', 'name']
    
    def __str__(self):
        position = self.safe_translation_getter('position', any_language=True)
        return f"{self.name} - {position}" if position else self.name


class CompanyValue(TranslatableModel):
    icon = models.CharField('Icono CSS', max_length=100, blank=True, help_text='Clase CSS del icono (ej: fa-solid fa-heart)')
    order = models.PositiveIntegerField('Orden', default=0)
    is_active = models.BooleanField('Activo', default=True)
    
    translations = TranslatedFields(
        title=models.CharField('Título', max_length=200),
        description=models.TextField('Descripción'),
    )
    
    class Meta:
        verbose_name = 'Valor de la Empresa'
        verbose_name_plural = 'Valores de la Empresa'
        ordering = ['order']
    
    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or f'Value {self.pk}'


class ContactMessage(models.Model):
    name = models.CharField('Nombre', max_length=200)
    email = models.EmailField('Email')
    phone = models.CharField('Teléfono', max_length=20, blank=True)
    message = models.TextField('Mensaje')
    created_at = models.DateTimeField('Fecha de envío', auto_now_add=True)
    is_read = models.BooleanField('Leído', default=False)
    
    class Meta:
        verbose_name = 'Mensaje de Contacto'
        verbose_name_plural = 'Mensajes de Contacto'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%d/%m/%Y')}"
