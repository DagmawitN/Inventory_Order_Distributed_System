from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model=User
    fields=('id','username','email','role')
