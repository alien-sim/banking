from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User_Profile
from phone_field import PhoneField



class User_Profile(forms.ModelForm):

    image = forms.FileField(required=True, widget=forms.FileInput(
        attrs={'class': 'form-control', 'multiple': True,  'accept': 'image/*'})),

    phone = PhoneField(required=True, blank=True, help_text='Contact phone number'),

    father_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Contact'})),

    mother_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Contact'})),

    gchoice = [
        ("Male", "Male"),
        ('Female', 'Female')

    ]
    gender = forms.CharField(required=True, choices=gchoice, widget=forms.
                             Select(attrs={'class': 'form-control'})),

    date_of_birth = forms.DateField(required=True),

    address = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Address'})),

    city = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the City'})),

    state = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the State'})),

    pincode = forms.IntegerField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Pincode'})),

    class Meta:
        model = User_Profile
        fields = {'image', 'phone_number', 'father_name', 'mother_name', 'phone', 'gender', 'date_of_birth',
                  'address', 'city', 'pincode', }






