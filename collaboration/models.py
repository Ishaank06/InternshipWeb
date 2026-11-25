from django.db import models
from core.models import UserProfile

class CollaborationProject(models.Model):
    PROJECT_TYPES = (
        ('CAPSTONE', 'Joint Capstone / Final Year Project'),
        ('INDUSTRY_RND', 'Applied Industry R&D Challenge'),
        ('HACKATHON', 'Sponsored Hackathon / Ideathon'),
        ('CONSULTANCY', 'Faculty-Industry Tech Consultancy'),
    )

    STATUS_CHOICES = (
        ('PROPOSED', 'Proposed / Open for Faculty & Students'),
        ('IN_PROGRESS', 'Active Project Team Assembled'),
        ('COMPLETED', 'Successfully Completed & Delivered'),
    )

    title = models.CharField(max_length=200)
    industry_partner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='industry_projects')
    faculty_mentor = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='mentored_projects')
    project_type = models.CharField(max_length=30, choices=PROJECT_TYPES, default='CAPSTONE')
    description = models.TextField()
    expected_outcomes = models.TextField(blank=True)
    stipend_grant = models.CharField(max_length=100, blank=True, help_text="e.g. ₹50,000 project grant or Sponsored API keys")
    team_size_limit = models.IntegerField(default=4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PROPOSED')
    start_date = models.DateField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.get_project_type_display()})"


class CurriculumFeedback(models.Model):
    STATUS_CHOICES = (
        ('PENDING_REVIEW', 'Pending Board of Studies (BoS) Review'),
        ('ACCEPTED', 'Accepted & Added to Upcoming Syllabus'),
        ('UNDER_EVALUATION', 'Under Faculty Committee Evaluation'),
        ('DECLINED', 'Not Applicable at This Stage'),
    )

    industry_partner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='curriculum_feedbacks')
    course_name = models.CharField(max_length=150, help_text="e.g. CS402 - Distributed Cloud Systems")
    department = models.CharField(max_length=100, default='Computer Science & Engineering')
    observed_industry_gap = models.TextField(help_text="What skills fresh graduates currently lack in production")
    proposed_technologies = models.TextField(help_text="Recommended tools, libraries, or practical modules to include")
    academic_response = models.TextField(blank=True, help_text="Action notes by HOD / BoS members")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING_REVIEW')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback on {self.course_name} by {self.industry_partner.company_name or self.industry_partner.user.username}"


class IndustryMoU(models.Model):
    company_name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    signing_date = models.DateField()
    valid_upto = models.DateField()
    focus_areas = models.CharField(max_length=255, default='Student Internships, Faculty Up-skilling, Curriculum Co-design')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"MoU with {self.company_name} (Active: {self.is_active})"
