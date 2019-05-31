from django.conf import settings
from rest_framework import serializers
from adminapp.models import Tasks


class TaskSerializer(serializers.ModelSerializer):
    due_date = serializers.CharField(max_length=100, read_only=True)
    created_by_id = serializers.IntegerField(read_only=True)
    updated_by_id = serializers.IntegerField(read_only=True)
    created_at = serializers.CharField(max_length=100, read_only=True)
    updated_at = serializers.CharField(max_length=100, read_only=True)
    description = serializers.CharField(max_length=1000, read_only=True)

    class Meta:
        model = Tasks
        fields = ('id', 'description', 'due_date', 'created_by_id', 'updated_by_id', 'created_at', 'updated_at')
