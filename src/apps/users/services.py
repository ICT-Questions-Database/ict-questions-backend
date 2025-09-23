from .models import CustomUser, UserAnswers
from .exceptions import MissingPasswordError, InvalidPasswordError, MissingExamAttemptError


def delete_user_account(user: CustomUser, password: str) -> None:
    if not password:
        raise MissingPasswordError("Password is required to delete account")

    if not user.check_password(password):
        raise InvalidPasswordError("Incorrect password.")
    user.delete()


def change_user_password(user: CustomUser, current_password, new_password: str) -> None:
    if not current_password or not new_password:
        raise MissingPasswordError(
            "Both current_password and new_password are required"
        )

    if not user.check_password(current_password):
        raise InvalidPasswordError("Incorrect password.")

    user.set_password(new_password)
    user.save()


def get_user_answers_by_exam(user: CustomUser, exam_attempt_id: str) -> None:
    if not exam_attempt_id:
        raise MissingExamAttemptError("No exam_attempt was given.")

    return (
        UserAnswers.objects
        .filter(user=user, exam_attempt=exam_attempt_id)
        .select_related("question", "alternative")
        .order_by("question_id")
    )