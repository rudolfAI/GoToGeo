from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime
from Profile.forms import ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(LoginRequiredMixin, View):
    """User's default profile view, protected from other users.
    
    Only the owner of a profile, can edit their profile.
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    
    def __init__(self, *args, **kwargs):
        """Generates default context and template name
        """
        
        self.template_name = 'Profile/profile.html'
        self.context = {
            'title' : 'User Profile',
            'date' : datetime.now()
        }
    
    def get(self, request, *args, **kwargs):
        """Get request returns user object and user update forms.
        """
        try:
            object = request.user.profile
        except: 
            return redirect('login')
        form_user = UserUpdateForm(instance=object.user)
        form_profile = ProfileUpdateForm(instance=object)
        
        self.context['object'] = object
        self.context['form_user'] = form_user
        self.context['form_profile'] = form_profile
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        """POST request validates forms and updates user data
        
        as per user's input.
        """
        try:
            object = request.user.profile
        except: 
            return redirect('login')
        form_user = UserUpdateForm(request.POST, instance=object.user)
        form_profile = ProfileUpdateForm(request.POST, request.FILES, instance=object)
        
        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            form_profile.save()
            return redirect('Profile:profile_view')
        
        self.context['object'] = object
        self.context['form_user'] = form_user
        self.context['form_profile'] = form_profile
        return render(request, self.template_name, self.context)