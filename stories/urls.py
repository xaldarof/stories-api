from django.contrib import admin
from django.urls import path
from story.views import StoryListAPIView, StoryUpdateAPIView, StoryDestroyAPIView
from category.views import StoryCategoryListAPIView, StoryCategoryUpdateAPIView, StoryCategoryDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # story
    path('admin/', admin.site.urls),
    path('api/v1/stories/', StoryListAPIView.as_view()),
    path('api/v1/story/<int:pk>/', StoryUpdateAPIView.as_view()),
    path('api/v1/story/delete/<int:pk>', StoryDestroyAPIView.as_view()),

    # category
    path('api/v1/categories/', StoryCategoryListAPIView.as_view()),
    path('api/v1/category/<int:pk>/', StoryCategoryUpdateAPIView.as_view()),
    path('api/v1/category/delete/<int:pk>', StoryCategoryDestroyAPIView.as_view()),

    # auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
