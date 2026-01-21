from django.urls import path
from . import views

app_name = 'backoffice'

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.DashboardView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Posts del Blog
    path('blog/posts/', views.PostListView.as_view(), name='post_list'),
    path('blog/posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('blog/posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('blog/posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('blog/posts/<int:pk>/toggle-publish/', views.post_toggle_publish, name='post_toggle_publish'),
    
    # Servicios
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='service_edit'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),
    
    # Equipo
    path('team/', views.TeamMemberListView.as_view(), name='team_list'),
    path('team/create/', views.TeamMemberCreateView.as_view(), name='team_create'),
    path('team/<int:pk>/edit/', views.TeamMemberUpdateView.as_view(), name='team_edit'),
    path('team/<int:pk>/delete/', views.TeamMemberDeleteView.as_view(), name='team_delete'),
    
    # Valores
    path('values/', views.CompanyValueListView.as_view(), name='value_list'),
    path('values/create/', views.CompanyValueCreateView.as_view(), name='value_create'),
    path('values/<int:pk>/edit/', views.CompanyValueUpdateView.as_view(), name='value_edit'),
    path('values/<int:pk>/delete/', views.CompanyValueDeleteView.as_view(), name='value_delete'),
    
    # Páginas
    path('pages/', views.PageListView.as_view(), name='page_list'),
    path('pages/<int:pk>/edit/', views.PageUpdateView.as_view(), name='page_edit'),
    
    # Mensajes de contacto
    path('contact/messages/', views.ContactMessageListView.as_view(), name='contact_message_list'),
    path('contact/messages/<int:pk>/toggle-read/', views.contact_message_toggle_read, name='contact_message_toggle_read'),
    path('contact/messages/<int:pk>/delete/', views.contact_message_delete, name='contact_message_delete'),
    
    # Categorías del blog
    path('blog/categories/', views.CategoryListView.as_view(), name='category_list'),
    path('blog/categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('blog/categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('blog/categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # Etiquetas del blog
    path('blog/tags/', views.TagListView.as_view(), name='tag_list'),
    path('blog/tags/create/', views.TagCreateView.as_view(), name='tag_create'),
    path('blog/tags/<int:pk>/edit/', views.TagUpdateView.as_view(), name='tag_edit'),
    path('blog/tags/<int:pk>/delete/', views.TagDeleteView.as_view(), name='tag_delete'),
]
