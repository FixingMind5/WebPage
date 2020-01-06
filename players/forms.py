"""Forms for sign up"""

# Django utilities
from django import forms

# Django models
from django.contrib.auth.models import User

# My models
from players.models import Player

# Utilities
from datetime import datetime


class PlayerForm(forms.Form):
    first_name = forms.CharField(min_length=2, max_length=30, required=True)
    last_name = forms.CharField(min_length=2, max_length=50, required=True)
    username = forms.CharField(min_length=3, max_length=30, required=True)
    email = forms.CharField(min_length=4, max_length=70, widget=forms.EmailInput(), required=True)
    password = forms.CharField(min_length=2, max_length=30, widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(min_length=2, max_length=30, widget=forms.PasswordInput(), required=True)
    day = forms.IntegerField(required=True)
    month = forms.IntegerField(required=True)
    year = forms.IntegerField(required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        is_username_taken = User.objects.filter(username=username).exists()
        if is_username_taken:
            raise forms.ValidationError("El nombre de usuario ya está en uso 😮")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        is_email_taken = User.objects.filter(email=email).exists()
        if is_email_taken:
            raise forms.ValidationError(f"El email {email} ya está registrado en nuestra base de datos 😮")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden 😞")

        return cleaned_data
    
    def save(self):
        cleaned_data = self.cleaned_data
        cleaned_data.pop('confirm_password')

        day = cleaned_data.get('day')
        month = cleaned_data.get('month')
        year = cleaned_data.get('year')

        birth_date_string = str(day) + "/" + str(month) + "/" + str(year)
        birth_date = datetime.strptime(birth_date_string, "%d/%m/%Y")

        cleaned_data.pop('day')
        cleaned_data.pop('month')
        cleaned_data.pop('year')

        user = User.objects.create_user(**cleaned_data)
        player = Player(user=user, birth_date=birth_date)
        player.save()