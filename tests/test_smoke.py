"""Smoke tests: prove Django is wired up before any app logic exists."""

import pytest
from django.apps import apps
from django.db import connection


def test_reports_app_is_installed():
    """The reports app is registered, so Django will find its models and migrations."""
    assert apps.is_installed("reports")


@pytest.mark.django_db
def test_database_is_reachable():
    """The test database accepts a query after migrations run."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        assert cursor.fetchone() == (1,)
