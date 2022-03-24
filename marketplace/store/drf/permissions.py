from rest_framework.permissions import IsAuthenticated


class ProductPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        if view.action == 'list' or view.action == 'retrieve':
            return True

        if view.action == 'create' and request.user.type == 'seller':
            return True

        return False


class OrderPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        if view.action == 'create' and request.user.type == 'buyer':
            return True

        return False
