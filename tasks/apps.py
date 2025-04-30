"""
App configuration for the Tasks application.
"""

from django.apps import AppConfig


class TasksConfig(AppConfig):
    """
    Configuration class for the Tasks app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "tasks"
