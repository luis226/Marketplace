from rest_framework.permissions import IsAuthenticated


class ProductPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        if request.method == 'GET':
            return True

        if request.action == 'POST ' and request.user.type == 'seller':
            return True

        return False


class OrderPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        if request.method == 'POST' and request.user.type == 'buyer':
            return True

        if request.method == 'GET':
            return True

        return False
