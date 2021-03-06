# Generated by Django 3.2.8 on 2021-10-31 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0004_alter_product_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('code', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='stock', verbose_name='Price list')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
