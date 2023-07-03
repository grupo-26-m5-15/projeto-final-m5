from rest_framework import permissions
from .models import User
from libraries.models import LibraryEmployee
from rest_framework.views import View


class IsAdminOrEmployee(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        try:
            employee_user = LibraryEmployee.objects.get(employee=request.user)
        except LibraryEmployee.DoesNotExist:
            return False

        return request.user.is_superuser or employee_user.is_employee


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        try:
            employee_user = LibraryEmployee.objects.get(employee=request.user)
        except LibraryEmployee.DoesNotExist:
            return False

        return (
            request.user.is_superuser
            or employee_user.is_employee
            or obj == request.user
        )
