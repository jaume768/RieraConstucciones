from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from parler.models import TranslatableModel, TranslatedFields
from ckeditor_uploader.fields import RichTextUploadingField


class Property(TranslatableModel):
    PROPERTY_TYPE_CHOICES = [
        ('casa', 'Casa'),
        ('piso', 'Piso'),
        ('apartamento', 'Apartamento'),
        ('local', 'Local Comercial'),
        ('terreno', 'Terreno'),
    ]
    
    slug = models.SlugField('Slug', max_length=200, unique=True)
    property_type = models.CharField('Tipo de propiedad', max_length=20, choices=PROPERTY_TYPE_CHOICES, default='casa')
    price = models.DecimalField('Precio', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    surface_area = models.PositiveIntegerField('Superficie (m²)')
    bedrooms = models.PositiveIntegerField('Habitaciones', default=0)
    bathrooms = models.PositiveIntegerField('Baños', default=0)
    location = models.CharField('Ubicación', max_length=200, help_text='Ciudad o zona (ej: Palma de Mallorca)')
    latitude = models.DecimalField('Latitud', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField('Longitud', max_digits=9, decimal_places=6, null=True, blank=True)
    is_sold = models.BooleanField('Vendido', default=False)
    is_featured = models.BooleanField('Destacado', default=False, help_text='Aparecerá en la página principal')
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    
    translations = TranslatedFields(
        title=models.CharField('Título', max_length=200),
        description=RichTextUploadingField('Descripción completa'),
        short_description=models.TextField('Resumen', max_length=300, help_text='Descripción breve para listados'),
        features=models.TextField('Características', blank=True, help_text='Piscina, garaje, terraza, etc. (una por línea)'),
        meta_title=models.CharField('Meta Title (SEO)', max_length=70, blank=True),
        meta_description=models.TextField('Meta Description (SEO)', max_length=160, blank=True),
    )
    
    class Meta:
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or f'Propiedad {self.pk}'
    
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
    
    def get_primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        return self.images.first()
    
    def get_features_list(self):
        features = self.safe_translation_getter('features', any_language=True)
        if features:
            return [f.strip() for f in features.split('\n') if f.strip()]
        return []
    
    def clean(self):
        if self.latitude and (self.latitude < -90 or self.latitude > 90):
            raise ValidationError({'latitude': 'Latitud inválida (debe estar entre -90 y 90)'})
        if self.longitude and (self.longitude < -180 or self.longitude > 180):
            raise ValidationError({'longitude': 'Longitud inválida (debe estar entre -180 y 180)'})
    
    def save(self, *args, **kwargs):
        if not self.slug and self.has_translation():
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images', verbose_name='Propiedad')
    image = models.ImageField('Imagen', upload_to='properties/')
    order = models.PositiveIntegerField('Orden', default=0)
    is_primary = models.BooleanField('Imagen principal', default=False)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Imagen de Propiedad'
        verbose_name_plural = 'Imágenes de Propiedades'
        ordering = ['order', '-is_primary']
    
    def __str__(self):
        return f'Imagen de {self.property}'
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            PropertyImage.objects.filter(property=self.property, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
