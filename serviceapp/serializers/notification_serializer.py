from rest_framework import serializers
from adminapp.models import NotificationStatus


class NotificationSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    sending_at = serializers.CharField(max_length=100, read_only=True)

    class Meta:
        model = NotificationStatus
        fields = ('id', 'text', 'avatar', 'sending_at')

    def get_text(self, notification):
        return notification.notification.text

    def get_avatar(self, notification):
        return notification.user.avatar.url if notification.user.avatar else ''
