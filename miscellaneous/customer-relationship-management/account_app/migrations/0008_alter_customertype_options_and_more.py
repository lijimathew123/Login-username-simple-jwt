# Generated by Django 4.2.9 on 2024-02-28 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0007_delete_platformcustomerlogin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customertype',
            options={'verbose_name': 'Customer Type', 'verbose_name_plural': 'Customer Type'},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'verbose_name': 'Organization', 'verbose_name_plural': 'Organization'},
        ),
        migrations.AlterModelOptions(
            name='organizationbranch',
            options={'verbose_name': 'Branch', 'verbose_name_plural': 'Branch'},
        ),
        migrations.AlterModelOptions(
            name='platformcustomer',
            options={'verbose_name': 'Platform Customer', 'verbose_name_plural': 'Platform Customer'},
        ),
        migrations.AlterModelOptions(
            name='platformcustomerdetails',
            options={'verbose_name': 'Platform Customer Details', 'verbose_name_plural': 'Platform Customer Details'},
        ),
    ]