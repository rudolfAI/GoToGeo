from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from Profile.models import Profile
from django.contrib.auth.models import User


class CustomPhoneNumberPrefixWidget(PhoneNumberPrefixWidget):
    """This form is used to create a country selector widget 
    
    to be displayed with the phone number field.

    Example: You can choose South Africa, and type in 
    
    078 123 1234 and it will update it to +27 78 123 1234
    """
    def subwidgets(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        return context['widget']['subwidgets']


class UserUpdateForm(forms.ModelForm):
    """This form is used to update user personal information,
    
    excluding passwords. TODO: add password change/reset.

    It has to be used in conjunction with ProfileUpdateForm.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class ProfileUpdateForm(forms.ModelForm):
    """This form is used to create or update user profile data.

    It has to be used in conjunction with UserUpdateForm or NewUserForm.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['picture'].widget.attrs['class'] = 'form-control'

        contact_widgets = self.fields['phone_number'].widget.widgets
        contact_widgets[0].attrs.update({'class': 'form-select'})
        contact_widgets[1].attrs.update({
            'class': 'form-control',
            'placeholder': 'Phone Number'
        })

        self.fields['home_address'].widget.attrs['class'] = 'form-control'
        self.fields['geo_h'].widget.attrs['class'] = 'form-control'
        self.fields['geo_v'].widget.attrs['class'] = 'form-control'

        self.fields['home_address'].widget.attrs['placeholder'] = self.fields['home_address'].label
        self.fields['geo_h'].widget.attrs['placeholder'] = 'NS coordinate'
        self.fields['geo_v'].widget.attrs['placeholder'] = 'WE coordinates'

    class Meta:
        model = Profile
        exclude = (
            'user',
        )
        widgets = {
            "phone_number": CustomPhoneNumberPrefixWidget(),
        }
