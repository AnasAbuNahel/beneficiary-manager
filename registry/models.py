from django.core.exceptions import ValidationError
from django.db import models

from .validators import validate_national_id, validate_phone


class Beneficiary(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        PENDING = "pending", "Pending verification"
        CLOSED = "closed", "Closed"

    national_id = models.CharField(
        max_length=9, unique=True, validators=[validate_national_id]
    )
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True, validators=[validate_phone])
    district = models.CharField(max_length=80)
    household_size = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    registered_on = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-registered_on", "full_name"]
        verbose_name_plural = "beneficiaries"

    def __str__(self):
        return f"{self.full_name} ({self.national_id})"

    def clean(self):
        if self.household_size < 1:
            raise ValidationError({"household_size": "Household size must be at least 1."})
