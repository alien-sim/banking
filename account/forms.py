from .models import UserProfile, Account_details, Transactions
from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MoneyTransfer, Withdrawal
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = {'username', 'password1', 'password2'}


class ProfileForm(forms.ModelForm):

    # image = forms.FileField(required=True, widget=forms.FileInput(
    #     attrs={'class': 'form-control', 'multiple': True,  'accept': 'image/*'}))

    phone = forms.IntegerField(max_value=10000000000, required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': "Enter the Contact"}))

    father_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Enter the Fathers name"}))

    mother_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Mothers name'}))
    achoice = [

        ("Single Account", "Single Account"),
        ("Joint Account", "Joint Account")
    ]

    account_type = forms.TypedChoiceField(required=True, choices=achoice, widget=forms.Select(
        attrs={'class': 'form-control'}))

    choices = [
        ("Male", "Male"),
        ('Female', 'Female')

      ]
    gender = forms.TypedChoiceField(required=True, choices=choices, widget=forms.
                             Select(attrs={'class': 'form-control'}))

    YEARS = [x for x in range(1940, 2021)]

    date_of_birth = forms.DateField(label='What is your birth date?', widget=forms.SelectDateWidget(years=YEARS))

    address = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Address'}))

    city = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the City'}))

    state = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the State'}))

    pincode = forms.IntegerField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter the Pincode'}))

    class Meta:
        model = UserProfile
        fields = {'father_name', 'mother_name', 'phone', 'gender', 'date_of_birth',
                  'address', 'city', 'pincode', }


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


class AccountDetailsForm(forms.ModelForm):

    date_of_opening = forms.DateField(required=True, widget=forms.
                             SelectDateWidget(attrs={'class': 'form-control'}))

    achoice = [
        ("Single Account", "Single Account"),
        ("Joint Account", "Joint Account")
    ]
    account_type = forms.TypedChoiceField(required=True, choices=achoice, widget=forms.Select(
        attrs={'class': 'form-control'}))

    balance = forms.FloatField(required=True, widget=forms.NumberInput(
        attrs={'class': 'form-control'}))


    class Meta:
        model = Account_details
        fields = {'date_of_opening', 'account_type', 'balance'}


class MoneyTransferForm (forms.ModelForm):
    class Meta:
        model = models.MoneyTransfer
        fields = [
            "enter_your_user_name",
            "enter_the_destination_account_number",
            "enter_the_amount_to_be_transferred_in_INR"
        ]


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ["amount"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WithdrawalForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if self.user.account.balance < amount:
            raise forms.ValidationError(
                'You Can Not Withdraw More Than You Balance.'
            )

        return amount
