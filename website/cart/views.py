from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import CartItem
from .serializers import CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage cart items.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Restrict the cart items to the logged-in user's cart
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the logged-in user with the cart item
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def clear_cart(self, request):
        """
        Custom action to clear the cart.
        """
        CartItem.objects.filter(user=request.user).delete()
        return Response({"message": "Cart cleared successfully."}, status=204)