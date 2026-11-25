from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('skills/', include('skills.urls')),
    path('internships/', include('internships.urls')),
    path('collaboration/', include('collaboration.urls')),
]
