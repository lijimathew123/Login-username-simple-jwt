from rest_framework import serializers

from .models import Role,CustomerRole


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields = '__all__'



class CustomerRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRole
        fields = '__all__'