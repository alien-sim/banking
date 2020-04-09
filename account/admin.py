from django.contrib import admin
from account.models import User_Profile, Account_details, Transactions, Deposit, Withdrawal
# Register your models here.

admin.site.register(User_Profile)
admin.site.register(Account_details)
admin.site.register(Transactions)
admin.site.register(Deposit)
admin.site.register(Withdrawal)