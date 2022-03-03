from django.test import RequestFactory
from django.http import Http404
from django.contrib.auth.models import AnonymousUser, User
import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

from Profile.views import ProfileView

class TestProfileView:
    def test_get(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = ProfileView.as_view()(req)
        assert resp.status_code == 302, 'Should redirect since user is not logged in'
        
        req.user = mixer.blend('auth.User')        
        resp = ProfileView.as_view()(req)
        assert resp.status_code == 302, 'Should redirect since user is not logged in'
        
    def test_post(self):
        profile = mixer.blend('Profile.Profile')
        data = {
            'phone_number' : 123,
            'home_address' : 321,
            'geo_h' : 12,
            'geo_v' : 12,
        }
        req = RequestFactory().post('/', data=data)
        req.user = AnonymousUser()
        resp = ProfileView.as_view()(req)
        assert resp.status_code == 302, 'Should redirect since user is not logged in'
        
        req.user = mixer.blend('auth.User')        
        resp = ProfileView.as_view()(req)
        assert resp.status_code == 302, 'Should redirect since user is not logged in'

        profile.refresh_from_db()
        
        assert profile.phone_number != 123, \
            'Object should not be updated, since phone number format is incorrect'
            
        data = {
            'phone_number' : +27788027374,
            'home_address' : 321,
            'geo_h' : 12,
            'geo_v' : 12,
        }
        resp = ProfileView.as_view()(req)
        profile.refresh_from_db()
        assert profile.phone_number != +27788027374, \
            'Object should not be updated, since phone number format is incorrect'