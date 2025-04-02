from django.apps import AppConfig

class VotersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voters'
    verbose_name = 'Voter Management'

    def ready(self):
        # Avoid importing models here
        pass