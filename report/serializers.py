from rest_framework.serializers import ModelSerializer

from report.models import StoryReport


class StorySerializer(ModelSerializer):
    class Meta:
        model = StoryReport
        fields = "__all__"
