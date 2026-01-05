from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from .serializers import OrderCreateSerializer,OrderListSerializer,OrderStatusUpdateSerializer
from products.models import Product
class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]
        
        total_price = product.price *quantity
        
        order = Order.objects.create(
            product= product,
            quantity= quantity,
            total_price = total_price,
            user = request.user
        )
        
        return Response({"message": "Order created successfully"},status=status.HTTP_201_CREATED)
    
class MyOrderListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,req):
        orders = Order.objects.filter(user = req.user)
        serializer = OrderListSerializer(orders,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class AllOrdersListView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    
    def get(self,req):
        orders = Order.objects.all()
        serializer = OrderListSerializer(orders,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class OrderStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    
    def patch(self,req,pk):
        order = get_object_or_404(Order,pk=pk)
        serializer = OrderStatusUpdateSerializer(order,data=req.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"message": f"Status updated successfully to {serializer.data["status"]}"})