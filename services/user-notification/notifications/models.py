from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    type=models.CharField(max_length=50)
    content=models.TextField()
    status=models.CharField(max_length=20)
