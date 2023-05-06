from django.contrib.auth import authenticate
from django.shortcuts import render
from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer


class RegistrationAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        token = request.data['fcmToken']
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        print("Fcm token", token)
        device = FCMDevice.objects.get(registration_id=token)
        if device:
            device.user = user
            device.save()
            print('Success updated device')
        else:
            fcm_device = FCMDevice()
            fcm_device.registration_id = token
            fcm_device.user = user
            fcm_device.save()
            print('New created')
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        token = request.data.get('fcmToken')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        device = FCMDevice.objects.get(registration_id=token)
        if device:
            device.user = user
            device.save()
            print('Success updated device')
        else:
            fcm_device = FCMDevice()
            fcm_device.registration_id = token
            fcm_device.user = user
            fcm_device.save()
            print('New created')

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })


class ProfileView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
