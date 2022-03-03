from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from io import BytesIO
from django.core.files import File
from PIL import Image

from django.urls import reverse

def content_image_name(instance, imagename):
    """Images uploaded to the server default saving location
    needs to be updated to be more organized and accessible.
    """
    file_type = imagename.split(".")
    path = f"Profile/{instance.id}/profile_image.{file_type[-1]}"
    return path

class Profile(models.Model):
    """Creates a single Profile entry extending the :model:`auth.user` model
    in a one to one fashion.


    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=content_image_name)
    phone_number = PhoneNumberField()
    home_address = models.CharField(max_length=256)
    geo_h = models.FloatField()
    geo_v = models.FloatField()

    def __str__(self):
        """Makes output strings more readable when called.
        """
        if self.user.first_name and self.user.last_name:
            name =  f"{self.user.first_name} {self.user.last_name}"
        else:
            name = f"{self.user}"
        return name

    def get_absolute_url(self):
        """Returns url to the user's profile page
        """
        return reverse("Profile:profile_view")
    
    def get_geo_profile_url(self):
        """Returns url to geo profile on display.
        """
        return reverse("GeoMap:profile_view", kwargs={"id": self.id})
    
    def save(self, *args, **kwargs):
        """Overrides default save method to appropriately handle
        saving profile pictures as well as resizing them smaller.
        """
        if not self.id:
            temp_picture = self.picture
            self.picture = None
            super().save(*args, **kwargs) # get id / preserve image save path
            self.picture = temp_picture

        if self.picture:
            self.picture = self.resize_image(self.picture, size=(480,270))

        super().save(*args, **kwargs)
        
    def resize_image(self, image, size=(900,600)):
        """Resizes image to default 900x600.
        Can be overridden as required.
        """
        img = Image.open(image)
        
        if img.mode in ("RGBA", "P"):
            img = img.convert('RGB')
        
        elif img.mode in ("JPEG"):
            pass
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail
    
class Audit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    login = models.BooleanField()

    def __str__(self):
        if self.login:
            msg = "Logged in"
        else:
            msg = "Logged out"
        return f"User: {self.user}: Date & Time: {self.time}: Status: {msg}"