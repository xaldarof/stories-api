import firebase_admin
from firebase_admin import credentials, messaging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

cred = credentials.Certificate("stories-96d17-firebase-adminsdk-22ng4-1336b4a29c.json")
firebase_admin.initialize_app(cred)


class NotificationAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, args):
        message = messaging.MulticastMessage(
            notification=messaging.Notification(title=self.request.data['title'], body=self.request.data['body']),
            data=dict(self.request.data['data']),
            tokens=self.request.data['tokens'])
        response = messaging.send_multicast(message)
        print('Successfully sent : ', response)
        print('Count : ', response.success_count)
        return Response("success")
