# Generated by Django 3.2.10 on 2021-12-24 00:28

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
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.TextField(unique=True)),
                ('agency', models.TextField(null=True)),
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
                ('url', models.TextField(unique=True)),
                ('description', models.TextField(null=True)),
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
                ('collect_item', models.JSONField(default=dict)),
                ('collect_target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataprocess.collecttarget')),
            ],
            options={
                'db_table': 'collect_data',
            },
        ),
        migrations.AddField(
            model_name='artist',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dataprocess.artistprofile'),
        ),
    ]