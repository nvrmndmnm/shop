# Generated by Django 3.2.8 on 2021-11-02 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0002_auto_20211102_0746'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('street', models.CharField(max_length=100, verbose_name='Street')),
                ('building', models.CharField(max_length=20, verbose_name='Building')),
                ('apartment', models.CharField(blank=True, max_length=20, null=True, verbose_name='Apartment')),
                ('country', models.CharField(max_length=50, verbose_name='Country')),
                ('zip_code', models.CharField(max_length=20, verbose_name='Zip code')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Address user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
