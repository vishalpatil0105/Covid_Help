from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse

CHOICES = (
    ("Plasma", "Plasma"),
    ("Oxygen", "Oxygen"),
    ("Bed", "Bed"),
    ("Emergency", "Emergency")
)

class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now) 
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    help_type = models.CharField(max_length=300, choices = CHOICES, null=True)
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comments(models.Model):
    post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    def get_absolute_url(self):
        return reverse('Home')
    

    