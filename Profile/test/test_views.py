from io import BytesIO
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
from PIL import Image

from Profile.views import ProfileView
from Profile.models import Profile

class TestProfileView:
    def create_test_image(self):
        file = BytesIO()
        image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file
    
    def test_get(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        resp = ProfileView.as_view()(req)
        assert 'login' in resp.url, 'Should redirect since user is not logged in'
        
        req = RequestFactory().get('/')
        req.user = mixer.blend('auth.User')
        resp = ProfileView.as_view()(req)
        assert 'login' in resp.url, 'Should redirect since user has no profile'
        
        req = RequestFactory().get('/')
        profile = mixer.blend('Profile.Profile')        
        req.user = profile.user        
        resp = ProfileView.as_view()(req)
        assert resp.status_code == 200, 'Should return 200 ok, since user has a profile'
        
    def test_post(self):
        profile = mixer.blend('Profile.Profile')
        
        data = {
            'first_name' : 'name',
            'last_name' : 'surname',
            'email' : 'test@test.com',
            'picture' : self.create_test_image().read(),
            'phone_number_0' : '+27',
            'phone_number_1': 788027374,
            'home_address' : 321,
            'geo_h' : 12,
            'geo_v' : 12,
        }
        req = RequestFactory().post('/', data=data)
        req.user = AnonymousUser()
        resp = ProfileView.as_view()(req)
        assert 'login' in resp.url, 'Should redirect since user is not logged in'
        
        req.user = mixer.blend('auth.User')
        resp = ProfileView.as_view()(req)
        assert 'login' in resp.url, 'Should redirect since user has no profile'

        profile.refresh_from_db()
        assert profile.phone_number != 788027374, \
            'Object should not be updated, since phone number format is incorrect'
            
        req = RequestFactory().post('/', data=data)
        req.user = profile.user
        resp = ProfileView.as_view()(req)
        profile = Profile.objects.get(id=1)
        assert profile.phone_number.national_number == 788027374, \
            'Object should be updated to new value'
            
            
        data = {
            'first_name' : 'name',
            'last_name' : 'surname',
            'email' : 'test@test.com',
            'picture' : self.create_test_image().read(),
            'phone_number_0' : '+27',
            'phone_number_1': 788027374321123213, #faulty data
            'home_address' : 321,
            'geo_h' : 12,
            'geo_v' : 12,
        }
        req = RequestFactory().post('/', data=data)
        req.user = profile.user
        resp = ProfileView.as_view()(req)
        profile = Profile.objects.get(id=1)
        assert profile.phone_number.national_number == 788027374, \
            'Object should be updated to new value'