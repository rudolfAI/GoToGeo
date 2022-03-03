from django.test import RequestFactory
from django.http import Http404
import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

from Profile.models import Profile, Audit

class TestProfile:
    def test_model(self):
        obj = mixer.blend('Profile.Profile')
        assert obj.id == 1, 'Test create object'  
        
    def test___str__(self):
        obj = mixer.blend('Profile.Profile')
        assert f"{obj}" == f"{obj.user.first_name} {obj.user.last_name}", 'Test object output string'
        
    def test_get_absolute_url(self):
        obj = mixer.blend('Profile.Profile')
        assert obj.get_absolute_url() == "/profile/", "Should provide profile url"
        
    def test_get_geo_profile_url(self):
        obj = mixer.blend('Profile.Profile')
        assert obj.get_geo_profile_url() == f"/geo_map/profile/{obj.id}/", "Should provide profile url"
        
    def test_save(self):
        obj = mixer.blend('Profile.Profile')
        result = obj.picture.url
        expect = f'/media/{obj.picture.name}'
        obj.delete()
        assert result == expect, \
            'Upon save, profile image should be moved to correct folder'
            
    def test_resize_image(self):
        """3rd party lib, skip testing
        """
        pass
    
class TestAudit:
    def test_model(self):
        obj = mixer.blend('Profile.Audit')
        assert obj.id == 1, 'Test create object'  
    def test___str__(self):
        obj = mixer.blend('Profile.Audit', login=True)
        assert f"{obj}" == f"User: {obj.user}; Date & Time: {obj.time}; Status: Logged in", \
            "Output string needs to be formatted correctly"
        