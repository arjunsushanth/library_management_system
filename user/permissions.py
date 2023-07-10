
from rest_framework.permissions import BasePermission

class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.user_type == 'librarian')
    






