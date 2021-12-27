# Generated by Django 3.2.10 on 2021-12-24 00:28

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.TextField(unique=True)),
                ('yg_email', models.TextField(unique=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('has_email_auth', models.BooleanField(default=True)),
                ('email_auth_token', models.TextField(null=True)),
                ('admin_type', models.TextField(default='Regular User')),
            ],
            options={
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
