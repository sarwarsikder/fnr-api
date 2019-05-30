from rest_framework import serializers

from pushnotificationapp.models import PushNotification, Subscribers


class SubscribersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribers
        fields = '__all__'


class PushNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushNotification
        fields = '__all__'
