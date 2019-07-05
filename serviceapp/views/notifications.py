from rest_framework.permissions import BasePermission
from rest_framework.views import APIView

from adminapp.models import NotificationStatus, ProjectStuff
from rest_framework.pagination import PageNumberPagination
from serviceapp.serializers.notification_serializer import NotificationSerializer


class NotificationPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method == 'GET':
            return True
        return False


class NotificationsViewSet(APIView):
    permission_classes = (NotificationPermissions,)

    def get(self, request, **kwargs):
        notifications = NotificationStatus.objects.filter(user_id=request.user.id).order_by('-sending_at')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(notifications, request)
        serializer = NotificationSerializer(result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)
