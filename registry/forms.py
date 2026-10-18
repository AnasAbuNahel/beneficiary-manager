from django import forms

from .models import Beneficiary


class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = ["national_id", "full_name", "phone", "district", "household_size", "status", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}


class CsvUploadForm(forms.Form):
    file = forms.FileField(
        help_text="UTF-8 CSV with columns: national_id, full_name, phone, district, household_size, status"
    )
