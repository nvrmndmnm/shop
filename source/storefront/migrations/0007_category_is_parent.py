# Generated by Django 3.2.8 on 2021-10-31 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0006_alter_pricelist_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_parent',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
