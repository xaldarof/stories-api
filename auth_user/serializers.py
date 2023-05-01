from django.contrib.auth.models import User
from rest_framework import serializers

from story.models import StoryView, Story


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    lastName = serializers.CharField(read_only=True, source='last_name')
    firstName = serializers.CharField(read_only=True, source='first_name')
    dateJoined = serializers.CharField(read_only=True, source='date_joined')
    score = serializers.SerializerMethodField()

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'firstName', 'lastName', 'password', 'dateJoined', 'score')

    def get_score(self, obj):
        viewed = StoryView.objects.filter(user_id=obj.id).count()
        posted = Story.objects.filter(user_id=obj.id).count()
        return viewed * posted
