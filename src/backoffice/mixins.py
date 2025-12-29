from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages


class StaffRequiredMixin(LoginRequiredMixin):
    """
    Requiere que el usuario sea staff (is_staff=True).
    Si no lo es, redirige al login con mensaje de error.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if not request.user.is_staff:
            messages.error(request, 'No tienes permisos para acceder al backoffice.')
            return redirect('backoffice:login')
        
        return super().dispatch(request, *args, **kwargs)


class BackofficePermissionMixin(StaffRequiredMixin, PermissionRequiredMixin):
    """
    Combina StaffRequired con PermissionRequired.
    Uso: permission_required = 'blog.add_post'
    """
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        
        messages.error(
            self.request, 
            'No tienes los permisos necesarios para realizar esta acción.'
        )
        return redirect('backoffice:dashboard')
