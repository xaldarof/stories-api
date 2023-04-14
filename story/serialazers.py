from rest_framework import serializers

from .models import Story


class StorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Story
        fields = "__all__"
