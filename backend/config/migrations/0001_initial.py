# Generated by Django 3.2.10 on 2022-02-03 03:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dataprocess', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_type', models.TextField(default='hour')),
                ('execute_time', models.TimeField()),
                ('period', models.TimeField(default=datetime.time(3, 0))),
                ('active', models.BooleanField(default=True)),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('update_dt', models.DateTimeField(auto_now_add=True)),
                ('collect_target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataprocess.collecttarget')),
            ],
            options={
                'db_table': 'schedule',
            },
        ),
        migrations.CreateModel(
            name='PlatformTargetItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_name', models.TextField(default='')),
                ('target_type', models.TextField(default='int')),
                ('xpath', models.TextField(blank=True, default='')),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('update_dt', models.DateTimeField(auto_now_add=True)),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataprocess.platform')),
            ],
            options={
                'db_table': 'platform_target_item',
            },
        ),
        migrations.CreateModel(
            name='CollectTargetItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_name', models.TextField(default='')),
                ('target_type', models.TextField(default='int')),
                ('xpath', models.TextField(blank=True, default='')),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('update_dt', models.DateTimeField(auto_now_add=True)),
                ('collect_target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataprocess.collecttarget')),
            ],
            options={
                'db_table': 'collect_target_item',
            },
        ),
        migrations.CreateModel(
            name='AuthInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_type', models.TextField(default='login')),
                ('user_id', models.TextField(null=True)),
                ('user_pw', models.TextField(null=True)),
                ('api_key', models.TextField(null=True)),
                ('secret_key', models.TextField(null=True)),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('update_dt', models.DateTimeField(auto_now_add=True)),
                ('collect_target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataprocess.collecttarget')),
            ],
            options={
                'db_table': 'auth_info',
            },
        ),
    ]
