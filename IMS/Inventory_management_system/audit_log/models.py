from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    change_message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)


    # These fields must exist if you're using them in `list_display` and `list_filter`
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)  # Ensure this exists
    model_name = models.CharField(max_length=255, null=True, blank=True)  # Ensure this exists

    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"
