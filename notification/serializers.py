from rest_framework import serializers

from notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user.id')
    timeCreate = serializers.DateTimeField(source='time_create')
    isRead = serializers.BooleanField(source='is_read')

    class Meta:
        model = Notification
        fields = ('id', 'userId', "timeCreate", "isRead", "content")
