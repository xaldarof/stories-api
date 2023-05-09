from django.contrib.auth import get_user_model
from django.db import models

from story.models import Story


# Create your models here.


class StoryReport(models.Model):
    time_create = models.DateTimeField(auto_now=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=200, default=None, null=True, blank=True)
