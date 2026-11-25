from django.urls import path
from . import views

urlpatterns = [
    path('', views.collaboration_hub, name='collaboration_hub'),
    path('propose-project/', views.propose_project, name='propose_project'),
    path('curriculum-feedback/', views.submit_curriculum_feedback, name='submit_curriculum_feedback'),
    path('curriculum-feedback/<int:pk>/update/', views.update_feedback_status, name='update_feedback_status'),
]
