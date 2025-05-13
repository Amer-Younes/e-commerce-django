from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User , Profile
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))

    class Meta:
        model = User
        fields = ['username' , 'email']



class ProfileUpdateForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Full Name"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Phone"}))
    bio = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Bio"}))
    image= forms.ImageField(widget=forms.ClearableFileInput(attrs={"placeholder":"Image"}))
    class Meta:
        model = Profile
        fields = ["image", "full_name", "phone", "bio"]

        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control mt-2", "id": "id_image"}),
            "full_name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
