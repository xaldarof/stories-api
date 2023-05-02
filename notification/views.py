from rest_framework.views import APIView

from django.shortcuts import render

from notification.models import Notification
from notification.serializers import NotificationSerializer
from rest_framework.response import Response


# Create your views here.


class UserNotificationsAPIView(APIView):

    def get(self, *args):
        notifications = Notification.objects.filter(user=self.request.user).order_by('is_read')
        ser = NotificationSerializer(data=notifications, many=True)
        ser.is_valid()
        return Response({"results": ser.data})

    def post(self, *args, **kwargs):
        notification = Notification.objects.get(pk=self.request.data['id'])
        notification.is_read = 1
        notification.save(update_fields=['is_read'])
        return Response(status=200)
