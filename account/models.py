from uuid import uuid4
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import RegexValidator
from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)

choices = [
    ("Male", "Male"),
    ('Female', 'Female')

]
achoice = [

          ("Single Account", "Single Account"),
          ("Joint Account", "Joint Account")
      ]


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # image = models.FileField(upload_to='images/', null=True, blank=True,help_text="Upload only .png, .jpg & .jpeg image extension.")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=13, blank=True)
    father_name = models.CharField(max_length=30)
    mother_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=choices)
    account_type = models.CharField(max_length=20, choices=achoice)
    date_of_birth = models.DateTimeField()
    address = models.TextField()
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pincode = models.BigIntegerField()

    class Meta:
        db_table = 'user_profile'
        verbose_name_plural = 'USER_PROFILE'
        managed = True

    def __str__(self):
        return str(self.user)




class Account_details(models.Model):
    # id = models.UUIDField(primary_key=True,	default=uuid4, editable = False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.IntegerField()
    balance = models.IntegerField()
    user_name = models.CharField(max_length=150, default = None)

    class Meta:
        db_table = 'account_details'
        verbose_name_plural = 'ACCOUNT_DETAILS'
        managed = True

    def __str__(self):
        return str(self.id)


# tchoice = [
#         ('Online', 'Online'),
#         ('Credit-Card', 'Credit Card')
#     ]
#
#
# class Transactions(models.Model):
#     user = models.ForeignKey(User,  on_delete=models.CASCADE)
#     Recipient_Name = models.CharField(max_length=110)
#     transaction_type = models.CharField(max_length=110, choices=tchoice)
#     amount = models.FloatField()
#     account_no = models.PositiveIntegerField(
#         unique=True,
#         validators=[
#             MinValueValidator(10000000),
#             MaxValueValidator(99999999999999999)
#         ]
#     )
#     IFSC= models.CharField(max_length=110)
#     # date = models.DateTimeField(auto_now=True)
#     current_user = models.IntegerField()
#
#     class Meta:
#         db_table = 'transaction'
#         verbose_name_plural = 'TRANSACTION'
#         managed = True
#
#     def __str__(self):
#         return str(self.id)

class Transactions(models.Model):
    W = "Withdrawal"
    T = "Account Transfer"
    CHOICES = (
        (W, "Withdrawal"),
        (T, "Account Transfer"),
    )
    previous_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    transaction_time = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    transaction_id = models.CharField(max_length=100, default=0)
    type = models.CharField(max_length=50, choices=CHOICES, default=0)

    def __str__(self):
        return self.transaction_id

    def get_transaction_id(self):
        trans = str(self.user.username)+'_'+str(self.pk)
        return trans


class MoneyTransfer(models.Model):
    enter_your_user_name = models.CharField(max_length=150, default=None)
    enter_the_destination_account_number = models.IntegerField()
    enter_the_amount_to_be_transferred_in_INR = models.IntegerField()


class Withdrawal(models.Model):
    user = models.ForeignKey(User, related_name='withdrawals', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('10.00'))])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.id)