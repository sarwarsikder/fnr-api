# from  django.db.models.signals import post_save
# from django.dispatch import receiver
# from pywebpush import webpush, WebPushException
# import logging
#
# from pushnotificationapp.models import PushNotification, Subscribers
#
#
# # @receiver(post_save, sender=Subscribers)
# def send_notification(sender, **kwargs):
#     # WEBPUSH_VAPID_PRIVATE_KEY = 'NLSiChEl9fXKpH4V0diB-FIzrsYTQZJI3t6m29cMoxU'
#     # count = 0
#     # subscription_info = {"endpoint":"https://fcm.googleapis.com/fcm/send/fsjbvwa06ik:APA91bFmUDOncHeDAY7tTSnd4QxatnnTqJXkrv8sB0r2LnPekNrRmMtAaEockO5XqEaQKUBipGpphQxRFkdfYVf38gy8fjcra7x2-M5eO0wfwWE2yEFJl0iuBpIiXdaCP_KsVh1lz3rY","expirationTime":None,"keys":{"p256dh":"BNDo7RaVN_DDd5tb-Yr-FU21hH-G8kNs_h1cOWGjp_I6um0dGoImR_m8mI7MXn8jqFowReDqD_5m3Pa8P3CmHIw","auth":"AMoKHDep1LCZeFfU2OS0Sw"}}
#     # data = kwargs.get('instance')
#     # subscription_info = {"endpoint":data.get('endpoint'),"expirationTime":data.get('expirationTime'),"keys":{"p256dh":data.get('p256dh'),"auth":data.get('auth')}}
#     #
#     print("Trigger Happened")
#     print(kwargs.get('instance')['id'])
#     print(kwargs.get('instance')['keys'])
#     try:
#         print("Trigger Happened 2 ")
#     #     webpush(
#     #         subscription_info=subscription_info,
#     #         data="Test 123",
#     #         vapid_private_key=WEBPUSH_VAPID_PRIVATE_KEY,
#     #         vapid_claims={
#     #             "sub": "mailto:webpush@mydomain.com"
#     #         }
#     #     )
#     #     count += 1
#
#     except WebPushException as e:
#         logging.exception("webpush fail")
#
#
# post_save.connect(send_notification, sender=Subscribers)
from django.core.signals import request_finished
from pywebpush import webpush, WebPushException
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from pushnotificationapp.models import PushNotification, Subscribers
import json
import os

@receiver(post_save, sender=PushNotification)
def send_notification(sender, **kwargs):
    print("Trigger Happened")
    # kwargs['instance'].id
    subscribers = Subscribers.objects.filter(user_id=kwargs['instance'].recipient)
    for subscriber in subscribers:
        print(subscriber.endpoint)
        print(subscriber.expirationTime)
        print(subscriber.keys)
        subscription_info = {"endpoint": subscriber.endpoint,"keys": json.loads(subscriber.keys)}
        print(subscription_info)
        notification_sender(subscription_info, kwargs['instance'].message)

    print("Trigger Happened 2")


def notification_sender(subscription_info, data):
    # WEBPUSH_VAPID_PRIVATE_KEY = '8KWSbR9D9vWmEjVIdZDBqttPu9cUDNIDAo95xKAXE6I'

    count = 0
    DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH = os.path.abspath('private_key.txt')
    DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH = os.path.abspath('public_key.txt')
    VAPID_PRIVATE_KEY = open(DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH, "r+").readline().strip("\n")
    VAPID_PUBLIC_KEY = open(DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH, "r+").read().strip("\n")
    VAPID_CLAIMS = {
        "sub": "mailto:iftekhar@workspaceit.com",
    }

    # subscription_info = {"endpoint":"https://fcm.googleapis.com/fcm/send/fsjbvwa06ik:APA91bFmUDOncHeDAY7tTSnd4QxatnnTqJXkrv8sB0r2LnPekNrRmMtAaEockO5XqEaQKUBipGpphQxRFkdfYVf38gy8fjcra7x2-M5eO0wfwWE2yEFJl0iuBpIiXdaCP_KsVh1lz3rY","expirationTime":None,"keys":{"p256dh":"BNDo7RaVN_DDd5tb-Yr-FU21hH-G8kNs_h1cOWGjp_I6um0dGoImR_m8mI7MXn8jqFowReDqD_5m3Pa8P3CmHIw","auth":"AMoKHDep1LCZeFfU2OS0Sw"}}
    subscription_info = subscription_info
    try:
        webpush(
            subscription_info=subscription_info,
            data=data,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS
        )
        count += 1
    except WebPushException as e:
        logging.exception("webpush fail")
