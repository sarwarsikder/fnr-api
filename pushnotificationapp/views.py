from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=False, methods=['DELETE'], name='delete')
    def destroy_by_user(self, request, *args, **kwargs):
        user_id = request.POST['user_id']
        if user_id:
            queryset = Subscribers.objects.filter(user_id=user_id)
            self.perform_destroy(queryset)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PushNotificationViewSet(viewsets.ModelViewSet):
    queryset = PushNotification.objects.all()
    serializer_class = PushNotificationSerializer


    def get_queryset(self):
        user_id = self.request.GET.get("user_id")
        queryset = Subscribers.objects.all()
        if user_id:
            queryset = Subscribers.objects.filter(user_id=user_id)
        return queryset
