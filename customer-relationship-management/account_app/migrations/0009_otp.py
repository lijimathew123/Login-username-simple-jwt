# Generated by Django 4.2.9 on 2024-02-29 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0008_alter_customertype_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('otp_value', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
