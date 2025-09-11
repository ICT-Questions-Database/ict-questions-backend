from django.utils import timezone
from .models import ExamAttempt
from typing import Optional

def finish_exam_attempt(
    attempt: ExamAttempt, 
    grade: Optional[float] = None
) -> ExamAttempt:
    """
    Finaliza um ExamAttempt:
    - atualiza a nota (grade)
    - marca end_date
    - calcula duration
    """
    if grade is not None:
        attempt.grade = grade

    attempt.end_date = timezone.now()
    attempt.duration = attempt.end_date - attempt.start_date
    attempt.save()
    return attempt

