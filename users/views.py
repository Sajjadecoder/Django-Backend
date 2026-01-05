from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer,LoginSerializer,MeSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class= RegisterSerializer
    def post(self, req, *args,**kwargs):
        serializer = self.get_serializer(data=req.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({
            "message": 'User registered successfully',
            },
            status=status.HTTP_201_CREATED) 

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )

# users/views.py (temporary for browser testing)
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication

#DONOT USE THIS IN PRODUCTION
class JWTQueryParamAuthentication(JWTAuthentication):
    """
    Allow JWT to be passed as ?token=<access_token> for browser testing
    """
    def authenticate(self, request):
        token = request.query_params.get("token")
        if token:
            header = f"Bearer {token}"
            request.META["HTTP_AUTHORIZATION"] = header
        return super().authenticate(request)

#to check jwt is correctly working    
class MeView(APIView):
    authentication_classes = [JWTQueryParamAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,req):
        serializer = MeSerializer(req.user)
        return Response(serializer.data)
