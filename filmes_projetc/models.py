from django.db import models


class Filmes(models.Model):
    TIPO_FILME = "filme"
    TIPO_SERIE = "serie"
    TIPOS = (
        (TIPO_FILME, "Filme"),
        (TIPO_SERIE, "Série"),
    )

    id = models.AutoField(primary_key=True)
    tmdb_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    nome = models.CharField(max_length=200)
    genero = models.CharField(max_length=10, choices=TIPOS, default=TIPO_FILME)
    tamb = models.CharField(max_length=255, null=True, blank=True)
    sinopse = models.TextField(null=True, blank=True)
    data_filme = models.CharField(max_length=15, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True, null=True)
    atualizado_em = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ("-id",)
        constraints = [
            models.UniqueConstraint(
                fields=("tmdb_id", "genero"),
                name="filme_tmdb_tipo_unico",
            )
        ]

    def __str__(self):
        return self.nome


class MagnetcLinks(models.Model):
    id = models.OneToOneField(
        Filmes,
        on_delete=models.CASCADE,
        db_column="id",
        primary_key=True,
        related_name="links_download",
    )
    link_1080p_dub = models.TextField(blank=True)
    link_720p_dub = models.TextField(blank=True)
    link_1080p_eng = models.TextField(blank=True)
    link_720p_eng = models.TextField(blank=True)

    def __str__(self):
        return f"Links de {self.id.nome}"


class link_series(models.Model):
    id = models.AutoField(primary_key=True)
    link_eps = models.TextField(blank=True)
    ep_name = models.CharField(max_length=100)
    id_vinculado = models.ForeignKey(
        Filmes,
        on_delete=models.CASCADE,
        db_column="id_vinculado",
        related_name="episodios",
        limit_choices_to={"genero": Filmes.TIPO_SERIE},
    )

    class Meta:
        ordering = ("id",)
        constraints = [
            models.UniqueConstraint(
                fields=("id_vinculado", "ep_name"),
                name="episodio_nome_unico_por_serie",
            )
        ]

    def __str__(self):
        return f"{self.id_vinculado.nome} - {self.ep_name}"
