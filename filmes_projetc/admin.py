from django.contrib import admin

from .models import Filmes, MagnetcLinks, link_series


class MagnetcLinksInline(admin.StackedInline):
    model = MagnetcLinks
    extra = 0
    max_num = 1


class EpisodioInline(admin.TabularInline):
    model = link_series
    extra = 0


@admin.register(Filmes)
class FilmesAdmin(admin.ModelAdmin):
    list_display = ("nome", "genero", "tmdb_id", "data_filme", "atualizado_em")
    list_filter = ("genero",)
    search_fields = ("nome", "tmdb_id")
    inlines = (MagnetcLinksInline, EpisodioInline)


@admin.register(MagnetcLinks)
class MagnetcLinksAdmin(admin.ModelAdmin):
    search_fields = ("id__nome",)


@admin.register(link_series)
class EpisodioAdmin(admin.ModelAdmin):
    list_display = ("ep_name", "id_vinculado")
    search_fields = ("ep_name", "id_vinculado__nome")
