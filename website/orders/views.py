from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from cart.models import CartItem

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle order creation and retrieval.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Restrict orders to the logged-in user
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user

        # Get cart items for the user
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total price
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Create order
        order = serializer.save(user=user, total_price=total_price)

        # Create order items and clear the cart
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        cart_items.delete()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
