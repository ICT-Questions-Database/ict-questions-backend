from rest_framework.permissions import BasePermission

class QuestionSubmissionPermission(BasePermission):
    """
    Permite admins fazer tudo.
    Usuários só podem ler e alterar/excluir submissões próprias.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.submitted_by == request.user


class BaseSubmissionPermission(BasePermission):
    """
    Permite admins ou o dono da QuestionSubmission
    acessar/editar fontes de resposta.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.question_submission.submitted_by == request.user
