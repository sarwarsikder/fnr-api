from django.conf import settings
from rest_framework import serializers
from adminapp.models import Buildings, BuildingPlans
from adminapp.views.common_views import CommonView


class BuildingSerializer(serializers.ModelSerializer):
    total_tasks = serializers.IntegerField(read_only=True)
    tasks_done = serializers.IntegerField(read_only=True)
    total_flats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Buildings
        fields = ('id', 'hause_number', 'description', 'display_number', 'total_tasks', 'tasks_done', 'total_flats')


class PlanSerializer(serializers.ModelSerializer):
    plan_file = serializers.SerializerMethodField()

    class Meta:
        model = BuildingPlans
        fields = ('id', 'title', 'plan_file', 'file_type')

    def get_plan_file(self, plan):
        if plan.plan_file and hasattr(plan.plan_file, 'url'):
            plan_file = plan.plan_file.url
            return CommonView.get_file_path(plan_file)
        else:
            return None
