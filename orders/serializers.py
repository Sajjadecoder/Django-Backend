from rest_framework import serializers
from .models import Order
from products.serializers import ProductSerializer
from users.serializers import MeSerializer
class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["product", "quantity"]

class OrderListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ["id", "product", "quantity", "total_price", "status", "created_at"]
        
class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        models = Order
        fields = ['status']
    def validate_status(self,val):
        if val not in ["pending","paid","shipped","cancelled"]:
            raise serializers.ValidationError("Invalid status")
        return val
        