from django.urls import path
from .views import ProfileView
from django.contrib.auth.decorators import login_required

app_name = 'Profile'

urlpatterns = [
    path('', login_required(ProfileView.as_view()), name='profile_view')
]
