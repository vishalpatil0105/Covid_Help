from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from .models import CHOICES

class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length = 100)
    content = serializers.CharField()
    date = serializers.DateTimeField(default=timezone.now) 
    help_type = serializers.CharField()
        