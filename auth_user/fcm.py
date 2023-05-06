import os

import firebase_admin
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice

from firebase_admin import credentials, messaging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from stories.settings import BASE_DIR

cred = credentials.Certificate(os.path.join(BASE_DIR, "stories-96d17-firebase-adminsdk-22ng4-1336b4a29c.json"))

firebase_admin.initialize_app(cred)


#
# FCMDevice.objects.send_message(
#     Message(notification=Notification(title="title", body="body", image="image_url"))
# )


class NotificationAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, args):
        message = messaging.MulticastMessage(
            notification=messaging.Notification(title=self.request.data['title'], body=self.request.data['body']),
            data=dict(self.request.data['data']),
            tokens=self.request.data['tokens'])
        response = messaging.send_multicast(message)
        return Response("success")


def send_notification(user, title, body):
    device = FCMDevice.objects.filter(user_id=user.id).first()
    if device:
        device = FCMDevice.objects.filter(registration_id=device.registration_id).first()
        if not device:
            print("Device not found")
        else:
            response = device.send_message(
                Message(notification=Notification(title=title, body=body)
                        ))
            print("Result: ", response)
    else:
        print("Register id not found")
