# Generated by Django 5.0.2 on 2024-03-21 09:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Leads', '0010_defaultleadfields_required'),
        ('deals', '0004_alter_defaultdealfields_display_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='defaultdealfields',
            name='required',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='deals',
            name='leads',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Leads.leads'),
        ),
    ]
