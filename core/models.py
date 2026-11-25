from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('RECRUITER', 'Industry Recruiter / Partner'),
        ('FACULTY_TPO', 'Faculty / TPO Coordinator'),
        ('ADMIN', 'Institution Administrator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    avatar_url = models.CharField(max_length=500, blank=True, default='https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=256&q=80')

    # Student specific fields
    roll_number = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True, default='Computer Science & Engineering')
    graduation_year = models.IntegerField(default=2026, blank=True, null=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=8.5, blank=True, null=True)
    resume_link = models.URLField(blank=True)
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)

    # Industry / Recruiter specific fields
    company_name = models.CharField(max_length=150, blank=True)
    company_website = models.URLField(blank=True)
    company_sector = models.CharField(max_length=100, blank=True, default='Information Technology / Software')
    designation = models.CharField(max_length=100, blank=True)
    company_address = models.CharField(max_length=255, blank=True)
    company_logo = models.CharField(max_length=500, blank=True, default='https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=256&q=80')

    # Faculty / TPO specific fields
    employee_id = models.CharField(max_length=50, blank=True)
    faculty_department = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.role == 'RECRUITER' and self.company_name:
            return f"{self.user.get_full_name() or self.user.username} ({self.company_name})"
        elif self.role == 'STUDENT' and self.roll_number:
            return f"{self.user.get_full_name() or self.user.username} [{self.roll_number}]"
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    @property
    def is_student(self):
        return self.role == 'STUDENT'

    @property
    def is_recruiter(self):
        return self.role == 'RECRUITER'

    @property
    def is_faculty_tpo(self):
        return self.role == 'FACULTY_TPO' or self.user.is_superuser
