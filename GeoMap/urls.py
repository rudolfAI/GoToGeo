from django.urls import path
from .views import GeoMapView, ProfileView

app_name = 'GeoMap'

urlpatterns = [
    path('', GeoMapView.as_view(), name='geo_view'),
]
