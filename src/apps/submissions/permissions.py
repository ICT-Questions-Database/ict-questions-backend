from rest_framework.permissions import BasePermission, SAFE_METHODS

class QuestionSubmissionPermission(BasePermission):
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


class CorrectSubmissionAnswersSourcesPermission(BasePermission):
    """
    Permite admins ou o dono da QuestionSubmission
    acessar/editar fontes de resposta.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.question_submission.submitted_by == request.user