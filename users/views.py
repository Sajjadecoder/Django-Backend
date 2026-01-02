from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class= RegisterSerializer
    def post(self, req, *args,**kwargs):
        serializer = self.get_serializer(data=req.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({
            "message": 'User registered successfully',
            },
            status=status.HTTP_201_CREATED) 