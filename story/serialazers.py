from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
from category.serialazers import CategorySerializer
from .models import Story, Category


class AuthorSer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'username')
        model = User


class StorySerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    timeCreate = serializers.DateTimeField(source='time_create')
    categoryId = serializers.IntegerField(source='category.id')

    class Meta:
        model = Story
        fields = ("id", "body", "timeCreate", "author", "categoryId")

    @staticmethod
    def get_author(obj):
        return {"username": obj.user.username,
                "userid": obj.user.id
                }
