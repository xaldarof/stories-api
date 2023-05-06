from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Count
from fcm_django.models import FCMDevice
from rest_framework import serializers

from auth_user.fcm import send_notification
from .models import Story, Category, StoryView, StoryQuote


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
        story = Story.objects.get(pk=validated_data['story_id'])
        is_own = story == user.id
        if not is_own:
            story_object = StoryView.objects
            created = story_object.create(story_id=validated_data['story_id'], user=user, story_owner_id=story.user.id)
            current_reach_count = StoryView.objects.filter(story_owner_id=story.user.id).count()
            if current_reach_count % 10 == 0:
                send_notification(title="Congratulation !",
                                  body="You reached more " + str(current_reach_count) + " than  view !",
                                  user=story.user)
            return created
        return StoryView.objects.filter().first()

    @staticmethod
    def get_user_id(obj):
        return obj.user.id


class StoryQuoteSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(method_name='get_user')
    storyId = serializers.IntegerField(source='story_id')
    timeCreate = serializers.DateTimeField(source='time_create', read_only=True)
    isOwner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StoryQuote
        fields = ("id", "author", "storyId", "body", "timeCreate", "isOwner")

    def create(self, validated_data):
        user = self.context['request'].user
        return StoryQuote.objects.create(story_id=validated_data['story_id'], user=user,
                                         body=validated_data['body'])

    @staticmethod
    def get_user(obj):
        return {
            "username": obj.user.username,
            "id": obj.user.id
        }

    def get_isOwner(self, validated_data):
        user = self.context.get('request').user.id
        return user == validated_data.user_id


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
