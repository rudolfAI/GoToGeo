from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

from GeoMap.views import GeoMapView, ProfileView

class TestGeoMapView:
    def test_get(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = GeoMapView.as_view()(req)
        assert resp.status_code == 302, 'Should redirect since user is not logged in'
        
        # req.user = mixer.blend('auth.User')        
        # resp = ProfileView.as_view()(req)
        # assert resp.status_code == 302, 'Should redirect since user is not logged in'