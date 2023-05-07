import os

import firebase_admin
from fcm_django.models import FCMDevice
from firebase_admin import credentials
from firebase_admin.messaging import Message, Notification

from stories.settings import BASE_DIR

cred = credentials.Certificate(os.path.join(BASE_DIR, "stories-96d17-firebase-adminsdk-22ng4-1336b4a29c.json"))

firebase_admin.initialize_app(cred)


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
