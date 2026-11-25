from django import forms
from .models import Opportunity, Application

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = [
            'title', 'opportunity_type', 'work_mode', 'location', 
            'stipend_salary', 'duration', 'openings', 'min_cgpa', 
            'department_eligibility', 'description', 'responsibilities', 
            'perks', 'deadline'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Backend Engineering Intern'}),
            'opportunity_type': forms.Select(attrs={'class': 'form-select'}),
            'work_mode': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bangalore / Remote'}),
            'stipend_salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. ₹40,000 / month or ₹12 LPA'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 6 Months'}),
            'openings': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'department_eligibility': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CSE, IT, ECE'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'responsibilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'perks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'portfolio_url']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Explain why you are the best fit for this role and mention your relevant project experience...'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/your-username or portfolio'}),
        }


class ApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'interview_date', 'interview_link', 'recruiter_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'interview_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'interview_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://meet.google.com/...'}),
            'recruiter_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
