"""
URL configuration for jobtracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from jobs import views as job_view
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('jobs.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', job_view.register, name='register'),
    path('dashboard/', job_view.dashboard, name='dashboard'),
    path('jobs/create/', job_view.job_create, name='job-create'),
    path('jobs/<int:pk>/edit/', job_view.job_edit, name='job-edit'),
    path('jobs/<int:pk>/delete/', job_view.job_delete, name='job-delete'),
    path('api/', include('jobs.urls')),
    path('', job_view.dashboard, name='home'),  # Root URL
    
    
    #JWTokens Authentication
    path('api/tokens/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/tokens/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
