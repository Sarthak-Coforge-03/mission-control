"""Django admin registration for reports."""

from django.contrib import admin

from .models import Briefing, Report, TraceStep


class TraceStepInline(admin.TabularInline):
    """Shows a report's trace steps as a table on the report's admin page."""

    model = TraceStep
    extra = 0
    fields = (
        "order",
        "step",
        "round",
        "model",
        "input_tokens",
        "output_tokens",
        "cost_usd",
        "outcome",
    )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Lists reports with their key outcome columns and their trace inline."""

    inlines = (TraceStepInline,)

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
