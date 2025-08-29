from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class RolRequeridoMixin(UserPassesTestMixin):
    """
    Mixins para restringir el acceso a la vista a usuarios con roles específicos.
    """
    rol_requerido = None
    redirect_url = reverse_lazy("accounts:login")

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False

        roles = self.rol_requerido
        if isinstance(roles, str):
            roles = [roles]

        return user.groups.filter(name__in=roles).exists()

    def handle_no_permission(self):
        return redirect(self.redirect_url)


class PermisosDatosMixin:
    """
    Mixins para filtrar el queryset de la vista según el rol del usuario.
    
    Un cliente solo verá sus propios objetos (con 'solicitante' = usuario),
    mientras que un administrador verá todos los objetos.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Un administrador o superusuario ve todos los objetos
        if user.groups.filter(name='admin').exists() or user.is_superuser:
            return queryset
        
        # Un cliente solo ve sus propios objetos
        if user.groups.filter(name='cliente').exists():
            return queryset.filter(solicitante=user)
        
        # Por defecto, si no tiene un rol específico, no se muestra nada.
        return queryset.none()