# Generated by Django 4.2.9 on 2024-03-14 04:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        ('account_app', '0001_initial'),
        ('Leads', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leads',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company'),
        ),
        migrations.AddField(
            model_name='leads',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leads',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer'),
        ),
        migrations.AddField(
            model_name='leads',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_app.organization'),
        ),
        migrations.AddField(
            model_name='leads',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Leads.leadsource'),
        ),
        migrations.AddField(
            model_name='leads',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Leads.leadstatus'),
        ),
        migrations.AddField(
            model_name='defaultleadfields',
            name='catogory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Leads.defaultleadcategory'),
        ),
        migrations.AddField(
            model_name='defaultleadfields',
            name='field_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_app.fieldtype'),
        ),
        migrations.AddField(
            model_name='defaultleadfields',
            name='lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Leads.leads'),
        ),
    ]
