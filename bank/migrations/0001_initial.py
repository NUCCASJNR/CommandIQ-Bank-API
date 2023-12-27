# Generated by Django 5.0 on 2023-12-27 13:01

import bank.models.user
import datetime
import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account_number', models.IntegerField(unique=True)),
                ('account_name', models.CharField(max_length=100)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
            options={
                'db_table': 'accounts',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event_type', models.CharField(max_length=50)),
                ('payload', models.JSONField()),
            ],
            options={
                'db_table': 'events',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_type', models.CharField(choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal'), ('transfer', 'Transfer')], max_length=10)),
                ('account_id', models.ForeignKey(db_column='account_id', on_delete=django.db.models.deletion.CASCADE, to='bank.account')),
            ],
            options={
                'db_table': 'transactions',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=60, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('profile_picture', models.ImageField(max_length=255, null=True, upload_to=bank.models.user.user_profile_image_path)),
                ('groups', models.ManyToManyField(blank=True, related_name='bank_user_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='bank_user_permissions', to='auth.permission')),
            ],
            options={
                'db_table': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='bank.user'),
        ),
    ]
