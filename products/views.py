from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Product
from .serializers import ProductSerializer
from rest_framework import status
# Create your views here.
class ProductListView(APIView):
    permission_classes = [AllowAny]
    def get(self,req):
        products = Product.objects.all()
        serializer = ProductSerializer(products,many = True)
        return Response(serializer.data)
    def post(self,req):
        
        if not req.user.is_staff:
            return Response({
                "detail": "You are not permitted to create/add products"
            },status=status.HTTP_403_FORBIDDEN)
       
        serializer = ProductSerializer(data=req.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)