# Generated by Django 4.1.13 on 2024-03-20 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Leads', '0008_alter_defaultleadfields_display_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leads',
            name='converted_to_customer',
        ),
    ]