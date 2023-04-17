from django.core.paginator import Paginator, EmptyPage
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Story, StoryView
from .serialazers import StorySerializer, StoryViewSerializer


class StoryPaginationAPIView(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 1000

    def get_paginated_response(self, data):
        category_id = self.request.query_params.get('categoryId', "1")
        query_set = Story.objects.filter(category_id=category_id, is_published=True).order_by('time_create')
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
    permission_classes = (AllowAny,)


class StoryUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    # permission_classes = (IsAdminReadOnly,)


class StoryDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    # permission_classes = (IsAdminReadOnly,)


class StoryViewListApiView(generics.ListCreateAPIView):
    queryset = StoryView.objects.all()
    serializer_class = StoryViewSerializer
    # permission_classes = (IsAdminReadOnly,)


"""
{
"body" : "Але, мама, дай папе трубку. - Але, папа, Спартак чемпион???",
"category_id":1
}
"""
