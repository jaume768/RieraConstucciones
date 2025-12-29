from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.cache import cache_page
from .models import Page, TeamMember, CompanyValue, ContactMessage
from blog.models import Post
from services.models import Service


@cache_page(60 * 15)
def home_view(request):
    latest_posts = Post.objects.filter(is_published=True).order_by('-published_at')[:4]
    services = Service.objects.filter(is_active=True).order_by('order')[:6]
    
    context = {
        'meta_title': f'{settings.SITE_NAME} - Construcción y Reformas de Calidad',
        'meta_description': 'Empresa constructora especializada en obra nueva, reformas y rehabilitaciones. Más de 20 años de experiencia en el sector.',
        'latest_posts': latest_posts,
        'services': services,
    }
    return render(request, 'core/home.html', context)


@cache_page(60 * 15)
def about_view(request):
    team_members = TeamMember.objects.filter(is_active=True)
    company_values = CompanyValue.objects.filter(is_active=True)
    
    try:
        page = Page.objects.get(slug='sobre-nosotros', is_published=True)
        meta_title = page.get_meta_title()
        meta_description = page.get_meta_description()
        content = page.content
    except Page.DoesNotExist:
        page = None
        meta_title = f'Sobre Nosotros - {settings.SITE_NAME}'
        meta_description = 'Conoce nuestro equipo y valores. Somos una empresa constructora comprometida con la calidad y la satisfacción del cliente.'
        content = ''
    
    context = {
        'page': page,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'team_members': team_members,
        'company_values': company_values,
        'content': content,
    }
    return render(request, 'core/about.html', context)


def contact_view(request):
    if request.method == 'POST':
        honeypot = request.POST.get('website', '')
        
        if honeypot:
            messages.error(request, 'Detectamos actividad sospechosa. Por favor, intenta de nuevo.')
            return redirect('contact')
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message')
        
        if not all([name, email, message]):
            messages.error(request, 'Por favor, completa todos los campos obligatorios.')
            return redirect('contact')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        
        subject = f'Nuevo mensaje de contacto de {name}'
        email_message = f'''
        Nombre: {name}
        Email: {email}
        Teléfono: {phone}
        
        Mensaje:
        {message}
        '''
        
        try:
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error enviando email: {e}")
        
        messages.success(request, '¡Gracias por contactarnos! Te responderemos lo antes posible.')
        return redirect('contact')
    
    context = {
        'meta_title': f'Contacto - {settings.SITE_NAME}',
        'meta_description': 'Contacta con nosotros para cualquier consulta o presupuesto sin compromiso. Estamos aquí para ayudarte.',
    }
    return render(request, 'core/contact.html', context)
