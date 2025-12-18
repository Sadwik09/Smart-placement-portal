"""
Utility functions and helpers for the backend
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination class"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class IsStudent(BasePermission):
    """Permission class to check if user is a student"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'student'


class IsRecruiter(BasePermission):
    """Permission class to check if user is a recruiter"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'recruiter'


class IsAdmin(BasePermission):
    """Permission class to check if user is an admin"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class IsOwnerOrAdmin(BasePermission):
    """Permission class to check if user is owner or admin"""
    
    def has_object_permission(self, request, view, obj):
        # Admin can access anything
        if request.user.role == 'admin':
            return True
        
        # Check if object has a user field and user is the owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if object has a student field and user is the student
        if hasattr(obj, 'student'):
            return obj.student.user == request.user
        
        # Check if object has a recruiter field and user is the recruiter
        if hasattr(obj, 'recruiter'):
            return obj.recruiter.user == request.user
        
        return False
