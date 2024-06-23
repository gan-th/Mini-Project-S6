"""
URL configuration for gfg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views

urlpatterns = [
   #path('signin',views.signin,name="signin"),
   #path('signup',views.signup,name="signup"),
   #path('login/', include('login.urls')),
   path('signout',views.signout,name="signout"),
   path('log_m',views.log,name="log_m"),
   path('log_error',views.log,name="log_error"),
   path('sign_m',views.sign_m,name="sign_m"),
   path('dashboard',views.dashboard,name="dashboard"),
   path('about',views.about,name="about"),
   path('model',views.model,name="model"),
   path('search',views.search,name="search"),
   path('contact',views.contact,name="contact"),
   path('User_Profile',views.User_Profile,name="User_Profile"),
   path('', views.log,name="home"),
]
