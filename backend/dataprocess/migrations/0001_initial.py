# Generated by Django 3.2.10 on 2022-01-27 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100, unique=True)),
                ('level', models.TextField(default='S', max_length=10)),
                ('gender', models.TextField(default='M', max_length=10)),
                ('member_num', models.IntegerField(default=1)),
                ('member_nationality', models.TextField(blank=True, default='', max_length=100)),
                ('agency', models.TextField(blank=True, default='', null=True)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('debut_date', models.DateField(null=True)),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('update_dt', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'artist',
            },
        ),
        migrations.CreateModel(
            name='ArtistProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.TextField(null=True)),
                ('height', models.TextField(null=True)),
                ('weight', models.TextField(null=True)),
            ],
            options={
                'db_table': 'artist_profile',
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('url', models.TextField()),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'platform',
            },
        ),
        migrations.CreateModel(
            name='CollectTarget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_url', models.TextField(default='')),
                ('target_url_2', models.TextField(default='')),
                ('channel', models.TextField(null=True)),
                ('channel_name', models.TextField(null=True)),
                ('sibling', models.BooleanField(default=False)),
                ('create_dt', models.DateTimeField(auto_now_add=True)),
                ('update_dt', models.DateTimeField(auto_now_add=True)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataprocess.artist')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataprocess.platform')),
            ],
            options={
                'db_table': 'collect_target',
            },
        ),
        migrations.CreateModel(
            name='CollectData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collect_items', models.JSONField(default=dict)),
                ('collect_target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataprocess.collecttarget')),
            ],
            options={
                'db_table': 'collect_data',
            },
        ),
        migrations.AddField(
            model_name='artist',
            name='profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='dataprocess.artistprofile'),
        ),
    ]
