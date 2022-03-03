from django.urls import path
from .views import GeoMapView, ProfileView
from django.contrib.auth.decorators import login_required
app_name = 'GeoMap'

urlpatterns = [
    path('', login_required(GeoMapView.as_view()), name='geo_view'),
    path('profile/<int:id>/', login_required(ProfileView.as_view()), name='profile_view')
]
