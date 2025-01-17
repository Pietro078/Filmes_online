# Generated by Django 5.1.4 on 2024-12-27 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filmes',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('genero', models.CharField(blank=True, max_length=100)),
                ('tamb', models.CharField(max_length=50, null=True)),
                ('sinopse', models.CharField(max_length=400, null=True)),
                ('data_filme', models.CharField(max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='link_series',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('link_eps', models.CharField(blank=True, max_length=100)),
                ('link_ep1', models.CharField(blank=True, max_length=100)),
                ('link_ep2', models.CharField(blank=True, max_length=100)),
                ('link_ep3', models.CharField(blank=True, max_length=100)),
                ('link_ep4', models.CharField(blank=True, max_length=100)),
                ('link_ep5', models.CharField(blank=True, max_length=100)),
                ('link_ep6', models.CharField(blank=True, max_length=100)),
                ('link_ep7', models.CharField(blank=True, max_length=100)),
                ('link_ep8', models.CharField(blank=True, max_length=100)),
                ('link_ep9', models.CharField(blank=True, max_length=100)),
                ('link_ep10', models.CharField(blank=True, max_length=100)),
                ('link_ep11', models.CharField(blank=True, max_length=100)),
                ('link_ep12', models.CharField(blank=True, max_length=100)),
                ('link_ep13', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MagnetcLinks',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('link_1080p_dub', models.CharField(blank=True, max_length=100)),
                ('link_720p_dub', models.CharField(blank=True, max_length=100)),
                ('link_1080p_eng', models.CharField(blank=True, max_length=100)),
                ('link_720p_eng', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
