from django.urls import path
from . import views

urlpatterns = [
    path('', views.opportunity_list, name='opportunity_list'),
    path('<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('post/', views.post_opportunity, name='post_opportunity'),
    path('<int:pk>/apply/', views.apply_opportunity, name='apply_opportunity'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('manage-applications/', views.manage_applications, name='manage_applications'),
    path('manage-applications/<int:opportunity_id>/', views.manage_applications, name='manage_applications_opp'),
    path('application/<int:pk>/update/', views.update_application_status, name='update_application_status'),
    path('<int:pk>/tpo-action/', views.tpo_approve_opportunity, name='tpo_approve_opportunity'),
]
