from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from io import BytesIO
from django.core.files import File
from PIL import Image

from django.urls import reverse

def content_image_name(instance, imagename):
    path = f"Profile/{instance.id}/{imagename}"
    return path

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=content_image_name)
    phone_number = PhoneNumberField()
    home_address = models.CharField(max_length=256)
    geo_h = models.FloatField()
    geo_v = models.FloatField()

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            name =  f"{self.user.first_name} {self.user.last_name}\n"
        else:
            name = f"{self.user}\n"
        name += f"N: {self.geo_h}\n"
        name += f"W: {self.geo_v}\n"
        return name

    def get_absolute_url(self):
        return reverse("profile", kwargs={"id": self.id})
    
    def save(self, *args, **kwargs):
        if not self.id:
            temp_picture = self.picture
            self.picture = None
            super().save(*args, **kwargs) # get id / preserve image save path
            self.picture = temp_picture

        if self.picture:
            self.picture = self.resize_image(self.picture, size=(480,270))

        super().save(*args, **kwargs)
        
    def resize_image(self, image, size=(900,600)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail