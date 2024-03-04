# Generated by Django 4.2.9 on 2024-02-27 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0002_organization_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationbranch',
            name='owner',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
