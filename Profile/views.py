from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from datetime import datetime
from Profile.forms import ProfileUpdateForm, UserForm

from Profile.models import Profile

class ProfileView(View):
    def __init__(self, *args, **kwargs):
        self.template_name = 'Profile/profile.html'
        self.context = {
            'Title' : 'User Profile',
            'date' : datetime.now()
        }
    
    def get(self, request, *args, **kwargs):
        object = request.user.profile
        form_user = UserForm(instance=object.user)
        form_profile = ProfileUpdateForm(instance=object)
        
        self.context['object'] = object
        self.context['form_user'] = form_user
        self.context['form_profile'] = form_profile
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        object = request.user.profile
        form_user = UserForm(request.POST, instance=object.user)
        form_profile = ProfileUpdateForm(request.POST, instance=object)
        
        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            form_profile.save()
            return redirect('Profile:profile_view')
        
        self.context['object'] = object
        self.context['form_user'] = form_user
        self.context['form_profile'] = form_profile
        return render(request, self.template_name, self.context)