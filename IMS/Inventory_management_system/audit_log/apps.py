from django.apps import AppConfig

class AuditLogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'audit_log'

    def ready(self):
        import audit_log.signals  # Import the signals
