from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('sobre-nosotros/', views.about_view, name='about'),
    path('contacto/', views.contact_view, name='contact'),
]
