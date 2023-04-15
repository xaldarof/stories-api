from rest_framework import generics
from rest_framework.response import Response
from .models import Category
from .serialazers import CategorySerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser, AllowAny


class StoryCategoryPaginationAPIView(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    max_page_size = 1000

    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_paginated_response(self, data):
        return Response({"count": self.page.paginator.count, "results": data})


class StoryCategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StoryCategoryPaginationAPIView
    permission_classes = (AllowAny,)


class StoryCategoryUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsAdminReadOnly,)


class StoryCategoryDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsAdminReadOnly,)


"""
{
"body" : "Але, мама, дай папе трубку. - Але, папа, Спартак чемпион???",
"category_id":1
}
"""
