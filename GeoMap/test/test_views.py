from django.test import RequestFactory
from django.http import Http404
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
        assert 'login' in resp.url, 'Should redirect since user is not logged in'

        req.user = mixer.blend('auth.User')
        resp = GeoMapView.as_view()(req)
        assert resp.status_code == 200, 'Should return status OK, since it is a valid request'

class TestProfileView:
    def test_get(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = ProfileView.as_view()(req)
        assert 'login' in resp.url, 'Should redirect since user is not logged in'
        
        req.user = mixer.blend('auth.User')   
        profile = mixer.blend('Profile.Profile')     
        resp = ProfileView.as_view()(req, id=profile.id)
        assert resp.status_code == 200, 'Should return status OK, since it is a valid request'
        
        with pytest.raises(Http404):
            resp = ProfileView.as_view()(req)