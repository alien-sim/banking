# Generated by Django 3.0.4 on 2020-04-07 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200407_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account_details',
            name='User_account_no',
        ),
        migrations.AddField(
            model_name='account_details',
            name='balance',
            field=models.FloatField(default=0),
        ),
    ]