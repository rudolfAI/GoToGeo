from django.contrib import admin
from django.urls import path
from .views import ProfileView

app_name = 'Profile'

urlpatterns = [
    path('', ProfileView.as_view(), name='profile_view')
]
