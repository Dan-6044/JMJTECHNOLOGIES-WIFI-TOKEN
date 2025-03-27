
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User  # Use the default User model
        fields = ['username', 'email', 'password']  # Fields for user Signup

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            EmailValidator()(email)
        except ValidationError:
            raise ValidationError("Please enter a valid email address.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 or not any(char.isdigit() for char in password) \
                or not any(char.isupper() for char in password) or not any(char in '!@#$%^&*()' for char in password):
            raise ValidationError("Password must be at least 8 characters long, contain an uppercase letter, a number, and a symbol.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")




class SigninForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

from django import forms
from .models import Station

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['station_id', 'station_name', 'location', 'station_type', 'status']
        widgets = {
            'station_id': forms.TextInput(attrs={'class': 'form-control'}),
            'station_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'station_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
