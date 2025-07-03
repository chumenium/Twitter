from django.apps import AppConfig

class MicroboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'microboard'

    def ready(self):
        import microboard.signals
