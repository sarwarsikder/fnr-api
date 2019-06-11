from django.db import models


class Subscribers(models.Model):
    endpoint = models.TextField(max_length=2000)
    expirationTime = models.DateTimeField(null=True)
    keys = models.TextField(max_length=2000)
    user_id = models.IntegerField(null=False)
    device  = models.CharField(max_length=512)

class PushNotification(models.Model):
    recipient = models.IntegerField(null=False)
    title = models.CharField(max_length=512, null=True, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=10, default='unread')
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)

