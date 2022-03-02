from django.urls import path
from .views import GeoMapView, ProfileView

app_name = 'GeoMap'

urlpatterns = [
    path('', GeoMapView.as_view(), name='geo_view'),
    path('profile/<int:id>/', ProfileView.as_view(), name='profile_view')
]
