from datetime import datetime
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from Profile.models import Profile, Audit
 
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    audit = Audit(
        user = request.user,
        time = datetime.now(),
        login = True,
    )
    audit.save()
 
@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    audit = Audit(
        user = request.user,
        time = datetime.now(),
        login = False,
    )
    audit.save()
    
