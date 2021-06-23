from django.contrib import admin
from django import forms
from typing import Dict, Any
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from user.models import User as model_user

class LoginUser(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'id': "username",
                'placeholder': "Username",
                'data-error': "Please enter your name",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': "form-control",
                'id': "password",
                'placeholder': "Password",
                'data-error': "Please enter your password",
            }
        )
    )

def clean(self):
    user = authenticate(**dict(self.cleaned_data))
    if user is not None:
        user = self.cleaned_data["user"] 
        return self.cleaned_data
    else:
        self.add_error("username", "invalid username")
        self.add_error("password", "invalid password")
        raise forms.ValidationError("User not found!")

class UserForm(forms.ModelForm):
    password_repeat = forms.CharField(
        widget=forms.PasswordInput()
    )
    class Meta:
        model = model_user
        fields = [
            'username',
            'email',
            'password',
            'icon',
            ]
        widgets = {
            "password": forms.PasswordInput(),
            "icon" : forms.FileInput()
        }

    def clean(self):
        if self.cleaned_data["password"] != self.cleaned_data["password_repeat"]:
            raise forms.ValidationError("Пароли разные, переделай ~~")
        return super().clean()
    
    def save(self, commit:bool=False):
        user = super().save(commit=commit)
        user.set_password(user.password)
        user.save()
        return user

