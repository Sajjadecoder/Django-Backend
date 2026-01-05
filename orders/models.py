from django.db import models
import uuid
from users.models import User
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ("pending","Pending"),
        ("paid","Paid"),
        ("shipped","Shipped"),
        ("cancelled","Cancelled")
    )
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    def __str__(self):
        return f"Order {self.id} - User's email: {self.user.email}"
    