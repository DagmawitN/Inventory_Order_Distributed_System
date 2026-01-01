from django.contrib import admin
from django.urls import path
from users.views import RegisterView, UserProfileView
from notifications.views import SendNotificationView
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="User & Notification API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/register', RegisterView.as_view()),
    path('users/login', TokenObtainPairView.as_view()),
    path('users/<int:pk>', UserProfileView.as_view()),
    path('notifications/send', SendNotificationView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
