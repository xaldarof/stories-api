from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Story,StoryView

admin.site.register(Story)
admin.site.register(StoryView)
