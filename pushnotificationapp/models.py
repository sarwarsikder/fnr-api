from django.db import models
from django.db.models import CASCADE
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

class Subscribers(models.Model):
    endpoint = models.TextField(max_length=2000)
    expirationTime = models.DateTimeField(null=True)
    # p256dh = models.TextField(max_length=2000)
    # auth = models.TextField(max_length=500)
    keys = models.TextField(max_length=2000)


class PushNotification(models.Model):
    recipient = models.ForeignKey(Subscribers, on_delete=CASCADE)
    title = models.CharField(max_length=512, null=True, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=10, default='unread')
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)


@receiver(post_save, sender=Subscribers)
def send_notification(sender, **kwargs):
    print("Trigger Happened")
    print(kwargs['instance']['id'])
    print(kwargs['instance']['keys'])
    print("Trigger Happened 2")

# pre_save.connect(send_notification, sender= Subscribers)
#
# post_save.connect(send_notification, sender= Subscribers)