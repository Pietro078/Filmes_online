from django.db import migrations, models
import django.db.models.deletion


def preparar_relacionamentos(apps, schema_editor):
    Filmes = apps.get_model("filmes_projetc", "Filmes")
    MagnetcLinks = apps.get_model("filmes_projetc", "MagnetcLinks")
    Episodio = apps.get_model("filmes_projetc", "link_series")

    MagnetcLinks.objects.exclude(id__in=Filmes.objects.values("id")).delete()
    for filme_id in Filmes.objects.values_list("id", flat=True):
        MagnetcLinks.objects.get_or_create(id=filme_id)
    Episodio.objects.exclude(id_vinculado__in=Filmes.objects.values("id")).delete()


class Migration(migrations.Migration):
    dependencies = [("filmes_projetc", "0006_alter_link_series_ep_name")]

    operations = [
        migrations.RunPython(preparar_relacionamentos, migrations.RunPython.noop),
        migrations.AlterModelOptions(name="filmes", options={"ordering": ("-id",)}),
        migrations.AlterModelOptions(name="link_series", options={"ordering": ("id",)}),
        migrations.AlterField(
            model_name="filmes",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name="filmes",
            name="tmdb_id",
            field=models.PositiveIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="filmes",
            name="criado_em",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="filmes",
            name="atualizado_em",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name="filmes",
            name="nome",
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name="filmes",
            name="genero",
            field=models.CharField(
                choices=[("filme", "Filme"), ("serie", "Série")],
                default="filme",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="filmes",
            name="tamb",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="filmes",
            name="sinopse",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="filmes",
            name="data_filme",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="magnetclinks",
            name="id",
            field=models.OneToOneField(
                db_column="id",
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                related_name="links_download",
                serialize=False,
                to="filmes_projetc.filmes",
            ),
        ),
        migrations.AlterField(model_name="magnetclinks", name="link_1080p_dub", field=models.TextField(blank=True)),
        migrations.AlterField(model_name="magnetclinks", name="link_720p_dub", field=models.TextField(blank=True)),
        migrations.AlterField(model_name="magnetclinks", name="link_1080p_eng", field=models.TextField(blank=True)),
        migrations.AlterField(model_name="magnetclinks", name="link_720p_eng", field=models.TextField(blank=True)),
        migrations.AlterField(
            model_name="link_series",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(model_name="link_series", name="link_eps", field=models.TextField(blank=True)),
        migrations.AlterField(model_name="link_series", name="ep_name", field=models.CharField(max_length=100)),
        migrations.AlterField(
            model_name="link_series",
            name="id_vinculado",
            field=models.ForeignKey(
                db_column="id_vinculado",
                limit_choices_to={"genero": "serie"},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="episodios",
                to="filmes_projetc.filmes",
            ),
        ),
        migrations.AddConstraint(
            model_name="filmes",
            constraint=models.UniqueConstraint(fields=("tmdb_id", "genero"), name="filme_tmdb_tipo_unico"),
        ),
        migrations.AddConstraint(
            model_name="link_series",
            constraint=models.UniqueConstraint(fields=("id_vinculado", "ep_name"), name="episodio_nome_unico_por_serie"),
        ),
    ]
