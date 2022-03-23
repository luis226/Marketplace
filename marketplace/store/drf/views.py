from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from store.models import Product, User
from store.drf.serializers import CreateUserSerializer, ProductSerializer


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
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    