from rest_framework.permissions import BasePermission

class IsDoctor(BasePermission):
    """
    Allows access only to users with the role 'doctor'.
    """
    def has_permission(self, request, view):
        return request.user.role == 'doctor'

class IsPatient(BasePermission):
    """
    Allows access only to users with the role 'patient'.
    """
    def has_permission(self, request, view):
        return request.user.role == 'patient'
