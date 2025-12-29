from django.urls import path
from . import views

urlpatterns = [
    path('', views.services_list_view, name='services_list'),
    path('<slug:slug>/', views.service_detail_view, name='service_detail'),
]
