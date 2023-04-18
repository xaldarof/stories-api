from django.contrib.auth import get_user_model
from django.db import models
from category.models import Category


# Create your models here.


class Story(models.Model):
    title = models.CharField(max_length=500)
    body = models.CharField(max_length=1000)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    is_frozen = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class StoryView(models.Model):
    time_create = models.DateTimeField(auto_now_add=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
