from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from category.serialazers import CategorySerializer
from .models import Story, Category, StoryView

from rest_framework.fields import CurrentUserDefault


class AuthorSer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'username')
        model = User


class StoryViewSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    story_id = serializers.IntegerField()

    class Meta:
        model = StoryView
        fields = ("id", "user_id", "story_id")

    def create(self, validated_data):
        user = self.context['request'].user
        is_own = Story.objects.get(pk=validated_data['story_id']).user_id == user.id
        print(is_own)
        if not is_own:
            return StoryView.objects.create(story_id=validated_data['story_id'], user=user)
        else:
            return StoryView.objects.get(pk=1)

    @staticmethod
    def get_user_id(obj):
        return obj.user.id


class StorySerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    isOwner = serializers.SerializerMethodField()
    timeCreate = serializers.DateTimeField(source='time_create', read_only=True)
    isPremium = serializers.SerializerMethodField(method_name='get_is_premium', read_only=True)
    isFrozen = serializers.BooleanField(source='is_frozen', read_only=True)
    categoryId = serializers.IntegerField(source='category.id')
    viewCount = serializers.SerializerMethodField(method_name='get_view_count')
    isPublished = serializers.SerializerMethodField(allow_null=True, read_only=True)

    class Meta:
        model = Story
        fields = (
            "id", "title", "body", "isFrozen", "isPublished", "isOwner", "isPremium", "viewCount", "timeCreate",
            "author",
            "categoryId")

    def get_isOwner(self, validated_data):
        user = self.context.get('request').user.id
        return user == validated_data.user_id

    def get_isPublished(self, validated_data):
        user = self.context.get('request').user.id
        if user == validated_data.user_id:
            return validated_data.is_published
        else:
            return None

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

    @staticmethod
    def get_view_count(obj):
        count = StoryView.objects.filter(story_id=obj.id).count()
        return count

    @staticmethod
    def get_is_premium(obj):
        count = StoryView.objects.filter(story_id=obj.id).count()
        return count > 20 or obj.user.is_superuser


class StoryUpdateSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    isOwner = serializers.SerializerMethodField()
    timeCreate = serializers.DateTimeField(source='time_create', read_only=True)
    isPremium = serializers.SerializerMethodField(method_name='get_is_premium', read_only=True)
    isFrozen = serializers.BooleanField(source='is_frozen', read_only=True)
    categoryId = serializers.IntegerField(source='category.id', read_only=True)
    viewCount = serializers.SerializerMethodField(method_name='get_view_count')

    class Meta:
        model = Story
        fields = (
            "id", "title", "body", "isFrozen", "isOwner", "isPremium", "viewCount", "timeCreate", "author",
            "categoryId")

    def get_isOwner(self, validated_data):
        user = self.context.get('request').user.id
        return user == validated_data.user_id

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

    @staticmethod
    def get_view_count(obj):
        count = StoryView.objects.filter(story_id=obj.id).count()
        return count

    @staticmethod
    def get_is_premium(obj):
        count = StoryView.objects.filter(story_id=obj.id).count()
        return count > 20 or obj.user.is_superuser
