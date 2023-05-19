from django.contrib.auth.models import User
from rest_framework import serializers

from story.models import StoryView, Story
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'count')

    def get_count(self, obj):
        request_type = self.context.get('type')
        if request_type == 'for_all':
            count = Story.objects.filter(category_id=obj.id, is_published=True).count()
            return count
        else:
            user_id = self.context.get('user_id')
            count = Story.objects.filter(category_id=obj.id, user_id=user_id).count()
            return count
