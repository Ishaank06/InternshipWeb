from django.contrib import admin
from .models import SkillCategory, Skill, StudentSkill

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'description')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_trending', 'industry_demand_index')
    list_filter = ('category', 'is_trending')
    search_fields = ('name',)

@admin.register(StudentSkill)
class StudentSkillAdmin(admin.ModelAdmin):
    list_display = ('student', 'skill', 'proficiency', 'is_verified', 'last_updated')
    list_filter = ('proficiency', 'is_verified', 'skill__category')
    search_fields = ('student__user__username', 'skill__name')
