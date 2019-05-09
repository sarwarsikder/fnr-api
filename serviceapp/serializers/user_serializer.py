from rest_framework import serializers
from adminapp.models import Users


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.CharField(required=True)
    avatar = serializers.CharField(read_only=True)

    class Meta:
        model = Users
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'avatar')

