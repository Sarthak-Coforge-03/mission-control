"""Database models for anomaly reports."""

from django.db import models


class Report(models.Model):
    """An anomaly report filed by an engineer, plus what the pipeline decided about it."""

    class Verdict(models.TextChoices):
        """Launch verdict, set only by the launch-limit code."""

        GO = "go", "Go"
        NO_GO = "no_go", "No go"

    class Subsystem(models.TextChoices):
        """Subsystem the model sorts the report into."""

        PROPULSION = "propulsion", "Propulsion"
        AVIONICS = "avionics", "Avionics"
        TELEMETRY = "telemetry", "Telemetry"
        GROUND = "ground", "Ground"
        WEATHER = "weather", "Weather"
        OTHER = "other", "Other"

    class Severity(models.TextChoices):
        """Severity the model assigns to the report."""

        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    class BriefBy(models.IntegerChoices):
        """Minutes within which the Flight Director must be briefed."""

        HIGH = 5, "5 minutes"
        MEDIUM = 15, "15 minutes"
        LOW = 30, "30 minutes"

    class Status(models.TextChoices):
        """Where the report is in the pipeline."""

        PROCESSING = "processing", "Processing"
        READY = "ready", "Ready"
        NEEDS_REVIEW = "needs_review", "Needs review"
        FAILED = "failed", "Failed"

    # Filed by the engineer
    engineer_name = models.CharField(max_length=100)
    station = models.CharField(max_length=100)
    wind_knots = models.FloatField()
    temp_c = models.FloatField()
    fuel_pct = models.FloatField()
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Set by the pipeline
    verdict = models.CharField(max_length=10, choices=Verdict.choices, blank=True)
    violations = models.JSONField(default=list, blank=True)
    subsystem = models.CharField(max_length=20, choices=Subsystem.choices, blank=True)
    severity = models.CharField(max_length=10, choices=Severity.choices, blank=True)
    brief_by_minutes = models.IntegerField(
        choices=BriefBy.choices, null=True, blank=True
    )

    # The three model checks on the note
    injection_flagged = models.BooleanField(default=False)
    injection_reason = models.TextField(blank=True)
    missing_details_flagged = models.BooleanField(default=False)
    missing_details_reason = models.TextField(blank=True)
    panic_flagged = models.BooleanField(default=False)
    panic_reason = models.TextField(blank=True)

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PROCESSING
    )

    class Meta:
        """Newest reports first."""

        ordering = ("-created_at",)

    def __str__(self) -> str:
        """Short label used in the admin and the shell."""
        return f"#{self.pk} {self.station} ({self.engineer_name})"


class Briefing(models.Model):
    """The drafted briefing for one report; only a person may approve it."""

    class Status(models.TextChoices):
        """Approval state; the pipeline only ever creates PENDING."""

        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"

    class Rounds(models.IntegerChoices):
        """How many draft/review rounds it took (the loop stops at three)."""

        ONE = 1, "1 round"
        TWO = 2, "2 rounds"
        THREE = 3, "3 rounds"

    report = models.OneToOneField(
        Report, on_delete=models.CASCADE, related_name="briefing"
    )
    text = models.TextField()
    rounds = models.IntegerField(choices=Rounds.choices)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    approved_by = models.CharField(max_length=100, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Short label used in the admin and the shell."""
        return f"Briefing for report #{self.report_id} ({self.status})"
