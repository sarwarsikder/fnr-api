from django.db.models import Count, Q
from rest_framework.permissions import BasePermission
from rest_framework import viewsets, mixins
from rest_framework.views import APIView

from adminapp.models import Buildings, BuildingPlans
from rest_framework.pagination import PageNumberPagination
from serviceapp.serializers.building_serializer import BuildingSerializer, PlanSerializer


class StaffPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff and request.method == 'GET':
            return True
        return False


class BuildingViewSet(APIView):
    permission_classes = (StaffPermissions,)

    def get(self, request, **kwargs):
        project_id = kwargs['project_id']
        paginator = PageNumberPagination()
        paginator.page_size = 2
        buildings = Buildings.objects.annotate(total_flats=Count('flats', distinct=True), total_tasks=Count('buildingcomponents__tasks', filter=Q(buildingcomponents__flat__isnull=True)), tasks_done=Count('buildingcomponents__tasks', filter=Q(buildingcomponents__tasks__status='done', buildingcomponents__flat__isnull=True))).filter(project_id=project_id)
        result_page = paginator.paginate_queryset(buildings, request)
        serializer = BuildingSerializer(result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)


class BuildingPlanViewSet(APIView):
    permission_classes = (StaffPermissions, )

    def get(self, request, **kwargs):
        building_id = kwargs['building_id']
        paginator = PageNumberPagination()
        paginator.page_size = 2
        plans = BuildingPlans.objects.filter(building_id=building_id)
        result_page = paginator.paginate_queryset(plans, request)
        serializer = PlanSerializer(result_page, many=True)
        return paginator.get_paginated_response(data=serializer.data)
