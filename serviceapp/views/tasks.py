from django.db.models import Q, F
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView

from adminapp.models import Tasks
from rest_framework.pagination import PageNumberPagination
from serviceapp.serializers.task_serializer import TaskSerializer


class TaskPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff and request.method == 'GET':
            return True
        return False


class BuildingTasksViewSet(APIView):
    permission_classes = (TaskPermissions,)

    def get(self, request, **kwargs):
        building_id = kwargs['building_id']
        component_id = kwargs['component_id']
        status = request.GET.get('type')
        paginator = PageNumberPagination()
        paginator.page_size = 10
        if status == 'pending':
            tasks = Tasks.objects.annotate(description=F('building_component__description')).filter(building_component__building_id=building_id, building_component__flat__isnull=True).filter(Q(Q(building_component__component__parent_id=component_id) | Q(building_component__component_id=component_id))).exclude(status='done')
        elif status == 'done':
            tasks = Tasks.objects.annotate(description=F('building_component__description')).filter(
                building_component__building_id=building_id,
                building_component__flat__isnull=True, status='done').filter(Q(
                Q(building_component__component__parent_id=component_id) | Q(
                    building_component__component_id=component_id)))
        else:
            tasks = Tasks.objects.annotate(description=F('building_component__description')).filter(building_component__building_id=building_id,
                                         building_component__flat__isnull=True).filter(Q(
                Q(building_component__component__parent_id=component_id) | Q(
                    building_component__component_id=component_id)))
        result_page = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)


class FlatTasksViewSet(APIView):
    permission_classes = (TaskPermissions,)

    def get(self, request, **kwargs):
        flat_id = kwargs['flat_id']
        component_id = kwargs['component_id']
        type = request.data.pop("type", None)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        if type == 'pending':
            tasks = Tasks.objects.annotate(description=F('building_component__description')).filter(building_component__flat_id=flat_id).filter(Q(Q(building_component__component__parent_id=component_id) | Q(building_component__component_id=component_id))).exclude(status='done')
        elif type == 'done':
            tasks = Tasks.objects.annotate(description=F('building_component__description')).filter(building_component__flat_id=flat_id, status='done').filter(Q(
                        Q(building_component__component__parent_id=component_id) | Q(
                            building_component__component_id=component_id)))
        else:
            tasks = Tasks.objects.annotate(description=F('building_component__description')).filter(building_component__flat_id=flat_id).filter(Q(
                        Q(building_component__component__parent_id=component_id) | Q(
                            building_component__component_id=component_id)))
        result_page = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)

