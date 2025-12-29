from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Page(models.Model):
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField('Slug', max_length=200, unique=True)
    content = RichTextField('Contenido')
    meta_title = models.CharField('Meta Title (SEO)', max_length=70, blank=True, help_text='Si está vacío, se usará el título de la página')
    meta_description = models.TextField('Meta Description (SEO)', max_length=160, blank=True, help_text='Si está vacío, se usará un extracto del contenido')
    og_image = models.ImageField('Imagen Open Graph', upload_to='og_images/', blank=True, null=True)
    is_published = models.BooleanField('Publicado', default=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Página'
        verbose_name_plural = 'Páginas'
        ordering = ['title']
    
    def __str__(self):
        return self.title
    
    def get_meta_title(self):
        return self.meta_title if self.meta_title else self.title
    
    def get_meta_description(self):
        if self.meta_description:
            return self.meta_description
        return self.content[:160] if self.content else ''
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class TeamMember(models.Model):
    name = models.CharField('Nombre completo', max_length=200)
    position = models.CharField('Cargo/Posición', max_length=200)
    photo = models.ImageField('Foto', upload_to='team/', blank=True, null=True)
    bio = models.TextField('Biografía', blank=True)
    email = models.EmailField('Email', blank=True)
    linkedin = models.URLField('LinkedIn', blank=True)
    order = models.PositiveIntegerField('Orden', default=0, help_text='Orden de visualización en la página')
    is_active = models.BooleanField('Activo', default=True)
    
    class Meta:
        verbose_name = 'Miembro del Equipo'
        verbose_name_plural = 'Equipo'
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class CompanyValue(models.Model):
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción')
    icon = models.CharField('Icono CSS', max_length=100, blank=True, help_text='Clase CSS del icono (ej: fa-solid fa-heart)')
    order = models.PositiveIntegerField('Orden', default=0)
    is_active = models.BooleanField('Activo', default=True)
    
    class Meta:
        verbose_name = 'Valor de la Empresa'
        verbose_name_plural = 'Valores de la Empresa'
        ordering = ['order']
    
    def __str__(self):
        return self.title


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
