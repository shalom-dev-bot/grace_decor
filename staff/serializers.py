from rest_framework import serializers
from .models import StaffMember
from core.serializers import UserSerializer

class StaffMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StaffMember
        fields = '__all__'
