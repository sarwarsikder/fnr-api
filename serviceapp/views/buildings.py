from django.db.models import Count, Q, F
from rest_framework.permissions import BasePermission
from rest_framework import viewsets, mixins
from rest_framework.views import APIView

from adminapp.models import Buildings, BuildingPlans, BuildingComponents, Tasks
from rest_framework.pagination import PageNumberPagination
from serviceapp.serializers.building_serializer import BuildingSerializer, BuildingPlanSerializer, ComponentSerializer


class BuildingPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff and request.method == 'GET':
            return True
        return False


class BuildingViewSet(APIView):
    permission_classes = (BuildingPermissions,)

    def get(self, request, **kwargs):
        project_id = kwargs['project_id']
        paginator = PageNumberPagination()
        paginator.page_size = 10
        buildings = Buildings.objects.annotate(total_flats=Count('flats', distinct=True), total_tasks=Count('buildingcomponents__tasks', filter=Q(buildingcomponents__flat__isnull=True)), tasks_done=Count('buildingcomponents__tasks', filter=Q(buildingcomponents__tasks__status='done', buildingcomponents__flat__isnull=True))).filter(project_id=project_id)
        result_page = paginator.paginate_queryset(buildings, request)
        serializer = BuildingSerializer(result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)


class BuildingComponentViewSet(APIView):
    permission_classes = (BuildingPermissions,)

    def get(self, request, **kwargs):
        building_id = kwargs['building_id']
        paginator = PageNumberPagination()
        paginator.page_size = 10
        components = BuildingComponents.objects.annotate(name=F('component__name')).filter(building_id=building_id, flat__isnull=True, component__parent__isnull=True)
        # components = BuildingComponents.objects.annotate(name=F('component__name'), total_tasks=Count('tasks', filter=Q(Q(tasks__building_component__component__parent_id=F('component_id')) | Q(tasks__building_component__component_id=F('component_id'))))).filter(building_id=building_id, flat__isnull=True, component__parent__isnull=True)
        # for component in components:
        #     print(component.component_id)
        #     component.total_tasks = Tasks.objects.filter(building_component__flat__isnull=True).filter(Q(Q(building_component__component__parent_id=component.component_id) | Q(building_component__component_id=component.component_id)))
        #     print(component.total_tasks.query)
        #     component.total_tasks = Tasks.objects.filter(building_component__flat__isnull=True, status='done').filter(Q(Q(building_component__component__parent_id=component.component_id) | Q(building_component__component_id=component.component_id))).count()
        result_page = paginator.paginate_queryset(components, request)
        serializer = ComponentSerializer(result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)


class BuildingPlanViewSet(APIView):
    permission_classes = (BuildingPermissions, )

    def get(self, request, **kwargs):
        building_id = kwargs['building_id']
        paginator = PageNumberPagination()
        paginator.page_size = 10
        plans = BuildingPlans.objects.filter(building_id=building_id)
        result_page = paginator.paginate_queryset(plans, request)
        serializer = BuildingPlanSerializer(result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)
