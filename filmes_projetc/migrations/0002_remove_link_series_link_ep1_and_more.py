# Generated by Django 5.0.6 on 2025-02-10 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmes_projetc', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link_series',
            name='link_ep1',
        ),
        migrations.RemoveField(
            model_name='link_series',
            name='link_ep10',
        ),
        migrations.RemoveField(
            model_name='link_series',
            name='link_ep11',
        ),
        migrations.RemoveField(
            model_name='link_series',
            name='link_ep12',
        ),
        migrations.RemoveField(
            model_name='link_series',
            name='link_ep13',
        ),
        migrations.RemoveField(
            model_name='link_series',
            name='link_ep2',
        ),
        migrations.RemoveField(
            model_name='link_series',
            name='link_ep3',
        ),
        migrations.RemoveField(
            model_name='link_series',
            name='link_ep4',
        ),
        migrations.RemoveField(
            model_name='link_series',
            name='link_ep5',
        ),
        migrations.RemoveField(
            model_name='link_series',
            name='link_ep6',
        ),
        migrations.RemoveField(
            model_name='link_series',
            name='link_ep7',
        ),
        migrations.RemoveField(
            model_name='link_series',
            name='link_ep8',
        ),
        migrations.RemoveField(
            model_name='link_series',
            name='link_ep9',
        ),
        migrations.AddField(
            model_name='link_series',
            name='ep_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
