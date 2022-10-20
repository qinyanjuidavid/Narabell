from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.store"

    def ready(self):
        import modules.store.signals
