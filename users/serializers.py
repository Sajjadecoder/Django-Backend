from rest_framework import serializers
from .models import User

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
