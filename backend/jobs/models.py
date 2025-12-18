from django.db import models
from recruiters.models import Recruiter
from students.models import Student


class Job(models.Model):
    """Job posting model"""
    
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    JOB_TYPE_CHOICES = (
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('INTERNSHIP', 'Internship'),
        ('CONTRACT', 'Contract'),
    )
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='FULL_TIME')
    
    skills_required = models.JSONField(default=list)
    
    experience_required = models.CharField(max_length=50, blank=True, null=True)
    education_required = models.CharField(max_length=100, blank=True, null=True)
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    ctc = models.CharField(max_length=50, blank=True, null=True)
    stipend = models.CharField(max_length=50, blank=True, null=True)
    
    location = models.CharField(max_length=255)
    is_remote = models.BooleanField(default=False)
    
    posted_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    openings = models.IntegerField(default=1)
    responsibilities = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)
    
    views_count = models.IntegerField(default=0)
    applications_count = models.IntegerField(default=0)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} at {self.recruiter.company_name}"
    
    class Meta:
        db_table = 'jobs'
        ordering = ['-posted_at']


class Application(models.Model):
    """Job application model"""
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    
    STATUS_CHOICES = (
        ('APPLIED', 'Applied'),
        ('UNDER_REVIEW', 'Under Review'),
        ('SHORTLISTED', 'Shortlisted'),
        ('INTERVIEW_SCHEDULED', 'Interview Scheduled'),
        ('SELECTED', 'Selected'),
        ('REJECTED', 'Rejected'),
        ('WITHDRAWN', 'Withdrawn'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
    
    match_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    matched_skills = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    
    cover_letter = models.TextField(blank=True, null=True)
    
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    recruiter_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.job.title}"
    
    class Meta:
        db_table = 'applications'
        ordering = ['-applied_at']
        unique_together = ['student', 'job']


class Interview(models.Model):
    """Interview scheduling model"""
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    
    MODE_CHOICES = (
        ('ONLINE', 'Online'),
        ('OFFLINE', 'Offline'),
        ('PHONE', 'Phone'),
    )
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='ONLINE')
    
    location = models.TextField(blank=True, null=True)
    
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('RESCHEDULED', 'Rescheduled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    
    interviewer_name = models.CharField(max_length=255, blank=True, null=True)
    interviewer_email = models.EmailField(blank=True, null=True)
    
    feedback = models.TextField(blank=True, null=True)
    rating = models.IntegerField(null=True, blank=True)
    
    reminder_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Interview for {self.application.student.name} - {self.scheduled_date}"
    
    class Meta:
        db_table = 'interviews'
        ordering = ['scheduled_date', 'scheduled_time']
