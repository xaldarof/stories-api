from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.


class Notification(models.Model):
    content = models.CharField(max_length=1000)
    time_create = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, blank=False)
