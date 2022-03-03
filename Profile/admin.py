from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin


@admin.register(Profile)
class CustomProfile(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if request.user.is_superuser:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(id=request.user.profile.id)
