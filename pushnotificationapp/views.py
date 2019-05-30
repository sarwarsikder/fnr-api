from rest_framework import viewsets
from pushnotificationapp.models import Subscribers, PushNotification
from pushnotificationapp.serializers import SubscribersSerializer, PushNotificationSerializer


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscribers.objects.all()
    serializer_class = SubscribersSerializer


    def get_queryset(self):
        user_id = self.request.GET.get("user_id")
        queryset = Subscribers.objects.all()
        if user_id:
            queryset = Subscribers.objects.filter(user_id=user_id)
        return queryset

class PushNotificationViewSet(viewsets.ModelViewSet):
    queryset = PushNotification.objects.all()
    serializer_class = PushNotificationSerializer


    def get_queryset(self):
        user_id = self.request.GET.get("user_id")
        queryset = Subscribers.objects.all()
        if user_id:
            queryset = Subscribers.objects.filter(user_id=user_id)
        return queryset
