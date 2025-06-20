from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class IsAuthenticatedOrReadonly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user and request.user.is_authenticated
    
class IsReader(BasePermission):  # Allows access only to authenticated users with 'reader' role
    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated): # Check if user is logged in
            return False
        # Safely check if user has a profile and role == 'reader'
        if hasattr(user, 'userprofile') and user.profile.role == 'reader':
            return True
        return False
    
class IsAuthor(BasePermission): # Allows access only to authenticated users with 'author' role
    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated): # Check if user is logged in
            return False
        return getattr(user, 'userprofile', None) and user.userprofile.role == 'author'  # Check if user has a profile and role is 'author'