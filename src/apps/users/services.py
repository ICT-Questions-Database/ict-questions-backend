from .models import CustomUser
from .exceptions import MissingPasswordError, InvalidPasswordError

def delete_user_account(user: CustomUser, password: str):
    if not password:
        raise MissingPasswordError("Password is required to delete account")
    
    if not user.check_password(password):
        raise InvalidPasswordError("Incorrect password.")
    user.delete()
    