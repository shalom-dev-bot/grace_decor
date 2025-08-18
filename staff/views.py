from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import StaffMember
from .serializers import StaffMemberSerializer

class StaffMemberViewSet(viewsets.ModelViewSet):
    queryset = StaffMember.objects.all()
    serializer_class = StaffMemberSerializer
