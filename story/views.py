from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Story
from .serialazers import StorySerializer


class StoryPaginationAPIView(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({"count": self.page.paginator.count, "results": data})


class StoryListAPIView(generics.ListCreateAPIView):
    serializer_class = StorySerializer
    pagination_class = StoryPaginationAPIView
    permission_classes = (AllowAny,)

    def get_queryset(self):
        category_id = self.request.query_params.get('categoryId')
        if category_id is not None:
            queryset = Story.objects.filter(category_id=category_id)
        else:
            queryset = Story.objects.all()
        return queryset


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
