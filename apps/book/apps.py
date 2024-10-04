from django.apps import AppConfig


class BookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.book'

    def ready(self) -> None:
        import apps.book.signals.signals