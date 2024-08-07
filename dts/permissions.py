from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.groups.filter(name='superuser').exists():
            return True
        else:
            raise PermissionDenied(detail="Anda tidak memiliki hak akses untuk menu ini.")  

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and (user.groups.filter(name='admin').exists() or user.groups.filter(name='superuser').exists()):
            return True
        else:
            raise PermissionDenied(detail="Anda tidak memiliki hak akses untuk menu ini.") 
        
class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and (user.groups.filter(name='admin').exists() or user.groups.filter(name='superuser').exists() or user.groups.filter(name='staff').exists()):
            return True
        else:
            raise PermissionDenied(detail="Anda tidak memiliki hak akses untuk menu ini.")

class IsStaffView(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and (user.groups.filter(name='admin').exists() or user.groups.filter(name='superuser').exists() or user.groups.filter(name='staff view').exists()):
            return True
        else:
            raise PermissionDenied(detail="Anda tidak memiliki hak akses untuk menu ini.")

class IsStaffAndView(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and (user.groups.filter(name='admin').exists() or user.groups.filter(name='superuser').exists() or user.groups.filter(name='staff view').exists() or user.groups.filter(name='staff').exists()):
            return True
        else:
            raise PermissionDenied(detail="Anda tidak memiliki hak akses untuk menu ini.")