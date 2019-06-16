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
