from rest_framework import serializers
from adminapp.models import Projects, ProjectPlans


class ProjectSerializer(serializers.ModelSerializer):
    total_tasks = serializers.CharField(read_only=True)
    tasks_done = serializers.CharField(read_only=True)

    class Meta:
        model = Projects
        fields = ('id', 'address', 'description', 'city', 'type', 'energetic_standard', 'total_tasks', 'tasks_done')


class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectPlans
        fields = ('id', 'title', 'plan_file', 'file_type')
