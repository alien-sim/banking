# Generated by Django 3.0.5 on 2020-04-09 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200407_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='contact',
            field=models.BigIntegerField(),
        ),
    ]