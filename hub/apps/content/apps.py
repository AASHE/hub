from django.apps import AppConfig


class ContentTypesConfig(AppConfig):
    name = 'hub.apps.content'
    verbose_name = 'Content Types'

    def ready(self):
        import signals  # Register signal handlers.  # noqa
