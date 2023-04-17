from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
from category.serialazers import CategorySerializer
from .models import Story, Category, StoryView


class AuthorSer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'username')
        model = User


class StoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryView
        fields = ("id", "user_id", "story_id")


class StorySerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    timeCreate = serializers.DateTimeField(source='time_create', read_only=True)
    categoryId = serializers.IntegerField(source='category.id')
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ("id", "title", "body", "view_count", "timeCreate", "author", "categoryId")

    def create(self, validated_data):
        user = self.context['request'].user
        return Story.objects.create(body=validated_data['body'],
                                    title=validated_data['title'],
                                    category=Category.objects.get(pk=validated_data['category']['id'], ),
                                    user=user)

    def get_author(self, obj):
        return {"username": obj.user.username,
                "userid": obj.user.id
                }

    def get_view_count(self, obj):
        print("Title " + obj.title + " id : " + str(obj.id) + " ")
        count = StoryView.objects.filter(story_id=obj.id).count()
        print(count)
        return count
