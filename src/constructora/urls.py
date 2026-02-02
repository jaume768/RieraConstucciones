from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from .sitemaps import PageSitemap, PostSitemap, ServiceSitemap

sitemaps = {
    'pages': PageSitemap,
    'posts': PostSitemap,
    'services': ServiceSitemap,
}

# URLs sin prefijo de idioma (admin, backoffice, sitemap, robots, i18n)
urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('backoffice/', include('backoffice.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_txt'),
]

# URLs con prefijo de idioma (/es/, /ca/, /en/, /de/)
urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('servicios/', include('services.urls')),
    path('propiedades/', include('properties.urls')),
    prefix_default_language=False,  # No agregar /es/ en español
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
