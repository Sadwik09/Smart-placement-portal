from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from django.utils import timezone
from authentication.models import User
from students.models import Student
from jobs.models import Job, Application
from .models import Notification
from placement_portal.permissions import IsAdmin


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        total_users = User.objects.count()
        pending_approvals = User.objects.filter(is_approved=False).count()
        total_students = Student.objects.count()
        total_jobs = Job.objects.count()
        active_jobs = Job.objects.filter(is_active=True).count()
        total_applications = Application.objects.count()
        
        return Response({
            'users': {'total': total_users, 'pending_approvals': pending_approvals, 'students': total_students},
            'jobs': {'total': total_jobs, 'active': active_jobs},
            'applications': {'total': total_applications},
        })


class UserApprovalView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        pending_users = User.objects.filter(is_approved=False)
        users_data = [{'id': u.id, 'email': u.email, 'role': u.role} for u in pending_users]
        return Response(users_data)
    
    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.is_approved = True
            user.save()
            Notification.objects.create(user=user, notification_type='APPROVAL', title='Account Approved', message='Your account has been approved.')
            return Response({'message': 'User approved'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


class PlacementStatisticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        total_students = Student.objects.count()
        placed_students = Application.objects.filter(status='SELECTED').values('student').distinct().count()
        placement_percentage = (placed_students / total_students * 100) if total_students > 0 else 0
        
        return Response({
            'total_students': total_students,
            'placed_students': placed_students,
            'placement_percentage': round(placement_percentage, 2),
        })
