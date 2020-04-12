from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# from phone_field import PhoneField
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)

class User_Profile(models.Model):
	g_choice = (
		("Male", "Male"),
		("Female", "Female")
		)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.FileField(upload_to='images/', null=True, blank=True,help_text="Upload only .png, .jpg & .jpeg image extension.")
	contact = models.BigIntegerField()
	father_name = models.CharField(max_length=30)
	mother_name = models.CharField(max_length=30)
	gender = models.CharField(max_length=10,choices=g_choice)
	date_of_birth = models.DateField()
	address = models.TextField()
	city = models.CharField(max_length=20)
	state = models.CharField(max_length=20)
	pincode = models.BigIntegerField()

	class Meta:
		db_table = 'user_profile'
		verbose_name_plural = 'USER_PROFILE'
		managed = True

	def __str__(self):
		return str(self.user.id)


class Account_details(models.Model):
	acc_choice = [
		('Current', 'Current'),
		('Saving', 'Saving'),
		('Capital', 'Capital'),
	]

	id = models.UUIDField(primary_key=True,	default=uuid4, editable = False)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	account_type = models.CharField(max_length=20,choices=acc_choice)
	balance = models.FloatField(default=0)
	date_of_opening = models.DateField(auto_now_add=True)
	current_user = models.IntegerField(default=0)

	class Meta:
		db_table = 'account_details'
		verbose_name_plural = 'ACCOUNT_DETAILS'
		managed = True

	# def __str__(self):
	# 	return str(self.id)

tchoice = [
	('Debit', 'Debit'),
	('Credit', 'Credit'),
	('Transfer','Transfer')
]



class Transactions(models.Model):
	# user = models.ForeignKey(User,  on_delete=models.CASCADE)
	transaction_type = models.CharField(max_length=110, choices=tchoice)
	amount = models.FloatField()
	current_user = models.IntegerField(default=0)
	datetime = models.DateTimeField(auto_now=True)
	recipient_acc = models.ForeignKey(Account_details,  on_delete=models.CASCADE)
	balance = models.FloatField()

	class Meta:
		db_table = 'transactions'
		verbose_name_plural = 'TRANSACTIONS'
		managed = True

	def __str__(self):
		return str(self.id)

class UserActivation(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=False)
	activation_key = models.CharField(max_length=40, blank=True)
	key_expires = models.DateTimeField()

	class Meta:
		db_table = 'user_activation'
		verbose_name_plural = 'USER_ACTIVATION'
		managed = True

	def __str__(self):
		return self.user.username
