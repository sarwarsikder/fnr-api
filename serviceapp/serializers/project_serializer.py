from django.conf import settings
from rest_framework import serializers
from adminapp.models import Projects, ProjectPlans
from adminapp.views.common_views import CommonView


class ProjectSerializer(serializers.ModelSerializer):
    total_tasks = serializers.CharField(read_only=True)
    tasks_done = serializers.CharField(read_only=True)

    class Meta:
        model = Projects
        fields = ('id', 'address', 'description', 'city', 'type', 'energetic_standard', 'total_tasks', 'tasks_done')


class PlanSerializer(serializers.ModelSerializer):
    plan_file = serializers.SerializerMethodField()

    class Meta:
        model = ProjectPlans
        fields = ('id', 'title', 'plan_file', 'file_type')

    def get_plan_file(self, plan):
        if plan.plan_file and hasattr(plan.plan_file, 'url'):
            plan_file = plan.plan_file.url
            return CommonView.get_file_path(plan_file)
        else:
            return None
