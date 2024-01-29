from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):

    message = 'невозможно выполнить действие'

    def has_permission(self, request, view):
        if request.user.role == 'moderator':
            return False
        return True


class IsUser(BasePermission):
    message = 'невозможно выполнить действие'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False