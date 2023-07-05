
from rest_framework.permissions import BasePermission
from .models import User


class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'librarain'


