from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms


class BootstrapAuthenticationForm(AuthenticationForm):
    """Default form used by django to log in users.

    It has been extended to use bootstrap classes for styling.
    """
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'User name'}))
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder': 'Password'
        }))


class NewUserForm(UserCreationForm):
    """This form is used to capture all the user's personal information.

    It has to be used in conjunction with ProfileUpdateForm.
    """
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2"
        )

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
