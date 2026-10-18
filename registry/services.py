"""Data-quality helpers: duplicate detection, CSV import, Excel export."""
import csv
import io
from collections import defaultdict
from dataclasses import dataclass, field

from django.core.exceptions import ValidationError
from openpyxl import Workbook

from .models import Beneficiary

EXPORT_COLUMNS = [
    ("national_id", "ID number"),
    ("full_name", "Full name"),
    ("phone", "Phone"),
    ("district", "District"),
    ("household_size", "Household size"),
    ("status", "Status"),
    ("registered_on", "Registered on"),
]


def normalise_name(name: str) -> str:
    return " ".join(name.split()).casefold()


def find_duplicate_groups():
    """Group records that share a phone number or the same normalised name + district."""
    groups = defaultdict(list)
    for b in Beneficiary.objects.all():
        if b.phone:
            groups[("phone", b.phone.replace(" ", ""))].append(b)
        groups[("name", normalise_name(b.full_name), b.district.casefold())].append(b)
    seen, result = set(), []
    for key, members in groups.items():
        ids = tuple(sorted(m.pk for m in members))
        if len(members) > 1 and ids not in seen:
            seen.add(ids)
            result.append({"reason": key[0], "members": members})
    return result


@dataclass
class ImportReport:
    created: int = 0
    skipped_existing: int = 0
    errors: list = field(default_factory=list)  # (row_number, message)

    @property
    def ok(self):
        return not self.errors


def import_csv(text_stream) -> ImportReport:
    """Import beneficiaries from a CSV text stream; every bad row is reported, good rows are kept."""
    report = ImportReport()
    reader = csv.DictReader(text_stream)
    for line_no, row in enumerate(reader, start=2):
        national_id = (row.get("national_id") or "").strip()
        if Beneficiary.objects.filter(national_id=national_id).exists():
            report.skipped_existing += 1
            continue
        try:
            obj = Beneficiary(
                national_id=national_id,
                full_name=" ".join((row.get("full_name") or "").split()),
                phone=(row.get("phone") or "").strip(),
                district=(row.get("district") or "").strip(),
                household_size=int(row.get("household_size") or 1),
                status=(row.get("status") or Beneficiary.Status.PENDING).strip(),
            )
            if not obj.full_name or not obj.district:
                raise ValidationError("Full name and district are required.")
            obj.full_clean()
            obj.save()
            report.created += 1
        except (ValidationError, ValueError) as exc:
            msg = "; ".join(exc.messages) if isinstance(exc, ValidationError) else str(exc)
            report.errors.append((line_no, msg))
    return report


def export_xlsx(queryset) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Beneficiaries"
    ws.append([label for _, label in EXPORT_COLUMNS])
    for b in queryset:
        ws.append([str(getattr(b, attr)) if attr == "registered_on" else getattr(b, attr) for attr, _ in EXPORT_COLUMNS])
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = max(len(str(c.value or "")) for c in col) + 3
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()
