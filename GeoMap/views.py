from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.views import View
from Profile.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin


class GeoMapView(LoginRequiredMixin, View):
    """This view generates map with all registered coordinates

    displayed on the map.
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def __init__(self, *args, **kwargs):
        """Generates default context and template name
        """
        self.template_name = 'GeoMap/geomap.html'
        self.context = {
            'title': 'Geo Map',
            'date': datetime.now()
        }

    def get(self, request, *args, **kwargs):
        """Creates map with MapBox js library displaying the map

        and all registered user's gps coordinates.
        """
        users = Profile.objects.all()
        users = users.select_related()
        self.context['coordinates'] = users
        return render(request, self.template_name, self.context)


class ProfileView(LoginRequiredMixin, View):
    """Profile view accessible to everyone.

    This view has no editing options.
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def __init__(self, *args, **kwargs):
        """Generates default context and template name
        """
        self.template_name = 'GeoMap/profile.html'
        self.context = {
            'title': 'Geo Profile',
            'date': datetime.now()
        }

    def get(self, request, id=None, *args, **kwargs):
        """Registered users can view all other user's profiles.

        This view has no editing capabilities.
        """
        object = get_object_or_404(Profile, id=id)
        self.context['object'] = object
        return render(request, self.template_name, self.context)
