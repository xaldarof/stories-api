from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category
from .serialazers import CategorySerializer


class StoryCategoryListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, args):
        categories = Category.objects.filter()
        serializer = CategorySerializer(data=categories, context={"request": self.request, "type": "for_all"},
                                        many=True)
        serializer.is_valid()
        return Response({"results": serializer.data})


class UserStoryCategoryListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, args):
        user_id = self.request.query_params.get('userId', None)
        categories = Category.objects.filter()
        serializer = CategorySerializer(data=categories, context={"user_id": user_id, "type": "for_user"},
                                        many=True)
        serializer.is_valid()
        return Response({"results": serializer.data})


class StoryCategoryUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsAdminReadOnly,)


class StoryCategoryDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsAdminReadOnly,)
