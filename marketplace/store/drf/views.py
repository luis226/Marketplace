from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from store.drf.permissions import ProductPermission, OrderPermission
from store.models import Product, User, Order
from store.drf.serializers import CreateUserSerializer, ProductSerializer, OrderSerializer


class UserView(generics.CreateAPIView):
    # There is no permission_class because a user can be registered 
    # annonymusly
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    '''
    TODO: The user will only be able to see the items in the shop 
    unless he creates an account first. I think the user should be able
    to take a look at the store items before creating an account.
    '''
    permission_classes = [ProductPermission]

    def get_queryset(self):
        # Seller user only see his products, buyer can see all active products
        queryset = super().get_queryset()
        if self.request.user.type == 'seller':
            queryset = queryset.filter(selled_by=self.request.user)
        else:
            queryset = queryset.filter(is_active=True)
        return queryset


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    permission_classes = [OrderPermission]

    def get_queryset(self):
        # Seller can only see orders of his products, buyer only his orders
        queryset = super().get_queryset()
        if self.request.user.type == 'buyer':
            queryset = queryset.filter(buyer=self.request.user)
        else:
            queryset = queryset.filter(product__seller=self.request.user)

        return queryset

    def perform_create(self, serializer):
        return serializer.save(status='cart')
