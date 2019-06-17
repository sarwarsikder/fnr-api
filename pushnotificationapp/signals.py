from pywebpush import webpush, WebPushException
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from adminapp.models import Users
from pushnotificationapp.models import Subscribers
from adminapp.models import NotificationStatus
import json
from pyfcm import FCMNotification
from notifications.signals import notify


def notification_sender(subscription_info, data):
    count = 0
    VAPID_CLAIMS = {
        "exp": 1212121212,
        "sub": "mailto:iftekhar@workspaceit.com"
    }

    subscription_info = subscription_info
    try:
        webpush(
            subscription_info=subscription_info,
            data=data,
            vapid_private_key="bF0oatL1tc0-vPr_9Lx8VMUmXA4Fgp_dJaQMpZk25ag",
            vapid_claims=VAPID_CLAIMS
        )
        count += 1
    except WebPushException as e:
        logging.exception("webpush fail")


@receiver(post_save, sender=NotificationStatus)
def send_notification(sender, **kwargs):
    try:
        subscribers = Subscribers.objects.filter(user_id=kwargs['instance'].user_id)
        for subscriber in subscribers:
            if subscriber.device == "mobile":
                push_service = FCMNotification(api_key="AIzaSyDe760rQNsg6JOJbohxdrYTW86E9FtDSyw")
                registration_id = "d7mMlK4FKR4:APA91bGCnJ-fPmlmvRDJTnTBTeg7-ZSeUh-puqrSHdAShkNIZEJrF5c2pTcadmU5rioks8aOIwek9oFKCxI0jIJXC1I19gMhyyD3gnGOU0eTeo8SDjkGTejxjYyDYww7d5t77yqsruUs"
                result = push_service.notify_single_device(registration_id=registration_id,
                                                           message_title="Notification title",
                                                           message_body=kwargs['instance'].notification.text)

            else:
                subscription_info = {"endpoint": subscriber.endpoint, "keys": json.loads(subscriber.keys)}
                notification_sender(subscription_info, kwargs['instance'].notification.text)
        # user = Users.objects.get(id=kwargs['instance'].user_id)
        # print(user)
        # avatar = kwargs['instance'].notification.sending_by.avatar.url if kwargs['instance'].notification.sending_by.avatar else ''
        # notify.send(kwargs['instance'].notification.sending_by, recipient=user, verb=kwargs['instance'].notification.text, description=avatar, target=kwargs['instance'].notification.task)
    except Exception as e:
        print(e)
