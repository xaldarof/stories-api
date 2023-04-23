from django.core.paginator import Paginator, EmptyPage
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Story, StoryView
from .permissions import IsAdminReadOnly
from .serialazers import StorySerializer, StoryViewSerializer


class StoryPaginationAPIView(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 1000

    def get_paginated_response(self, data):
        category_id = self.request.query_params.get('categoryId', None)
        if category_id:
            query_set = Story.objects.filter(category_id=category_id).order_by('?')
        else:
            query_set = Story.objects.filter().order_by('?')
        paginator = Paginator(query_set, 10)
        page_size = self.request.query_params.get('page')
        if page_size:
            try:
                page = paginator.page(page_size)
            except EmptyPage:
                page = paginator.page(paginator.num_pages)

            serializer = StorySerializer(data=page, many=True)
            serializer.is_valid()
            return Response({
                "count": paginator.count,
                'results': serializer.data,
            })
        else:
            serializer = StorySerializer(data=query_set, many=True)
            serializer.is_valid()
            return Response({
                "count": paginator.count,
                "results": serializer.data,
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
            query_set = Story.objects.filter(user_id=self.request.query_params['userId']).order_by('-time_create')
        paginator = Paginator(query_set, 10)

        page_size = self.request.query_params.get('page')
        if page_size:
            try:
                page = paginator.page(page_size)
            except EmptyPage:
                page = paginator.page(paginator.num_pages)

            serializer = StorySerializer(data=page, many=True)
            serializer.is_valid()
            return Response({
                "count": paginator.count,
                'results': serializer.data,
            })
        else:
            serializer = StorySerializer(data=query_set, many=True)
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
    serializer_class = StorySerializer
    permission_classes = (IsAdminReadOnly,)


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
        story_count = stories.count()

        view_reach_count = 0
        for story in stories:
            view_reach_count += views.filter(story_id=story.id).count()

        return Response({"readStoriesCount": StoryView.objects.filter(user_id=user_id).count(),
                         "storyCount": story_count,
                         "viewReachCount": view_reach_count,
                         })


class StoryViewListApiView(generics.ListCreateAPIView):
    queryset = StoryView.objects.all()
    serializer_class = StoryViewSerializer
    permission_classes = (IsAuthenticated,)
