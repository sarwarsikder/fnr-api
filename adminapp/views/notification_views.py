from django.views import generic
from adminapp.models import Notification, NotificationStatus
from adminapp.views.helper import LogHelper


class NotificationsView(generic.DetailView):
    def create_notfication(request, type, text, task_id, sending_by_id):
        try:
            notification_form = {
                "type": type,
                "text": text,
                "task_id": task_id,
                "sending_by_id": sending_by_id
            }
            notification = Notification(**notification_form)
            notification.save()
            NotificationsView.create_notification_user(request, notification.id)
        except Exception as e:
            LogHelper.efail(e)
        return

    def create_notification_user(request, notification_id):
        try:
            notification_user_form = {
                "user_id": 1,
                "notification_id": notification_id
            }
            notification_user = NotificationStatus(**notification_user_form)
            notification_user.save()
        except Exception as e:
            LogHelper.efail(e)
        return
