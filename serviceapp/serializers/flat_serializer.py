from django.conf import settings
from rest_framework import serializers
from adminapp.models import Flats, FlatPlans


class FlatSerializer(serializers.ModelSerializer):
    total_tasks = serializers.IntegerField(read_only=True)
    tasks_done = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flats
        fields = ('id', 'number', 'description', 'client_name', 'client_address', 'client_email', 'client_tel', 'total_tasks', 'tasks_done')


class FlatPlanSerializer(serializers.ModelSerializer):
    plan_file = serializers.SerializerMethodField()

    class Meta:
        model = FlatPlans
        fields = ('id', 'title', 'plan_file', 'file_type')

    def get_plan_file(self, plan):
        if plan.plan_file and hasattr(plan.plan_file, 'url'):
            plan_file = plan.plan_file.url
            return plan_file
        else:
            return None
