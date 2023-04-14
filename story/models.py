from django.contrib.auth import get_user_model
from django.db import models
from category.models import Category


# Create your models here.


class Story(models.Model):
    body = models.CharField(max_length=1000)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(get_user_model(), verbose_name='Пользователь', on_delete=models.CASCADE)
