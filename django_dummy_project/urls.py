"""
URL configuration for django_dummy_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django_dummy_app.views import *     
from django.conf import settings        # App settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # Static files servings

urlpatterns = [
    #path('api/', include('django_dummy_app.urls')),
    #path('home/', home, name="recipes"),                # Home page
    #path("admin/", admin.site.urls),                    # Admin interface
    #path('', include('users.urls'))                    # Url patterns for users app, I'm not sure how to set this up yet
    
    # Unused url patterns
    # django_dummy_app views
    # path('admin/', admin.site.urls),
    # path('login/', login_page, name='login_page'),       # Login page
    # path('register/', register_page, name='register'),   # Registration page
    # path('', views.home, name='home'),
]