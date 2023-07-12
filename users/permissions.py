from rest_framework import permissions
from .models import User
from libraries.models import LibraryEmployee
from rest_framework.views import View


class IsAdminOrEmployee(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
        if request.user.is_authenticated and request.user.is_superuser:
            return True

        try:
            employee_user = LibraryEmployee.objects.get(employee=request.user)
        except LibraryEmployee.DoesNotExist:
            return False

        return request.user.is_authenticated and employee_user.is_employee


class IsAccountOwnerOrAdminOrEmployee(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        if request.user.is_authenticated and request.user.is_superuser:
            return True

        if request.user.is_authenticated and obj == request.user:
            return True

        try:
            employee_user = LibraryEmployee.objects.get(employee=request.user)
        except LibraryEmployee.DoesNotExist:
            return False

        return request.user.is_authenticated and employee_user.is_employee


class IsAccountOwnerOrAdminOrEmployeeFollow(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        if request.user.is_authenticated and request.user.is_superuser:
            return True

        if request.user.is_authenticated and obj.user == request.user:
            return True

        try:
            employee_user = LibraryEmployee.objects.get(employee=request.user)
        except LibraryEmployee.DoesNotExist:
            return False

        return request.user.is_authenticated and employee_user.is_employee


class IsAccountOwnerFollow(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return request.user.is_authenticated and obj.user == request.user


class SafeAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_authenticated:
            return True
