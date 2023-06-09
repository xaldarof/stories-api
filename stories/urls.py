from django.contrib import admin
from django.urls import path

from report.views import ReportStoryAPIView
from story.views import StoryListAPIView, StoryUpdateAPIView, StoryDestroyAPIView, StoryViewListApiView, \
    UserStoryListAPIView, UserStoryStatsListAPIView, StoryVisibilityAPIView, StoryQuoteListApiView, TopUsersListApiView
from category.views import StoryCategoryListAPIView, StoryCategoryUpdateAPIView, StoryCategoryDestroyAPIView, \
    UserStoryCategoryListAPIView
from notification.views import UserNotificationsAPIView, NotificationAPIView, NotificationRefreshTokenAPIView
from auth_user.views import RegistrationAPIView, ProfileView, LoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    # story
    path('admin/', admin.site.urls),
    path('api/v1/stories/', StoryListAPIView.as_view()),
    path('api/v1/story/<int:pk>/', StoryUpdateAPIView.as_view()),
    path('api/v1/story/visible/<int:pk>', StoryVisibilityAPIView.as_view()),
    path('api/v1/story/delete/<int:pk>', StoryDestroyAPIView.as_view()),
    path('api/v1/stories/user', UserStoryListAPIView.as_view()),
    path('api/v1/stories/stats', UserStoryStatsListAPIView.as_view()),

    # view
    path('api/v1/story/views', StoryViewListApiView.as_view()),

    # quote
    path('api/v1/story/quotes', StoryQuoteListApiView.as_view()),

    # notification
    path('api/v1/user/notification', UserNotificationsAPIView.as_view()),
    path('api/v1/user/notification/send', NotificationAPIView.as_view()),
    path('api/v1/user/notification/refreshToken', NotificationRefreshTokenAPIView.as_view()),

    # report
    path('api/v1/stories/report', ReportStoryAPIView.as_view()),

    # top users
    path('api/v1/users/topusers', TopUsersListApiView.as_view()),
    # category
    path('api/v1/categories/', StoryCategoryListAPIView.as_view()),
    path('api/v1/user/categories/', UserStoryCategoryListAPIView.as_view()),
    path('api/v1/category/<int:pk>/', StoryCategoryUpdateAPIView.as_view()),
    path('api/v1/category/delete/<int:pk>', StoryCategoryDestroyAPIView.as_view()),

    # auth
    path('api/token/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/register/', RegistrationAPIView.as_view(), name='token_verify'),
    path('api/profile/', ProfileView.as_view(), name='profile'),

]
