from django.contrib import admin
from .models import Opportunity, OpportunitySkillRequirement, Application

class OpportunitySkillRequirementInline(admin.TabularInline):
    model = OpportunitySkillRequirement
    extra = 2

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'opportunity_type', 'work_mode', 'stipend_salary', 'min_cgpa', 'deadline', 'status')
    list_filter = ('opportunity_type', 'work_mode', 'status')
    search_fields = ('title', 'company__company_name', 'description')
    inlines = [OpportunitySkillRequirementInline]

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'opportunity', 'match_score', 'status', 'applied_at')
    list_filter = ('status',)
    search_fields = ('student__user__username', 'opportunity__title')
