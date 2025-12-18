from django.db import models
from authentication.models import User


class Student(models.Model):
    """Student profile model"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    
    BRANCH_CHOICES = (
        ('CSE', 'Computer Science Engineering'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
        ('OTHER', 'Other'),
    )
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)
    
    YEAR_CHOICES = (
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
    )
    year = models.IntegerField(choices=YEAR_CHOICES)
    
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    phone = models.CharField(max_length=15)
    skills = models.JSONField(default=list, blank=True)
    
    linkedin = models.URLField(max_length=255, blank=True, null=True)
    github = models.URLField(max_length=255, blank=True, null=True)
    portfolio = models.URLField(max_length=255, blank=True, null=True)
    
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    
    profile_completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.roll_number})"
    
    class Meta:
        db_table = 'students'
        ordering = ['-created_at']
