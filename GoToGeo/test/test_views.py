from django.test import RequestFactory
from django.http import Http404
from django.contrib.auth.models import AnonymousUser, User
import pytest
from mixer.backend.django import mixer
from django.test.testcases import TestCase
pytestmark = pytest.mark.django_db

from io import BytesIO
from PIL import Image

from GoToGeo.views import RegisterView, HomeView

class TestHomeView:
    def test_get(self):
        req = RequestFactory().get('/')
        resp = HomeView.as_view()(req)
        assert resp.status_code == 200, 'Should be able to view'

class TestRegisterView(TestCase):
    def create_test_image(self):
        file = BytesIO()
        image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file
    
    def test_get(self):
        req = RequestFactory().get('/')
        resp = RegisterView.as_view()(req)
        assert resp.status_code == 200, 'Should be able to view'
        
    def test_post(self):
        data = {
            'username' : 'email@email.com',
            'first_name' : 'name',
            'last_name' : 'surname',
            'email' : 'email@email.com',
            'password1' : 'Test1234!@#$',
            'password2' : 'Test1234!@#$',
            'picture' : self.create_test_image(),
            'phone_number_0' : '+27',
            'phone_number_1': '0788027374',
            'home_address' : 321,
            'geo_h' : 12,
            'geo_v' : 12,
        }
        response = self.client.post("/register", data)
        user = User.objects.get(email="email@email.com")
        self.assertEqual(user.username, "email@email.com")
        self.assertEqual(response.status_code, 302) #if it's successful it redirects.       
        
        data = {
            'username' : 'email@email.com',
            'first_name' : 'name',
            'last_name' : 'surname',
            'email' : 'email@email.com',
            'password1' : 'Test1234!@#$',
            'password2' : 'Test1234!@#$',
            'picture' : self.create_test_image(),
            'phone_number_0' : '+27',
            'phone_number_1': '0788027374123123123', #faulty data
            'home_address' : 321,
            'geo_h' : 12,
            'geo_v' : 12,
        }
        response = self.client.post("/register", data)
        self.assertEqual(response.status_code, 200) #if it's unsuccessful it re-renders. 