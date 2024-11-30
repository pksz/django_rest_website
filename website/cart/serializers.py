from rest_framework import serializers
from .models import CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'product_name', 'product_price', 'quantity']
        extra_kwargs = {
            'user': {'read_only': True},  # Automatically set the user in the view
        }