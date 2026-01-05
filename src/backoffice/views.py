from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from blog.models import Post, Category, Tag
from services.models import Service
from core.models import TeamMember, CompanyValue, Page, ContactMessage

from .mixins import StaffRequiredMixin, BackofficePermissionMixin
from .forms import (
    PostForm, ServiceForm, TeamMemberForm, 
    CompanyValueForm, PageForm, CategoryForm, TagForm
)


# ============================================================
# AUTENTICACIÓN
# ============================================================

@csrf_protect
def login_view(request):
    """Vista de login personalizada para backoffice"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('backoffice:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            next_url = request.GET.get('next', 'backoffice:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos, o no tienes permisos de staff.')
    
    return render(request, 'backoffice/login.html')


@login_required
def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('backoffice:login')


# ============================================================
# DASHBOARD
# ============================================================

class DashboardView(StaffRequiredMixin, TemplateView):
    """Dashboard principal del backoffice"""
    template_name = 'backoffice/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas de posts
        context['posts_published'] = Post.objects.filter(is_published=True).count()
        context['posts_draft'] = Post.objects.filter(is_published=False).count()
        context['recent_posts'] = Post.objects.select_related('author', 'category').order_by('-updated_at')[:5]
        
        # Mensajes de contacto recientes (si existen)
        context['recent_messages'] = ContactMessage.objects.order_by('-created_at')[:5]
        context['unread_messages'] = ContactMessage.objects.filter(is_read=False).count()
        
        # Otras estadísticas
        context['services_count'] = Service.objects.filter(is_active=True).count()
        context['team_members_count'] = TeamMember.objects.filter(is_active=True).count()
        
        return context


# ============================================================
# POSTS DEL BLOG
# ============================================================

class PostListView(BackofficePermissionMixin, ListView):
    """Listado de posts con búsqueda y filtros"""
    model = Post
    template_name = 'backoffice/posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20
    permission_required = 'blog.view_post'
    
    def get_queryset(self):
        queryset = Post.objects.select_related('author', 'category').prefetch_related('tags')
        
        # Búsqueda por título
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(summary__icontains=search_query)
            )
        
        # Filtro por estado (publicado/borrador)
        status = self.request.GET.get('status', '')
        if status == 'published':
            queryset = queryset.filter(is_published=True)
        elif status == 'draft':
            queryset = queryset.filter(is_published=False)
        
        # Filtro por categoría
        category_id = self.request.GET.get('category', '')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['categories'] = Category.objects.all()
        return context


class PostCreateView(BackofficePermissionMixin, CreateView):
    """Crear nuevo post"""
    model = Post
    form_class = PostForm
    template_name = 'backoffice/posts/post_form.html'
    success_url = reverse_lazy('backoffice:post_list')
    permission_required = 'blog.add_post'
    
    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user
        return initial
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Post "{form.instance.title}" creado exitosamente.')
        return super().form_valid(form)


class PostUpdateView(BackofficePermissionMixin, UpdateView):
    """Editar post existente"""
    model = Post
    form_class = PostForm
    template_name = 'backoffice/posts/post_form.html'
    success_url = reverse_lazy('backoffice:post_list')
    permission_required = 'blog.change_post'
    
    def form_valid(self, form):
        messages.success(self.request, f'Post "{form.instance.title}" actualizado correctamente.')
        return super().form_valid(form)


class PostDeleteView(BackofficePermissionMixin, DeleteView):
    """Eliminar post"""
    model = Post
    template_name = 'backoffice/posts/post_confirm_delete.html'
    success_url = reverse_lazy('backoffice:post_list')
    permission_required = 'blog.delete_post'
    
    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        messages.success(request, f'Post "{post.title}" eliminado correctamente.')
        return super().delete(request, *args, **kwargs)


@require_POST
@login_required
def post_toggle_publish(request, pk):
    """Toggle publicado/borrador (HTMX o AJAX)"""
    if not request.user.has_perm('blog.change_post'):
        return JsonResponse({'error': 'Sin permisos'}, status=403)
    
    post = get_object_or_404(Post, pk=pk)
    post.is_published = not post.is_published
    post.save()
    
    status_text = 'publicado' if post.is_published else 'borrador'
    messages.success(request, f'Post "{post.title}" marcado como {status_text}.')
    
    return JsonResponse({
        'success': True,
        'is_published': post.is_published,
        'status_text': status_text
    })


# ============================================================
# SERVICIOS
# ============================================================

class ServiceListView(BackofficePermissionMixin, ListView):
    """Listado de servicios"""
    model = Service
    template_name = 'backoffice/services/service_list.html'
    context_object_name = 'services'
    permission_required = 'services.view_service'
    ordering = ['order']


class ServiceCreateView(BackofficePermissionMixin, CreateView):
    """Crear servicio"""
    model = Service
    form_class = ServiceForm
    template_name = 'backoffice/services/service_form.html'
    success_url = reverse_lazy('backoffice:service_list')
    permission_required = 'services.add_service'
    
    def form_valid(self, form):
        messages.success(self.request, f'Servicio "{form.instance.title}" creado exitosamente.')
        return super().form_valid(form)


class ServiceUpdateView(BackofficePermissionMixin, UpdateView):
    """Editar servicio"""
    model = Service
    form_class = ServiceForm
    template_name = 'backoffice/services/service_form.html'
    success_url = reverse_lazy('backoffice:service_list')
    permission_required = 'services.change_service'
    
    def form_valid(self, form):
        messages.success(self.request, f'Servicio "{form.instance.title}" actualizado correctamente.')
        return super().form_valid(form)


class ServiceDeleteView(BackofficePermissionMixin, DeleteView):
    """Eliminar servicio"""
    model = Service
    template_name = 'backoffice/services/service_confirm_delete.html'
    success_url = reverse_lazy('backoffice:service_list')
    permission_required = 'services.delete_service'
    
    def delete(self, request, *args, **kwargs):
        service = self.get_object()
        messages.success(request, f'Servicio "{service.title}" eliminado correctamente.')
        return super().delete(request, *args, **kwargs)


# ============================================================
# EQUIPO
# ============================================================

class TeamMemberListView(BackofficePermissionMixin, ListView):
    """Listado de miembros del equipo"""
    model = TeamMember
    template_name = 'backoffice/team/team_list.html'
    context_object_name = 'members'
    permission_required = 'core.view_teammember'
    ordering = ['order', 'name']


class TeamMemberCreateView(BackofficePermissionMixin, CreateView):
    """Crear miembro del equipo"""
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'backoffice/team/team_form.html'
    success_url = reverse_lazy('backoffice:team_list')
    permission_required = 'core.add_teammember'
    
    def form_valid(self, form):
        messages.success(self.request, f'Miembro "{form.instance.name}" agregado exitosamente.')
        return super().form_valid(form)


class TeamMemberUpdateView(BackofficePermissionMixin, UpdateView):
    """Editar miembro del equipo"""
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'backoffice/team/team_form.html'
    success_url = reverse_lazy('backoffice:team_list')
    permission_required = 'core.change_teammember'
    
    def form_valid(self, form):
        messages.success(self.request, f'Miembro "{form.instance.name}" actualizado correctamente.')
        return super().form_valid(form)


class TeamMemberDeleteView(BackofficePermissionMixin, DeleteView):
    """Eliminar miembro del equipo"""
    model = TeamMember
    template_name = 'backoffice/team/team_confirm_delete.html'
    success_url = reverse_lazy('backoffice:team_list')
    permission_required = 'core.delete_teammember'
    
    def delete(self, request, *args, **kwargs):
        member = self.get_object()
        messages.success(request, f'Miembro "{member.name}" eliminado correctamente.')
        return super().delete(request, *args, **kwargs)


# ============================================================
# VALORES DE LA EMPRESA
# ============================================================

class CompanyValueListView(BackofficePermissionMixin, ListView):
    """Listado de valores de la empresa"""
    model = CompanyValue
    template_name = 'backoffice/values/value_list.html'
    context_object_name = 'values'
    permission_required = 'core.view_companyvalue'
    ordering = ['order']


class CompanyValueCreateView(BackofficePermissionMixin, CreateView):
    """Crear valor"""
    model = CompanyValue
    form_class = CompanyValueForm
    template_name = 'backoffice/values/value_form.html'
    success_url = reverse_lazy('backoffice:value_list')
    permission_required = 'core.add_companyvalue'
    
    def form_valid(self, form):
        messages.success(self.request, f'Valor "{form.instance.title}" creado exitosamente.')
        return super().form_valid(form)


class CompanyValueUpdateView(BackofficePermissionMixin, UpdateView):
    """Editar valor"""
    model = CompanyValue
    form_class = CompanyValueForm
    template_name = 'backoffice/values/value_form.html'
    success_url = reverse_lazy('backoffice:value_list')
    permission_required = 'core.change_companyvalue'
    
    def form_valid(self, form):
        messages.success(self.request, f'Valor "{form.instance.title}" actualizado correctamente.')
        return super().form_valid(form)


class CompanyValueDeleteView(BackofficePermissionMixin, DeleteView):
    """Eliminar valor"""
    model = CompanyValue
    template_name = 'backoffice/values/value_confirm_delete.html'
    success_url = reverse_lazy('backoffice:value_list')
    permission_required = 'core.delete_companyvalue'
    
    def delete(self, request, *args, **kwargs):
        value = self.get_object()
        messages.success(request, f'Valor "{value.title}" eliminado correctamente.')
        return super().delete(request, *args, **kwargs)


# ============================================================
# PÁGINAS ESTÁTICAS
# ============================================================

class PageListView(BackofficePermissionMixin, ListView):
    """Listado de páginas estáticas"""
    model = Page
    template_name = 'backoffice/pages/page_list.html'
    context_object_name = 'pages'
    permission_required = 'core.view_page'
    ordering = ['slug']


class PageUpdateView(BackofficePermissionMixin, UpdateView):
    """Editar página estática"""
    model = Page
    form_class = PageForm
    template_name = 'backoffice/pages/page_form.html'
    success_url = reverse_lazy('backoffice:page_list')
    permission_required = 'core.change_page'
    
    def form_valid(self, form):
        messages.success(self.request, f'Página "{form.instance.title}" actualizada correctamente.')
        return super().form_valid(form)


# ============================================================
# MENSAJES DE CONTACTO
# ============================================================

class ContactMessageListView(BackofficePermissionMixin, ListView):
    """Listado de mensajes de contacto"""
    model = ContactMessage
    template_name = 'backoffice/contact/message_list.html'
    context_object_name = 'messages_list'
    permission_required = 'core.view_contactmessage'
    paginate_by = 20
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por leído/no leído
        status = self.request.GET.get('status', '')
        if status == 'unread':
            queryset = queryset.filter(is_read=False)
        elif status == 'read':
            queryset = queryset.filter(is_read=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', '')
        context['unread_count'] = ContactMessage.objects.filter(is_read=False).count()
        return context


@require_POST
@login_required
def contact_message_toggle_read(request, pk):
    """Marcar mensaje como leído/no leído"""
    if not request.user.has_perm('core.change_contactmessage'):
        return JsonResponse({'error': 'Sin permisos'}, status=403)
    
    message = get_object_or_404(ContactMessage, pk=pk)
    message.is_read = not message.is_read
    message.save()
    
    status_text = 'leído' if message.is_read else 'no leído'
    messages.success(request, f'Mensaje marcado como {status_text}.')
    
    return JsonResponse({
        'success': True,
        'is_read': message.is_read,
        'status_text': status_text
    })


# ============================================================
# CATEGORÍAS DEL BLOG
# ============================================================

class CategoryListView(BackofficePermissionMixin, ListView):
    """Listado de categorías del blog"""
    model = Category
    template_name = 'backoffice/categories/category_list.html'
    context_object_name = 'categories'
    permission_required = 'blog.view_category'
    
    def get_queryset(self):
        return Category.objects.annotate(
            post_count=Count('posts')
        ).order_by('slug')


class CategoryCreateView(BackofficePermissionMixin, CreateView):
    """Crear categoría"""
    model = Category
    form_class = CategoryForm
    template_name = 'backoffice/categories/category_form.html'
    success_url = reverse_lazy('backoffice:category_list')
    permission_required = 'blog.add_category'
    
    def form_valid(self, form):
        messages.success(self.request, f'Categoría "{form.instance.name}" creada correctamente.')
        return super().form_valid(form)


class CategoryUpdateView(BackofficePermissionMixin, UpdateView):
    """Editar categoría"""
    model = Category
    form_class = CategoryForm
    template_name = 'backoffice/categories/category_form.html'
    success_url = reverse_lazy('backoffice:category_list')
    permission_required = 'blog.change_category'
    
    def form_valid(self, form):
        messages.success(self.request, f'Categoría "{form.instance.name}" actualizada correctamente.')
        return super().form_valid(form)


class CategoryDeleteView(BackofficePermissionMixin, DeleteView):
    """Eliminar categoría"""
    model = Category
    template_name = 'backoffice/categories/category_confirm_delete.html'
    success_url = reverse_lazy('backoffice:category_list')
    permission_required = 'blog.delete_category'
    
    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        messages.success(request, f'Categoría "{category.name}" eliminada correctamente.')
        return super().delete(request, *args, **kwargs)


# ============================================================
# ETIQUETAS DEL BLOG
# ============================================================

class TagListView(BackofficePermissionMixin, ListView):
    """Listado de etiquetas del blog"""
    model = Tag
    template_name = 'backoffice/tags/tag_list.html'
    context_object_name = 'tags'
    permission_required = 'blog.view_tag'
    
    def get_queryset(self):
        return Tag.objects.annotate(
            post_count=Count('posts')
        ).order_by('slug')


class TagCreateView(BackofficePermissionMixin, CreateView):
    """Crear etiqueta"""
    model = Tag
    form_class = TagForm
    template_name = 'backoffice/tags/tag_form.html'
    success_url = reverse_lazy('backoffice:tag_list')
    permission_required = 'blog.add_tag'
    
    def form_valid(self, form):
        messages.success(self.request, f'Etiqueta "{form.instance.name}" creada correctamente.')
        return super().form_valid(form)


class TagUpdateView(BackofficePermissionMixin, UpdateView):
    """Editar etiqueta"""
    model = Tag
    form_class = TagForm
    template_name = 'backoffice/tags/tag_form.html'
    success_url = reverse_lazy('backoffice:tag_list')
    permission_required = 'blog.change_tag'
    
    def form_valid(self, form):
        messages.success(self.request, f'Etiqueta "{form.instance.name}" actualizada correctamente.')
        return super().form_valid(form)


class TagDeleteView(BackofficePermissionMixin, DeleteView):
    """Eliminar etiqueta"""
    model = Tag
    template_name = 'backoffice/tags/tag_confirm_delete.html'
    success_url = reverse_lazy('backoffice:tag_list')
    permission_required = 'blog.delete_tag'
    
    def delete(self, request, *args, **kwargs):
        tag = self.get_object()
        messages.success(request, f'Etiqueta "{tag.name}" eliminada correctamente.')
        return super().delete(request, *args, **kwargs)
