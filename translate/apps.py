from django.apps import AppConfig


class TranslateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translate'

    def ready(self) -> None:

        from . import signals

        return super().ready()
