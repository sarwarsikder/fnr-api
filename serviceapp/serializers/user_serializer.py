from rest_framework import serializers
from adminapp.models import Users


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=True)
    avatar = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    telephone = serializers.CharField(required=False, read_only=True)
    company_name = serializers.CharField(required=False, read_only=True)
    working_type = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = Users
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'avatar', 'address', 'telephone', 'company_name', 'working_type')

