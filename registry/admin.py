from django.contrib import admin

from .models import Beneficiary


@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ("full_name", "national_id", "district", "household_size", "status")
    list_filter = ("status", "district")
    search_fields = ("full_name", "national_id", "phone")
