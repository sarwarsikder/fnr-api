from pywebpush import webpush, WebPushException
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

from adminapp.models import Users
from pushnotificationapp.models import PushNotification, Subscribers
import json
import os
import datetime
from notifications.signals import notify


def notification_sender(subscription_info, data):
    count = 0
    VAPID_CLAIMS = {
        "exp":  1212121212,
        "sub": "mailto:iftekhar@workspaceit.com"
    }

    subscription_info = subscription_info
    try:
        webpush(
            subscription_info=subscription_info,
            data=data,
            vapid_private_key="bF0oatL1tc0-vPr_9Lx8VMUmXA4Fgp_dJaQMpZk25ag",
            vapid_claims = VAPID_CLAIMS
        )
        count += 1
    except WebPushException as e:
        logging.exception("webpush fail")


@receiver(post_save, sender=PushNotification)
def send_notification(sender, **kwargs):
    subscribers = Subscribers.objects.filter(user_id=kwargs['instance'].recipient)
    for subscriber in subscribers:
        subscription_info = {"endpoint": subscriber.endpoint,"keys": json.loads(subscriber.keys)}
        notification_sender(subscription_info, kwargs['instance'].message)
        user = Users.objects.filter(id=kwargs['instance'].recipient)[0]
        notify.send(user, recipient=user, verb='you reached level 10')



