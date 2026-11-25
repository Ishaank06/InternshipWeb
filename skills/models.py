from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import UserProfile

class SkillCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, default='bi-code-slash')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Skill Categories"

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    description = models.TextField(blank=True)
    is_trending = models.BooleanField(default=False)
    industry_demand_index = models.IntegerField(default=85, help_text="Market demand index 1-100")

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class StudentSkill(models.Model):
    PROFICIENCY_CHOICES = (
        (1, '1 - Beginner (Concept only)'),
        (2, '2 - Elementary (Basic project)'),
        (3, '3 - Intermediate (Hands-on practical)'),
        (4, '4 - Advanced (Production ready)'),
        (5, '5 - Expert (Architecture & Mastery)'),
    )

    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='student_skills')
    proficiency = models.IntegerField(choices=PROFICIENCY_CHOICES, default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    certificate_name = models.CharField(max_length=200, blank=True)
    certificate_url = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_skills')
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'skill')

    def __str__(self):
        return f"{self.student.user.username} - {self.skill.name} ({self.proficiency}/5)"
