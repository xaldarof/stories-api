from django.shortcuts import render
from fcm_django.models import FCMDevice
from rest_framework.views import APIView
from rest_framework.response import Response

from notification.fcm import send_notification
from report.models import StoryReport
from story.models import Story


# Create your views here.


class ReportStoryAPIView(APIView):

    def post(self, request, *args, **kwargs):
        story = Story.objects.filter(pk=request.data.get('storyId')).first()
        if story:
            report = StoryReport()
            report.story = story
            report.user = self.request.user
            report.save()
            send_notification(user=story.user, title='Attention !',
                              body='Your story has been reported. Please check the status of your story. If you '
                                   'believe the report is false, please notify us at t.me/xaldarof')
            return Response("success")
        else:
            return Response("error", status=403)
