import re

from django.core.exceptions import ValidationError

ID_RE = re.compile(r"^\d{9}$")
PHONE_RE = re.compile(r"^(\+970|0)?5[0-9]{8}$")


def validate_national_id(value: str) -> None:
    """A Palestinian ID number has exactly nine digits."""
    if not ID_RE.match(value or ""):
        raise ValidationError("ID number must be exactly 9 digits.")


def validate_phone(value: str) -> None:
    """Accepts 05XXXXXXXX, 5XXXXXXXX or +9705XXXXXXXX."""
    if value and not PHONE_RE.match(value.replace(" ", "").replace("-", "")):
        raise ValidationError("Enter a valid mobile number, e.g. 0597654321.")
