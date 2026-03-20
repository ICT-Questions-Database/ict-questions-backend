from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Track(TextChoices):
    CLOUD = "cloud", _("Cloud")
    NETWORK = "network", _("Network")
    COMPUTING = "computing", _("Computing")


class Level(TextChoices):
    HCIA = "hcia", _("HCIA")
    HCIP = "hcip", _("HCIP")
    HCIE = "hcie", _("HCIE")


class Status(TextChoices):
    PENDING = "pending", _("Pending")
    APPROVED = "approved", _("Approved")
    REJECTED = "rejected", _("Rejected")


