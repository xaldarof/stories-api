from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = "__all__"
