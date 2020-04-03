from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class User_Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.FileField(upload_to='images/', null=True, blank=True,help_text="Upload only .png, .jpg & .jpeg image extension.")
	contact = models.BigIntegerField()
	father_name = models.CharField(max_length=30)
	mother_name = models.CharField(max_length=30)
	gender = models.CharField(max_length=10)
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
		return self.user.id

class Account_details(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	account_type = models.CharField(max_length=20)
	date_of_joining = models.DateField()

	class Meta:
		db_table = 'account_details'
		verbose_name_plural = 'ACCOUNT_DETAILS'
		managed = True

	def __str__(self):
		return str(self.id)