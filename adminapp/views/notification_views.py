from django.views import generic
from adminapp.models import Notification
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

        except Exception as e:
            LogHelper.efail(e)
        return








