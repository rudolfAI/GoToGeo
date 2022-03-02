from django.contrib import admin
from django.urls import path, include
from .views import HomeView
from .forms import BootstrapAuthenticationForm
from django.contrib.auth.views import LoginView
from datetime import datetime
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('profile/', include('Profile.urls'), name='Profile'),
    
    path('login/',
         LoginView.as_view
         (
             template_name='login.html',
             authentication_form=BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'date' : datetime.now(),
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
