# import phonenumbers
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from phonenumber_field.formfields import PhoneNumberField
from .models import User_Profile
from phone_field import PhoneField


class UserProfile(forms.ModelForm):

    image = forms.FileField(required=True, widget=forms.FileInput(
        attrs={'class': 'form-control', 'multiple': True,  'accept': 'image/*'})),

    phone = PhoneField(blank=True, help_text='Contact phone number'),

    father_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Contact'})),

    mother_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Contact'})),

    g_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )

    gender = forms.ChoiceField(choices=g_choice, widget=forms.
                Select(attrs={'class': 'form-control'})),

    date_of_birth = forms.DateField(required=True),

    address = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Contact'})),

    city = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the City'})),

    state = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the State'})),

    pincode = forms.IntegerField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Pincode'})),

    class Meta:
        model = User_Profile
        fields = {'image', 'phone', 'father_name', 'mother_name', 'gender', 'date_of_birth',
                  'address', 'city', 'pincode', }




