from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsModerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwnerOrStaff(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.owner == request.user
