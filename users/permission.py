from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import BloodSecretary,Secretary, Member

class SecretaryPermission(BasePermission):
    """
    Custom permission to check if the user has the 'secretary' role.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to access this")

        # Check if the user has a related Secretary instance
        try:
            secretary = Secretary.objects.get(user=request.user)
            return True  # If the user has a related Secretary, permission is granted
        except Secretary.DoesNotExist:
            pass
        
        raise PermissionDenied("You must be a secretary to access this")


class BloodSecretaryPermission(BasePermission):
    """
    Custom permission to check if the user has the 'blood_secretary' role.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to access this")

        # Check if the user has the 'blood_secretary' role
        try:
            blood_secretary = BloodSecretary.objects.get(user=request.user)
            if blood_secretary.role.role == 'blood_secretary':
                return True
        except BloodSecretary.DoesNotExist:
            pass
        
        raise PermissionDenied("You must be a blood secretary to access this")
    

class MemberPermission(BasePermission):
    """
    Custom permission to check if the user has the 'member' role.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to access this")

        # Check if the user has a related Member instance
        try:
            member = Member.objects.get(user=request.user)
            return True  # If the user has a related Member, permission is granted
        except Member.DoesNotExist:
            pass
        
        raise PermissionDenied("You must be a member to access this")

