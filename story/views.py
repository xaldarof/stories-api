from rest_framework import generics
from rest_framework.exceptions import NotFound

from .models import Story
from .serialazers import StorySerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser, AllowAny


class StoryPaginationAPIView(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({"count": self.page.paginator.count, "results": data})


class StoryListAPIView(generics.ListCreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    pagination_class = StoryPaginationAPIView
    permission_classes = (AllowAny,)


class StoryUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    # permission_classes = (IsAdminReadOnly,)


class StoryDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    # permission_classes = (IsAdminReadOnly,)


"""
{
"body" : "Але, мама, дай папе трубку. - Але, папа, Спартак чемпион???",
"category_id":1
}
"""
