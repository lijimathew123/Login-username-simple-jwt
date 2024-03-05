from rest_framework import serializers
from .models import Employee

class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('username','email', 'password')
        extra_kwargs = {'password': {'write_only': True}}



class EmployeeLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



    
