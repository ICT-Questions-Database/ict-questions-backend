from .models import CustomUser
from .exceptions import MissingPasswordError, InvalidPasswordError


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
