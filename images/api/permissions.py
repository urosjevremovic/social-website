from rest_framework.permissions import BasePermission


class CanViewImage(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.filter(id=request.user.id).exists()
