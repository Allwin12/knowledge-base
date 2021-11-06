from rest_framework.permissions import BasePermission
from users.models import User
from rest_framework import exceptions


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        """
        Custom permission class that allows only author to access the API
        :param request:
        :param view:
        :return:
        """
        if request.user.is_authenticated and request.user.role == User.AUTHOR:
            return True
        raise exceptions.PermissionDenied(detail="Only author can perform this operation!")
