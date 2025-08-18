from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .utils import send_activation_email
from rest_framework.views import APIView
from .utils import confirm_activation_token

# Token endpoints seront ajoutés dans urls.py

from rest_framework.response import Response
from rest_framework import status

from .utils import generate_activation_token, send_activation_email

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import CustomUser
from .serializers import UserSerializer, UserRegistrationSerializer
from .utils import send_activation_email
import os

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_activation_email(user)
            return Response({
                'message': 'User registered successfully. Please check your email to activate your account.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({
                'error': 'Please provide both email and password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=email, password=password)
        
        if user is None:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({
                'error': 'Account is not activated. Please check your email.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Update last login IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        user.last_login_ip = ip
        user.save()
        
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request):
        user = request.user
        profile_image = request.FILES.get('profile_image')
        
        if not profile_image:
            return Response({
                'error': 'No image provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Delete old image if exists
        if user.profile_image:
            try:
                if os.path.isfile(user.profile_image.path):
                    os.remove(user.profile_image.path)
            except:
                pass
        
        # Save new image
        user.profile_image = profile_image
        user.save()
        
        serializer = UserSerializer(user)
        return Response({
            'message': 'Profile image updated successfully',
            'profile_image': user.profile_image.url,
            'user': serializer.data
        })

@api_view(['GET'])
def activate_account(request, token):
    try:
        user = CustomUser.objects.get(activation_token=token)
        user.is_active = True
        user.email_verified = True
        user.activation_token = None
        user.save()
        return Response({
            'message': 'Account activated successfully!'
        })
    except CustomUser.DoesNotExist:
        return Response({
            'error': 'Invalid activation token'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not old_password or not new_password:
        return Response({
            'error': 'Please provide both old and new passwords'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.check_password(old_password):
        return Response({
            'error': 'Current password is incorrect'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    
    return Response({
        'message': 'Password changed successfully'
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def resend_activation_email(request):
    user = request.user
    
    if user.is_active:
        return Response({
            'error': 'Account is already activated'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    send_activation_email(user)
    
    return Response({
        'message': 'Activation email sent successfully'
    })
