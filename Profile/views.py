from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime
from Profile.forms import ProfileUpdateForm, UserForm

class ProfileView(View):
    def __init__(self, *args, **kwargs):
        self.template_name = 'Profile/profile.html'
        self.context = {
            'title' : 'User Profile',
            'date' : datetime.now()
        }
    
    def get(self, request, *args, **kwargs):
        try:
            object = request.user.profile
        except: 
            return redirect('login')
        form_user = UserForm(instance=object.user)
        form_profile = ProfileUpdateForm(instance=object)
        
        self.context['object'] = object
        self.context['form_user'] = form_user
        self.context['form_profile'] = form_profile
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        try:
            object = request.user.profile
        except: 
            return redirect('login')
        object = request.user.profile
        form_user = UserForm(request.POST, instance=object.user)
        form_profile = ProfileUpdateForm(request.POST, request.FILES, instance=object)
        
        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            form_profile.save()
            return redirect('Profile:profile_view')
        
        self.context['object'] = object
        self.context['form_user'] = form_user
        self.context['form_profile'] = form_profile
        return render(request, self.template_name, self.context)