# Generated by Django 4.2.9 on 2024-03-14 04:46

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformCustomer',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, null=True, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=15)),
                ('source', models.CharField(default='website', max_length=255)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('is_phone_verified', models.BooleanField(default=False)),
                ('created_at', models.PositiveIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Platform Customer',
                'verbose_name_plural': 'Platform Customer',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Customer Type',
                'verbose_name_plural': 'Customer Type',
            },
        ),
        migrations.CreateModel(
            name='FieldType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('organization_name', models.CharField(max_length=30)),
                ('business_type', models.CharField(max_length=25)),
                ('industry_type', models.CharField(max_length=25)),
                ('logo', models.ImageField(upload_to='logos/')),
                ('banner', models.ImageField(upload_to='banners/')),
                ('address', models.TextField()),
                ('location', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=40)),
                ('phone', models.CharField(max_length=12, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organization',
            },
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('otp_value', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialChannel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('icon', models.ImageField(upload_to='icons/')),
                ('name', models.CharField(max_length=255)),
                ('order', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Social Channel',
                'verbose_name_plural': 'Social Channel',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='UserLastLogin',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('last_login', models.PositiveIntegerField(blank=True, null=True)),
                ('status', models.CharField(max_length=20)),
                ('last_login_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlatformCustomerSocialChannels',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('profile_id', models.CharField(max_length=255)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_channels', to=settings.AUTH_USER_MODEL)),
                ('social_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_profiles', to='account_app.socialchannel')),
            ],
            options={
                'verbose_name': 'Platform customer social profile',
                'verbose_name_plural': 'Platform customer social profile',
            },
        ),
        migrations.CreateModel(
            name='PlatformCustomerPermissions',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer Permission',
                'verbose_name_plural': 'Customer Permission',
            },
        ),
        migrations.CreateModel(
            name='PlatformCustomerDetails',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=25)),
                ('phone_2', models.CharField(max_length=15)),
                ('dob', models.DateField()),
                ('image', models.ImageField(upload_to='profiles/')),
                ('address', models.JSONField()),
                ('state', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
                ('currency', models.CharField(max_length=20)),
                ('date_format', models.CharField(max_length=35)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('theme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account_app.theme')),
            ],
            options={
                'verbose_name': 'Platform Customer Details',
                'verbose_name_plural': 'Platform Customer Details',
            },
        ),
        migrations.CreateModel(
            name='OrganizationSocialChannel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('profile_id', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_app.organization')),
                ('social_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_app.socialchannel')),
            ],
            options={
                'verbose_name': 'Organization social profile',
                'verbose_name_plural': 'Organization social profile',
            },
        ),
        migrations.CreateModel(
            name='OrganizationBranch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=25)),
                ('phone', models.CharField(max_length=12, unique=True)),
                ('country', models.CharField(default='', max_length=255)),
                ('is_default', models.BooleanField(default=False)),
                ('organization_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_app.organization')),
            ],
            options={
                'verbose_name': 'Branch',
                'verbose_name_plural': 'Branch',
            },
        ),
        migrations.AddField(
            model_name='platformcustomer',
            name='customer_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account_app.customertype'),
        ),
        migrations.AddField(
            model_name='platformcustomer',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='platformcustomer',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
