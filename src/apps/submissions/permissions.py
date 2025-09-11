from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrOwner(BasePermission):
    """
    Permite admins fazer tudo.
    Usuários só podem ler e alterar/excluir submissões próprias.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if request.method in SAFE_METHODS:
            return obj.submitted_by == request.user
        
        return obj.submitted_by == request.user
    