from django.db import models
from authentication.models import User


class PlacementStatistics(models.Model):
    academic_year = models.CharField(max_length=20)
    total_students = models.IntegerField(default=0)
    students_placed = models.IntegerField(default=0)
    placement_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    branch_wise_stats = models.JSONField(default=dict, blank=True)
    average_package = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    highest_package = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    generated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'placement_statistics'
        ordering = ['-academic_year']


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    NOTIFICATION_TYPE_CHOICES = (
        ('APPLICATION', 'Application Update'),
        ('INTERVIEW', 'Interview Schedule'),
        ('JOB', 'New Job Posted'),
        ('APPROVAL', 'Account Approved'),
        ('SYSTEM', 'System Notification'),
    )
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
