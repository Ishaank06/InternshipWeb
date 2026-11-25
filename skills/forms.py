from django import forms
from .models import StudentSkill, Skill

class AddStudentSkillForm(forms.ModelForm):
    class Meta:
        model = StudentSkill
        fields = ['skill', 'proficiency', 'certificate_name', 'certificate_url']
        widgets = {
            'skill': forms.Select(attrs={'class': 'form-select'}),
            'proficiency': forms.Select(attrs={'class': 'form-select'}),
            'certificate_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. AWS Solutions Architect or Coursera'}),
            'certificate_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }
