# import phonenumbers
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User_Profile, Account_details, Transactions
from phone_field import PhoneField
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)

class UserProfileForm(forms.ModelForm):
    image = forms.FileField(required=False, widget=forms.FileInput(
        attrs={'class': 'form-control', 'accept': 'image/*'}))

    contact = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Contact'}))

    father_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Father\'s name' }))

    mother_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Mother\'s name'}))

    g_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    gender = forms.ChoiceField(choices=g_choice, widget=forms.
                Select(attrs={'class': 'form-control'}))

    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(
        attrs={'class':'form-control'}))

    address = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Contact'}))

    city = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the City'}))

    state = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the State'}))

    pincode = forms.IntegerField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Pincode'}))

    class Meta:
        model = User_Profile
        fields = {'image', 'contact', 'father_name', 'mother_name', 'gender', 'date_of_birth',
                  'address', 'city', 'pincode','state' }

class TransactionForm(forms.ModelForm):

    Recipient_Name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Recipient Name'}))

    IFSC = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the IFSC Code'}))

    account_no = forms.IntegerField(validators=[
            MinValueValidator(10000000),
            MaxValueValidator(99999999999999999)
        ], required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Account No.'}))

    tchoice = [
        ('Online', 'Online'),
        ('Credit-Card', 'Credit Card')
    ]

    transaction_type = forms.TypedChoiceField(required=True, choices=tchoice, widget=forms.Select(
        attrs={'class': 'form-control'}))

    # date = forms.DateField(required=True, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Date'}))

    amount = forms.IntegerField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Amount'}))

    class Meta:
        model = Transactions
        fields = {'Recipient_Name', 'IFSC', 'account_no', 'transaction_type', 'amount'}


