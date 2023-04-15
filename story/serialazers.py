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
    timeCreate = serializers.DateTimeField(source='time_create', read_only=True)
    categoryId = serializers.IntegerField(source='category.id')

    class Meta:
        model = Story
        fields = ("id", "title", "body", "timeCreate", "author", "categoryId")

    def create(self, validated_data):
        user = self.context['request'].user
        return Story.objects.create(body=validated_data['body'],
                                    title=validated_data['title'],
                                    category=Category.objects.get(pk=validated_data['category']['id'], ),
                                    user=user)

    @staticmethod
    def get_author(obj):
        return {"username": obj.user.username,
                "userid": obj.user.id
                }
