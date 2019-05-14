from rest_framework import serializers
from adminapp.models import Users


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=True)
    avatar = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = Users
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'avatar', 'address')

