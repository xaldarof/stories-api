from fcm_django.models import FCMDevice
from firebase_admin.messaging import Notification

from firebase_admin import messaging
from firebase_admin.messaging import Notification
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notification.models import Notification
from notification.serializers import NotificationSerializer


# Create your views here.


class NotificationAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, args):
        message = messaging.MulticastMessage(
            notification=messaging.Notification(title=self.request.data['title'], body=self.request.data['body']),
            data=dict(self.request.data['data']),
            tokens=self.request.data['tokens'])
        response = messaging.send_multicast(message)
        return Response("success")


class NotificationRefreshTokenAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, args):
        new_token = self.request.data['token']
        user = self.request.user
        device = FCMDevice.objects.filter(user=user).first()
        if device:
            device.registration_id = new_token
            device.save()
            return Response("success")
        else:
            return Response("not found", status=401)


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
