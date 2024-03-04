from rest_framework import serializers
from .models import Employee

class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class EmployeeLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()