# import phonenumbers
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from phonenumber_field.formfields import PhoneNumberField
from .models import User_Profile


class UserProfile(forms.ModelForm):

    image = forms.FileField(required=True, widget=forms.FileInput(
        attrs={'class': 'form-control', 'multiple': True,  'accept': 'image/*'})),

    contact = forms.IntegerField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Contact'})),

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
        attrs={'class': 'form-control', 'placeholder': 'Enter the Contact'})),

    state = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Contact'})),

    pincode = forms.IntegerField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Contact'})),

    class Meta:
        model = User_Profile
        fields = {'image', 'father_name', 'mother_name', 'contact', 'gender', 'date_of_birth',
                  'address', 'city', 'pincode', }

    # def clean_phone_number(self):
    #     phone_number = self.cleaned_data.get("phone_number")
    #     z = phonenumbers.parse(phone_number, "SG")
    #     if not phonenumbers.is_valid_number(z):
    #         raise forms.ValidationError("Number not in SG format")
    #     return z.national_number



