"""Django admin registration for reports."""

from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Lists reports with their key outcome columns."""

    list_display = (
        "id",
        "engineer_name",
        "station",
        "verdict",
        "severity",
        "status",
        "created_at",
    )
    list_filter = ("verdict", "severity", "status")
