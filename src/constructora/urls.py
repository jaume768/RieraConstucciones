from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from .sitemaps import PageSitemap, PostSitemap, ServiceSitemap

sitemaps = {
    'pages': PageSitemap,
    'posts': PostSitemap,
    'services': ServiceSitemap,
}

urlpatterns = [
    path('django-admin/', admin.site.urls),
    
    path('backoffice/', include('backoffice.urls')),
    
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('servicios/', include('services.urls')),
    
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_txt'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
