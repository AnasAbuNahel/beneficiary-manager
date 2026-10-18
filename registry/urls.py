from django.urls import path

from . import views

app_name = "registry"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("beneficiaries/", views.beneficiary_list, name="list"),
    path("beneficiaries/new/", views.beneficiary_edit, name="new"),
    path("beneficiaries/<int:pk>/edit/", views.beneficiary_edit, name="edit"),
    path("duplicates/", views.duplicates, name="duplicates"),
    path("import/", views.import_view, name="import"),
    path("export/", views.export_view, name="export"),
]
