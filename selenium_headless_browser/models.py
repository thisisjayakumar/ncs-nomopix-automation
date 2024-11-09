from django.db import models
from django.utils import timezone
from users.models import User


class BaseClass(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CodeLogHistory(BaseClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_logs')
    major_code = models.CharField(max_length=100)
    result_json = models.JSONField()

    def __str__(self):
        return f"Log for Major Code {self.major_code} by User {self.user}"
