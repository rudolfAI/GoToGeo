from datetime import datetime
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

from GoToGeo.forms import NewUserForm
from Profile.forms import ProfileUpdateForm


class HomeView(View):
    def __init__(self, *args, **kwargs):
        """Generates default context and template name.
        
        """
        self.template_name = "home_view/home.html"
        self.context = {
            'title': 'Home',
            'date': datetime.now()
        }

    def get(self, request, *args, **kwargs):
        """Create default home page for unauthenticated users.
        
        """
        return render(request, self.template_name, self.context)


class RegisterView(View):
    def __init__(self, *args, **kwargs):
        """Generates default context and template name.
        
        """
        self.template_name = "register.html"
        self.context = {
            'title': "Register",
            'date': datetime.now()
        }

    def get(self, request, *args, **kwargs):
        """Creates user and profile forms. Both need to be filled
        
        in by the user to be valid.
        """
        form_user = NewUserForm()
        form_profile = ProfileUpdateForm()
        self.context['form_user'] = form_user
        self.context['form_profile'] = form_profile
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        """Validates form data and creates a new user and related profile.

        If forms aren't valid, will re-render the page with errors.

        If forms are valid, server will redirect user to their new profile.
        """
        form_user = NewUserForm(request.POST)
        form_profile = ProfileUpdateForm(request.POST, request.FILES)

        if form_user.is_valid() and form_profile.is_valid():
            Form_user = form_user.save(commit=False)
            Form_user.save()

            Form_profile = form_profile.save(commit=False)
            Form_profile.user = Form_user
            Form_profile.save()
            login(request, Form_user)
            return redirect('Profile:profile_view')

        self.context['form_user'] = form_user
        self.context['form_profile'] = form_profile
        return render(request, self.template_name, self.context)
