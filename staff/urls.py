from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StaffMemberViewSet

router = DefaultRouter()
router.register(r'staff', StaffMemberViewSet, basename='staff')

urlpatterns = [
    path('', include(router.urls)),
]
