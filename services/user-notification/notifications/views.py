
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from drf_yasg.utils import swagger_auto_schema 

class SendNotificationView(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(security=[{'Bearer': []}])
    def post(self, request):
        Notification.objects.create(**request.data, status='sent')
        return Response({'message': 'sent'})