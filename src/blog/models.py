from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField('Nombre', max_length=100)
    slug = models.SlugField('Slug', max_length=100, unique=True)
    description = models.TextField('Descripción', blank=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField('Nombre', max_length=50)
    slug = models.SlugField('Slug', max_length=50, unique=True)
    
    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField('Título', max_length=200)
    slug = models.SlugField('Slug', max_length=200, unique=True)
    summary = models.TextField('Resumen', max_length=300, help_text='Breve descripción para listados')
    content = RichTextField('Contenido')
    featured_image = models.ImageField('Imagen destacada', upload_to='blog/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Autor')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Categoría', related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Etiquetas', related_name='posts')
    
    meta_title = models.CharField('Meta Title (SEO)', max_length=70, blank=True, help_text='Si está vacío, se usará el título del post')
    meta_description = models.TextField('Meta Description (SEO)', max_length=160, blank=True, help_text='Si está vacío, se usará el resumen')
    
    is_published = models.BooleanField('Publicado', default=False)
    is_featured = models.BooleanField('Destacado', default=False, help_text='Aparecerá en la página principal')
    
    published_at = models.DateTimeField('Fecha de publicación', null=True, blank=True)
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    
    views = models.PositiveIntegerField('Visitas', default=0)
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_meta_title(self):
        return self.meta_title if self.meta_title else self.title
    
    def get_meta_description(self):
        if self.meta_description:
            return self.meta_description
        return self.summary if self.summary else self.content[:160]
    
    def get_related_posts(self, limit=3):
        related = Post.objects.filter(
            is_published=True,
            category=self.category
        ).exclude(id=self.id).order_by('-published_at')[:limit]
        
        if related.count() < limit:
            additional = Post.objects.filter(
                is_published=True
            ).exclude(id=self.id).exclude(
                id__in=[p.id for p in related]
            ).order_by('-published_at')[:limit - related.count()]
            related = list(related) + list(additional)
        
        return related
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        if self.is_published and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
