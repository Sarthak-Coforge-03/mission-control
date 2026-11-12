"""Django admin registration for reports."""

from django.contrib import admin

from .models import Briefing, Report


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


@admin.register(Briefing)
class BriefingAdmin(admin.ModelAdmin):
    """Lists briefings with their approval state."""

    list_display = ("id", "report", "status", "rounds", "approved_by", "approved_at")
    list_filter = ("status",)
