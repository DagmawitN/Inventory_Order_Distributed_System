from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from messaging.events import publish_user_registered
from .serializers import UserSerializer,RegisterSerializer
from drf_yasg.utils import swagger_auto_schema


from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: "User registered"},
    )
    def post(self, request):
        data = request.data

        user = User.objects.create(
            username=data["username"],
            email=data.get("email", ""),
            password=make_password(data["password"]),
        )
        publish_user_registered(user)

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=201,
        )



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(security=[{"Bearer": []}])
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        return Response(UserSerializer(user).data)
