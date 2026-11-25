from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import UserProfile
from skills.models import Skill, StudentSkill

class Opportunity(models.Model):
    TYPE_CHOICES = (
        ('INTERNSHIP', 'Summer / Semester Internship'),
        ('PLACEMENT', 'Full-Time Campus Placement'),
        ('RESEARCH_INTERN', 'Research & R&D Internship'),
    )

    WORK_MODE_CHOICES = (
        ('HYBRID', 'Hybrid (In-Office + Remote)'),
        ('REMOTE', '100% Remote / Work from Home'),
        ('ON_SITE', 'On-Site (At Company Office)'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'Pending TPO Approval'),
        ('APPROVED', 'Approved & Open for Applications'),
        ('CLOSED', 'Applications Closed'),
    )

    company = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='opportunities')
    title = models.CharField(max_length=200)
    opportunity_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='INTERNSHIP')
    work_mode = models.CharField(max_length=20, choices=WORK_MODE_CHOICES, default='HYBRID')
    location = models.CharField(max_length=150, default='Bengaluru / Gurgaon')
    stipend_salary = models.CharField(max_length=100, help_text="e.g. ₹35,000 / month or ₹12 - 16 LPA")
    duration = models.CharField(max_length=100, default='6 Months')
    openings = models.IntegerField(default=5)
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=7.0)
    department_eligibility = models.CharField(max_length=255, default='B.Tech / M.Tech / MCA (CSE, IT, ECE)')
    
    description = models.TextField()
    responsibilities = models.TextField(blank=True)
    perks = models.TextField(blank=True, default='PPO Opportunity, Mentorship by Senior Architects, Certification')
    
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPROVED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} @ {self.company.company_name or self.company.user.username}"

    def calculate_student_match(self, student_profile):
        """
        Calculates skill match percentage and gap analysis for a given student.
        """
        reqs = self.skill_requirements.all()
        if not reqs.exists():
            return 100, [], []

        total_req_points = sum(r.min_proficiency for r in reqs)
        student_points = 0
        matching_skills = []
        missing_skills = []

        # Fetch student's skills as a dictionary
        student_skills_dict = {
            ss.skill_id: ss.proficiency 
            for ss in StudentSkill.objects.filter(student=student_profile)
        }

        for req in reqs:
            student_prof = student_skills_dict.get(req.skill_id, 0)
            capped_prof = min(student_prof, req.min_proficiency)
            student_points += capped_prof

            diff = student_prof - req.min_proficiency
            skill_info = {
                'skill_name': req.skill.name,
                'required': req.min_proficiency,
                'student_level': student_prof,
                'is_mandatory': req.is_mandatory,
                'diff': diff
            }
            if student_prof >= req.min_proficiency:
                matching_skills.append(skill_info)
            else:
                missing_skills.append(skill_info)

        match_percent = int((student_points / total_req_points) * 100) if total_req_points > 0 else 0
        return min(match_percent, 100), matching_skills, missing_skills


class OpportunitySkillRequirement(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='skill_requirements')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    min_proficiency = models.IntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_mandatory = models.BooleanField(default=True)

    class Meta:
        unique_together = ('opportunity', 'skill')

    def __str__(self):
        return f"{self.skill.name} (>= {self.min_proficiency}/5) for {self.opportunity.title}"


class Application(models.Model):
    STATUS_CHOICES = (
        ('APPLIED', 'Application Submitted'),
        ('UNDER_REVIEW', 'Under Technical Review'),
        ('SHORTLISTED', 'Shortlisted for Assessment'),
        ('INTERVIEW_SCHEDULED', 'Interview Scheduled'),
        ('OFFERED', 'Offer Extended / Selected'),
        ('REJECTED', 'Not Selected'),
    )

    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    match_score = models.IntegerField(default=0)
    cover_letter = models.TextField(blank=True)
    portfolio_url = models.URLField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='APPLIED')
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_link = models.URLField(blank=True)
    recruiter_notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('opportunity', 'student')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.student.user.username} -> {self.opportunity.title} [{self.status}]"
