from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True)
    password2 = serializers.CharField(write_only=True,required=True)
    class Meta:
        model = User
        fields = ('email','full_name','password','password2')
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Pw donot match')
        return attrs
    def create(self,validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            email = validated_data['email'],
            full_name = validated_data.get('full_name',''),
            password = validated_data['password'],
            )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password= serializers.CharField(write_only=True)
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email,password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('Account isnt active')
        
        refresh = RefreshToken.for_user(user)
        refresh['email'] = user.email
        refresh['full_name'] = user.full_name
        refresh['user_id'] = str(user.id)
        
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": str(user.id),
                "full_name": user.full_name,
                "email": user.email
            }
        }        
        
class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','full_name','date_joined')
    