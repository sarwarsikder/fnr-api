from django.conf import settings
from rest_framework import serializers
from adminapp.models import Buildings, BuildingPlans, BuildingComponents


class BuildingSerializer(serializers.ModelSerializer):
    total_tasks = serializers.IntegerField(read_only=True, default=None)
    tasks_done = serializers.IntegerField(read_only=True,  default=None)
    total_flats = serializers.IntegerField(read_only=True,  default=None)

    class Meta:
        model = Buildings
        fields = ('id', 'hause_number', 'description', 'display_number', 'total_tasks', 'tasks_done', 'total_flats')


class BuildingPlanSerializer(serializers.ModelSerializer):
    plan_file = serializers.SerializerMethodField()

    class Meta:
        model = BuildingPlans
        fields = ('id', 'title', 'plan_file', 'file_type')

    def get_plan_file(self, plan):
        if plan.plan_file and hasattr(plan.plan_file, 'url'):
            plan_file = plan.plan_file.url
            return plan_file
        else:
            return None


class ComponentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, read_only=True)
    total_tasks = serializers.IntegerField(read_only=True, default=None)
    tasks_done = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = BuildingComponents
        fields = ('component_id', 'name', 'total_tasks', 'tasks_done')
