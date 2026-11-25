from django.contrib import admin
from .models import CollaborationProject, CurriculumFeedback, IndustryMoU

@admin.register(CollaborationProject)
class CollaborationProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'industry_partner', 'faculty_mentor', 'project_type', 'status', 'start_date')
    list_filter = ('project_type', 'status')
    search_fields = ('title', 'industry_partner__company_name')

@admin.register(CurriculumFeedback)
class CurriculumFeedbackAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'industry_partner', 'department', 'status', 'created_at')
    list_filter = ('status', 'department')
    search_fields = ('course_name', 'proposed_technologies')

@admin.register(IndustryMoU)
class IndustryMoUAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'signing_date', 'valid_upto', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('company_name',)
