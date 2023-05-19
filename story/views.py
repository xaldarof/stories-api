from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count, Sum, F, Q
from django.http import JsonResponse
from fcm_django.models import FCMDevice
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_user.serializers import UserSerializer
from notification.models import Notification
from .models import Story, StoryView, StoryQuote
from .permissions import IsAdminReadOnly
from .serialazers import StorySerializer, StoryViewSerializer, StoryUpdateSerializer, StoryQuoteSerializer


class StoryPaginationAPIView(PageNumberPagination):
    page_query_param = 'page'

    def get_paginated_response(self, data):
        category_id = self.request.query_params.get('categoryId', None)
        page = self.request.query_params.get('page')

        query_set = Story.objects.filter(category_id=category_id, is_published=True).order_by('?')
        paginator = Paginator(query_set, 10)

        try:
            page = paginator.page(int(page))
            serializer = StorySerializer(data=page, many=True, context={"request": self.request})
            serializer.is_valid()
            return Response({
                "count": query_set.count(),
                "results": serializer.data,
            })
        except EmptyPage:
            return Response({
                "count": query_set.count(),
                "results": [],
            })


class UserStoryPaginationAPIView(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 1000

    def get_paginated_response(self, data):
        category_id = self.request.query_params.get('categoryId', None)
        if category_id:
            query_set = Story.objects.filter(category_id=category_id,
                                             user_id=self.request.query_params['userId']).order_by(
                '-time_create')
        else:
            query_set = Story.objects.filter(user_id=self.request.query_params['userId']).order_by(
                '-time_create')
        paginator = Paginator(query_set, 10)

        page_size = self.request.query_params.get('page')
        if page_size:
            try:
                page = paginator.page(page_size)
            except EmptyPage:
                page = paginator.page(paginator.num_pages)

            serializer = StorySerializer(data=page, many=True, context={"request": self.request})
            serializer.is_valid()
            return Response({
                "count": paginator.count,
                'results': serializer.data,
            })
        else:
            serializer = StorySerializer(data=query_set, many=True, context={"request": self.request})
            serializer.is_valid()
            return Response({
                "count": paginator.count,
                "results": serializer.data,
            })


class StoryListAPIView(generics.ListCreateAPIView):
    serializer_class = StorySerializer
    queryset = Story.objects.all()
    pagination_class = StoryPaginationAPIView
    permission_classes = (IsAuthenticated,)


class StoryUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryUpdateSerializer
    permission_classes = (AllowAny,)


class StoryVisibilityAPIView(APIView):
    queryset = Story.objects.all()
    serializer_class = StoryUpdateSerializer
    permission_classes = (AllowAny,)

    @staticmethod
    def put(request, pk):
        story = Story.objects.get(pk=pk)
        if story.user.id == request.user.id:
            story.is_published = int(request.query_params['state']) == 1
            story.save(update_fields=['is_published'])
            return Response({"success"})
        else:
            return Response({"fail"}, status=405)


class StoryDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = (IsAdminReadOnly,)


class UserStoryListAPIView(generics.ListAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    pagination_class = UserStoryPaginationAPIView
    permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     user_id = self.request.user.id
    #     return


class UserStoryStatsListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = self.request.user.id
        stories = Story.objects.filter(user_id=user_id)
        views = StoryView.objects.all()
        unread_notification_count = Notification.objects.filter(user_id=user_id, is_read=0)
        view_reach_count = views.filter(story_owner_id=user_id).count()
        print(unread_notification_count.query)
        story_count = stories.count()

        return Response({"readStoriesCount": StoryView.objects.filter(user_id=user_id).count(),
                         "storyCount": story_count,
                         "viewReachCount": view_reach_count,
                         "unreadNotificationCount": unread_notification_count.count(),
                         })


class StoryViewListApiView(generics.ListCreateAPIView):
    queryset = StoryView.objects.all()
    serializer_class = StoryViewSerializer
    permission_classes = (IsAuthenticated,)


class StoryQuoteListApiView(generics.ListCreateAPIView):
    queryset = StoryQuote.objects.all()
    serializer_class = StoryQuoteSerializer
    permission_classes = (AllowAny,)

    def get_paginated_response(self, data):
        story_id = self.request.query_params.get('storyId')
        quotes = StoryQuote.objects.filter(story_id=story_id)
        serializer = StoryQuoteSerializer(data=quotes, many=True, context={"request": self.request})
        serializer.is_valid()
        return Response({"results": serializer.data})


class TopUsersListApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, *args):
        top_users = User.objects.annotate(view_count=Count('storyview') * Count('story')).order_by('-view_count')
        serializer = UserSerializer(top_users, many=True, context={"request": self.request})
        return Response({"results": serializer.data})


class TopActiveUsersListApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, *args):
        top_users = User.objects.annotate(view_count=Count('storyview')).order_by('-view_count')
        serializer = UserSerializer(top_users, many=True)
        return Response({"results": serializer.data})


class TopStoriesListApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, *args):
        top_users = User.objects.filter().annotate(num_views=Count('storyview')).order_by(
            '-num_views')[:100]
        serializer = UserSerializer(top_users, many=True)
        for i in top_users:
            print("Views : " + str(i.num_views))
        return Response({"results": serializer.data})
