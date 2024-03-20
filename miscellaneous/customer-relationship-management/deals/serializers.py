from rest_framework import serializers
from .models import DefaultDealFields

class DefaultDealFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultDealFields
        fields = '__all__'
