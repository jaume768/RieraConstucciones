from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.conf import settings
from .models import Service


@cache_page(60 * 15)
def services_list_view(request):
    services = Service.objects.filter(is_active=True)
    
    context = {
        'meta_title': f'Servicios - {settings.SITE_NAME}',
        'meta_description': 'Descubre todos nuestros servicios de construcción: obra nueva, reformas, rehabilitaciones y más.',
        'services': services,
    }
    return render(request, 'services/services_list.html', context)


def service_detail_view(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    other_services = Service.objects.filter(is_active=True).exclude(slug=slug)[:3]
    
    context = {
        'meta_title': service.get_meta_title(),
        'meta_description': service.get_meta_description(),
        'service': service,
        'other_services': other_services,
        'og_image': service.image.url if service.image else None,
    }
    return render(request, 'services/service_detail.html', context)
