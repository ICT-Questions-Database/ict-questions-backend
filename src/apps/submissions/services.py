from django.utils import timezone
from .models import QuestionSubmission

def review_submission(
    submission: QuestionSubmission, 
    reviewer, status, feedback: str
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
