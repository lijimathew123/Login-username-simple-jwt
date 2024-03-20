from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DefaultDealFields
from .serializers import DefaultDealFieldsSerializer

class DefaultDealFieldsAPIView(APIView):
    def get(self, request):
        default_deal_fields = DefaultDealFields.objects.all()
        serializer = DefaultDealFieldsSerializer(default_deal_fields, many=True)
        return Response(serializer.data)
