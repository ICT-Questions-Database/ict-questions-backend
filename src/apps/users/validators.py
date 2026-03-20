import re

from django.core.exceptions import ValidationError


class SpecialCharacterValidator:
    def validate(self, password, user=None):
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                    "A senha deve conter pelo menos um caractere especial",
                    code='password_no_special',
                    )

    def get_help_text(self):
        return "Sua senha deve conter pelo menos um caractere especial"

class CapitalLetterValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                    "A senha deve conter pelo menos uma letra maiúscula.",
                    code="password_no_upper",
                    )

    def get_help_text(self):
        return "Sua senha deve conter pelo menos uma letra maiúscula"
