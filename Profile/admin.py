from django.contrib import admin
from Profile.models import Audit, Profile

@admin.register(Profile)
class CustomProfile(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if request.user.is_superuser:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(id=request.user.profile.id)


admin.site.register(Audit)