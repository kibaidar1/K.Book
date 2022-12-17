from rest_framework import permissions
from rest_framework.permissions import BasePermission

from .models import Book


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return request.user == obj.author


class IsPageAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return request.user == obj.book.author

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        obj = Book.objects.get(slug=view.kwargs['book_slug'])
        return obj.author == request.user


