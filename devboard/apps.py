from django.apps import AppConfig


class DevboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'devboard'
    verbose_name = "Devboard v.0.1"

    def ready(self):
        print("Aplikacja DevBOARD została uruchomiona")