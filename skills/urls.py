from django.urls import path
from . import views

urlpatterns = [
    path('', views.skills_catalog, name='skills_catalog'),
    path('my-skills/', views.my_skills, name='my_skills'),
    path('add-skill/', views.add_student_skill, name='add_student_skill'),
    path('delete-skill/<int:pk>/', views.delete_student_skill, name='delete_student_skill'),
    path('gap-analysis/', views.skill_gap_analysis, name='skill_gap_analysis'),
    path('gap-analysis/<int:opportunity_id>/', views.skill_gap_analysis, name='skill_gap_analysis_opp'),
    path('resume-extractor/', views.extract_skills_from_resume, name='resume_extractor'),
    path('verify-skill/<int:pk>/', views.verify_student_skill, name='verify_student_skill'),
]
