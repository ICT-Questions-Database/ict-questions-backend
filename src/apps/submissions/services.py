from django.utils import timezone
from typing import Optional
from django.db.models import QuerySet
from .models import QuestionSubmission, CorrectSubmissionAnswersSources, AlternativeSubmission
from apps.users.models import CustomUser


def review_submission(
    submission: QuestionSubmission, reviewer, status, feedback: str
) -> QuestionSubmission:
    """
    Faz a revisão de uma QuestionSubmission.
    - Atualiza status
    - Define reviewed_by e reviewed_at
    - Atualiza feedback
    """
    if not reviewer.is_staff:
        raise PermissionError("Only admins can review submissions.")

    if status not in QuestionSubmission.Status.values:
        raise ValueError(f"Invalid status: {status}")

    submission.reviewed_by = reviewer
    submission.reviewed_at = timezone.now()
    submission.status = status
    if feedback is not None:
        submission.feedback = feedback

    submission.save()
    return submission


def get_sources_for_user(
    user: CustomUser, question_submission_id: Optional[int] = None
) -> QuerySet[CorrectSubmissionAnswersSources]:
    """
    Retorna as fontes de respostas de submissões para o usuário.

    - Admin pode ver tudo
    - User normal só vê suas próprias submissões
    - Se 'question_submission_id' for passado, filtra apenas para essa questão
    """
    queryset = CorrectSubmissionAnswersSources.objects.all().order_by("id")

    if not user.is_staff:
        queryset = queryset.filter(question_submission__submitted_by=user)

    if question_submission_id is not None:
        queryset = queryset.filter(question_submission_id=question_submission_id)

    return queryset


def get_alternatives_for_questions_by_user(
    user: CustomUser, question_submission_id: Optional[int] = None
) -> QuerySet[AlternativeSubmission]:
    """
    Retorna as alternativas das questões para o usuário

    - Admin pode ver tudo
    - User normal só vê as questões das próprias submissões
    - Se 'question_submission_id' for passado, filtra apenas para essa questão
    """
    queryset = AlternativeSubmission.objects.all().order_by("id")

    if not user.is_staff:
        queryset = queryset.filter(question_submission__submitted_by=user).order_by("id")

    if question_submission_id is not None:
        queryset = queryset.filter(question_submission_id=question_submission_id).order_by("id")

    return queryset
