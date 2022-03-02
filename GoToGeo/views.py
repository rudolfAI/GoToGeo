from django.views import View
from django.shortcuts import render

class HomeView(View):
    def __init__(self, *args, **kwargs):
        self.template_name = "home/home.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'hello':'world'})
    