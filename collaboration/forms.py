from django import forms
from .models import CollaborationProject, CurriculumFeedback

class CollaborationProjectForm(forms.ModelForm):
    class Meta:
        model = CollaborationProject
        fields = ['title', 'project_type', 'description', 'expected_outcomes', 'stipend_grant', 'team_size_limit', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. AI-Powered Smart Campus Traffic Optimization'}),
            'project_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'expected_outcomes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'stipend_grant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. ₹50,000 project grant'}),
            'team_size_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class CurriculumFeedbackForm(forms.ModelForm):
    class Meta:
        model = CurriculumFeedback
        fields = ['course_name', 'department', 'observed_industry_gap', 'proposed_technologies']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CS302 - Web Architectures'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Computer Science & Engineering'}),
            'observed_industry_gap': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'What skills or tools are graduates lacking when joining company projects?'}),
            'proposed_technologies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Specify concrete libraries, frameworks, or modern software practices to introduce'}),
        }
