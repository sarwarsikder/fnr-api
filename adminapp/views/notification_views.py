import json

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import generic
from adminapp.models import Notification, NotificationStatus, BuildingComponents, ProjectStuff
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
            NotificationsView.create_notification_user(request, notification)
        except Exception as e:
            LogHelper.efail(e)
        return


    # Notification will send to
    # Assigned user
    # All staffs of this project
    # All followers

    def create_notification_user(request, notification):
        try:
            notification_users = []
            assigned_user = BuildingComponents.objects.filter(component_id=notification.task.building_component.component.parent_id,
                                                               building_id=notification.task.building_component.building_id,
                                                               flat_id=notification.task.building_component.flat_id).first()
            if assigned_user.assign_to:
                notification_user_form = {
                    "user_id": assigned_user.assign_to.id,
                    "notification_id": notification.id
                }
                notification_users.append(NotificationStatus(**notification_user_form))
            staffs = ProjectStuff.objects.filter(project_id=notification.task.building_component.building.project_id, user__is_active=True)
            for staff in staffs:
                notification_user_form = {
                    "user_id": staff.user_id,
                    "notification_id": notification.id
                }
                notification_users.append(NotificationStatus(**notification_user_form))
            followers = notification.task.followers
            if followers:
                for follower in followers:
                    notification_user_form = {
                        "user_id": follower['id'],
                        "notification_id": notification.id
                    }
                    notification_users.append(NotificationStatus(**notification_user_form))
            NotificationStatus.objects.bulk_create(notification_users)
        except Exception as e:
            LogHelper.efail(e)
        return

    def get_new_notifications(request):
        response = {}
        try:
            notification_list = []
            notifications = NotificationStatus.objects.filter(user_id=request.user.id).order_by('status')[:5]
            for notification in notifications:
                notification_data = {
                    "avatar": notification.notification.sending_by.avatar.url if notification.notification.sending_by.avatar else '',
                    "message": notification.notification.text,
                    "task_id": notification.notification.task_id,
                    "sending_time": str(notification.sending_at)
                }
                notification_list.append(notification_data)
            unread_notifications = NotificationStatus.objects.filter(user_id=request.user.id, status=False).count()
            new_notifications = False
            if NotificationStatus.objects.filter(user_id=request.user.id, is_sent=False).count() > 0:
                new_notifications = True
            NotificationStatus.objects.filter(user_id=request.user.id).update(is_sent=True)
            response['success'] = True
            response['notifications'] = notification_list
            response['unread_notifications'] = unread_notifications
            response['new_notifications'] = new_notifications
        except Exception as e:
            LogHelper.efail(e)
            response['success'] = False
            response['message'] = "Something went wrong. Please try again"
        return HttpResponse(json.dumps(response), content_type='application/json')

    def read_notification(request, task_id):
        try:
            NotificationStatus.objects.filter(user_id=request.user.id, notification__task_id=task_id).update(status=True)
        except Exception as e:
            LogHelper.efail(e)
