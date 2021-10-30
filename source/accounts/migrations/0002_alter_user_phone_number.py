# Generated by Django 3.2.8 on 2021-10-29 12:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message='Should be a valid phone number.', regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
