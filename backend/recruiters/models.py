from django.db import models
from authentication.models import User


class Recruiter(models.Model):
    """Recruiter/Company profile model"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=255)
    company_description = models.TextField(blank=True, null=True)
    
    INDUSTRY_CHOICES = (
        ('IT', 'Information Technology'),
        ('FINANCE', 'Finance & Banking'),
        ('HEALTHCARE', 'Healthcare'),
        ('EDUCATION', 'Education'),
        ('ECOMMERCE', 'E-commerce'),
        ('MANUFACTURING', 'Manufacturing'),
        ('CONSULTING', 'Consulting'),
        ('STARTUP', 'Startup'),
        ('OTHER', 'Other'),
    )
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    
    website = models.URLField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    
    company_size = models.CharField(max_length=50, blank=True, null=True)
    founded_year = models.IntegerField(null=True, blank=True)
    
    is_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.company_name
    
    class Meta:
        db_table = 'recruiters'
        ordering = ['-created_at']
