from django import forms
from .models import User_Profile, Account_details, Transactions
from phone_field import PhoneField


class UserProfileForm(forms.ModelForm):

    image = forms.FileField(required=True, widget=forms.FileInput(
        attrs={'class': 'form-control', 'multiple': True,  'accept': 'image/*'}))

    phone = forms.CharField(required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    father_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Contact'}))

    mother_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Contact'}))

    choices = [
        ("Male", "Male"),
        ('Female', 'Female')

      ]
    gender = forms.TypedChoiceField(required=True, choices=choices, widget=forms.
                             Select(attrs={'class': 'form-control'}))

    date_of_birth = forms.DateField(required=True, widget=forms.
                             Select(attrs={'class': 'form-control'}))

    address = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Address'}))

    city = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the City'}))

    state = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the State'}))

    pincode = forms.IntegerField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Pincode'}))

    class Meta:
        model = User_Profile
        fields = {'image', 'father_name', 'mother_name', 'phone', 'gender', 'date_of_birth',
                  'address', 'city', 'pincode', }


class TransactionForm(forms.ModelForm):

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
        fields = {'transaction_type', 'amount'}


