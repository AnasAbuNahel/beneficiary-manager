import io

from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BeneficiaryForm, CsvUploadForm
from .models import Beneficiary
from .services import export_xlsx, find_duplicate_groups, import_csv


def dashboard(request):
    qs = Beneficiary.objects.all()
    context = {
        "total": qs.count(),
        "people_reached": qs.aggregate(n=Sum("household_size"))["n"] or 0,
        "by_status": qs.values("status").annotate(n=Count("id")).order_by("-n"),
        "by_district": qs.values("district").annotate(n=Count("id")).order_by("-n")[:10],
        "duplicate_groups": len(find_duplicate_groups()),
    }
    return render(request, "registry/dashboard.html", context)


def beneficiary_list(request):
    qs = Beneficiary.objects.all()
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    if q:
        qs = qs.filter(
            Q(full_name__icontains=q) | Q(national_id__icontains=q) | Q(phone__icontains=q)
        )
    if status:
        qs = qs.filter(status=status)
    return render(
        request,
        "registry/list.html",
        {"items": qs, "q": q, "status": status, "statuses": Beneficiary.Status.choices},
    )


def beneficiary_edit(request, pk=None):
    obj = get_object_or_404(Beneficiary, pk=pk) if pk else None
    form = BeneficiaryForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Saved.")
        return redirect("registry:list")
    return render(request, "registry/form.html", {"form": form, "obj": obj})


def duplicates(request):
    return render(request, "registry/duplicates.html", {"groups": find_duplicate_groups()})


def import_view(request):
    form = CsvUploadForm(request.POST or None, request.FILES or None)
    report = None
    if request.method == "POST" and form.is_valid():
        raw = form.cleaned_data["file"].read().decode("utf-8-sig")
        report = import_csv(io.StringIO(raw))
    return render(request, "registry/import.html", {"form": form, "report": report})


def export_view(request):
    data = export_xlsx(Beneficiary.objects.all())
    response = HttpResponse(
        data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="beneficiaries.xlsx"'
    return response
