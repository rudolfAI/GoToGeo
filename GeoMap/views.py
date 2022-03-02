from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.views import View
from Profile.models import Profile

class GeoMapView(View):
    def __init__(self, *args, **kwargs):
        self.template_name = 'GeoMap/geomap.html'
        self.context = {
            'title' : 'Goto Geo Map',
            'date' : datetime.now()
        }
        
    def get(self, request, *args, **kwargs):
        users = Profile.objects.all()
        users = users.select_related()
        self.context['coordinates'] = users
        return render(request, self.template_name, self.context)