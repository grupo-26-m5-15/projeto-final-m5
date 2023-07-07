from rest_framework import permissions


class IsLibraryEmployee(permissions.BasePermission):

    def has_object_permission(self, req, view, obj):        

        if req.method == "GET" and req.user["library_id"] == obj.id:
            return True

        if req.user["library_id"] == obj.id and req.user.is_superuser:
            return True

        return False
