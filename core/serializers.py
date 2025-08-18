from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'phone_number', 'role', 'profile_image', 'language', 'bio',
            'date_of_birth', 'address', 'city', 'country', 'postal_code',
            'is_active', 'email_verified', 'phone_verified', 'last_login_ip',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_active', 'email_verified', 'phone_verified', 
                           'last_login_ip', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add computed properties
        data['display_name'] = instance.display_name
        data['full_name'] = instance.full_name
        data['profile_image_url'] = instance.profile_image_url
        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'confirm_password',
            'first_name', 'last_name', 'phone_number', 'role',
            'language', 'bio', 'date_of_birth', 'address', 'city',
            'country', 'postal_code'
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            role=validated_data.get('role', 'client'),
            language=validated_data.get('language', 'fr'),
            bio=validated_data.get('bio', ''),
            date_of_birth=validated_data.get('date_of_birth'),
            address=validated_data.get('address', ''),
            city=validated_data.get('city', ''),
            country=validated_data.get('country', ''),
            postal_code=validated_data.get('postal_code', ''),
            is_active=False  # User must activate account
        )
        return user

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'phone_number',
            'language', 'bio', 'date_of_birth', 'address', 'city',
            'country', 'postal_code'
        ]

    def validate_username(self, value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(id=user.id).filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà pris")
        return value

class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_image']

    def validate_profile_image(self, value):
        # Validate file size (max 5MB)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("L'image ne doit pas dépasser 5MB")
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/gif']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Format d'image non supporté. Utilisez JPEG, PNG ou GIF")
        
        return value
