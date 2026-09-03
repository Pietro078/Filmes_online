from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import IntegrityError
from django.db.models import F, Q
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from urllib.parse import urlencode

from .forms import EpisodioForm, FilmeForm
from .models import Filmes, MagnetcLinks, link_series
from .services.catalogo import FilmeDuplicadoError, cadastrar_filme, editar_filme
from .services.tmdb import TMDBError


class SuperuserRequiredMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser


class Home(ListView):
    model = Filmes
    template_name = "home.html"
    context_object_name = "filme"
    paginate_by = 20

    def get_queryset(self):
        queryset = Filmes.objects.all()
        termo = self.request.GET.get("pesquisa", "").strip()

        if termo:
            for palavra in termo.split():
                queryset = queryset.filter(
                    Q(nome__icontains=palavra) | Q(sinopse__icontains=palavra)
                )

        return queryset.order_by(
            F("atualizado_em").desc(nulls_last=True),
            F("criado_em").desc(nulls_last=True),
            "-id",
        )

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["termo_pesquisa"] = self.request.GET.get("pesquisa", "").strip()
        contexto["titulo_catalogo"] = (
            f'Resultados para “{contexto["termo_pesquisa"]}”'
            if contexto["termo_pesquisa"]
            else "Adicionados recentemente"
        )
        return contexto

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return TemplateResponse(
                request=self.request,
                template="components/catalogo_resultados.html",
                context=context,
                **response_kwargs,
            )
        return super().render_to_response(context, **response_kwargs)


class Filme(View):
    template_name = "filme.html"

    def get(self, request, id):
        filme = get_object_or_404(
            Filmes.objects.select_related("links_download").prefetch_related("episodios"),
            id=id,
        )
        return render(
            request,
            self.template_name,
            {
                "filme": filme,
                "links": getattr(filme, "links_download", None),
                "linksEP": filme.episodios.all(),
                "filme_form": FilmeForm(
                    initial={
                        "nome": filme.nome,
                        "genero": filme.genero,
                        **self._links_iniciais(filme),
                    }
                ),
                "episodio_form": EpisodioForm(),
            },
        )

    @staticmethod
    def _links_iniciais(filme):
        try:
            links = filme.links_download
        except MagnetcLinks.DoesNotExist:
            return {}
        return {
            "link_1080p_dub": links.link_1080p_dub,
            "link_720p_dub": links.link_720p_dub,
            "link_1080p_eng": links.link_1080p_eng,
            "link_720p_eng": links.link_720p_eng,
        }


class Cadastrar_filme(SuperuserRequiredMixin, View):
    template_name = "cadastrar_filme.html"

    def get(self, request):
        return render(request, self.template_name, {"form": FilmeForm()})

    def post(self, request):
        form = FilmeForm(request.POST)
        if form.is_valid():
            try:
                filme = cadastrar_filme(
                    nome=form.cleaned_data["nome"].strip(),
                    genero=form.cleaned_data["genero"],
                    links=form.links,
                )
            except (TMDBError, FilmeDuplicadoError) as erro:
                form.add_error("nome", str(erro))
            else:
                messages.success(request, "Título cadastrado com sucesso.")
                return redirect("filme", id=filme.id)
        return render(request, self.template_name, {"form": form})


class Excluir(SuperuserRequiredMixin, View):
    def post(self, request, id):
        filme = get_object_or_404(Filmes, id=id)
        filme.delete()
        messages.success(request, "Título excluído com sucesso.")
        return redirect("home")


class Editar_filme(SuperuserRequiredMixin, View):
    def post(self, request, id):
        filme = get_object_or_404(Filmes, id=id)
        acao = request.POST.get("acao", "editar_filme")

        if acao == "editar_filme":
            return self._editar_filme(request, filme)
        if filme.genero != Filmes.TIPO_SERIE:
            raise Http404("Este título não é uma série.")
        if acao == "criar_episodio":
            return self._criar_episodio(request, filme)
        if acao == "editar_episodio":
            return self._editar_episodio(request, filme)
        if acao == "excluir_episodio":
            return self._excluir_episodio(request, filme)
        return HttpResponseNotAllowed(["POST"])

    def _editar_filme(self, request, filme):
        form = FilmeForm(request.POST)
        if form.is_valid():
            try:
                editar_filme(
                    filme=filme,
                    nome=form.cleaned_data["nome"].strip(),
                    genero=form.cleaned_data["genero"],
                    links=form.links,
                )
            except (TMDBError, FilmeDuplicadoError) as erro:
                messages.error(request, str(erro))
            else:
                messages.success(request, "Título atualizado com sucesso.")
        else:
            messages.error(request, "Revise os campos informados.")
        return redirect("filme", id=filme.id)

    def _criar_episodio(self, request, filme):
        form = EpisodioForm(request.POST)
        if form.is_valid():
            episodio = form.save(commit=False)
            episodio.id_vinculado = filme
            try:
                episodio.save()
            except IntegrityError:
                messages.error(request, "Já existe um episódio com esse nome.")
            else:
                filme.save(update_fields=("atualizado_em",))
                messages.success(request, "Episódio criado com sucesso.")
        else:
            messages.error(request, "Revise os dados do episódio.")
        return redirect("filme", id=filme.id)

    def _episodio(self, request, filme):
        return get_object_or_404(
            link_series,
            id=request.POST.get("episodio_id"),
            id_vinculado=filme,
        )

    def _editar_episodio(self, request, filme):
        episodio = self._episodio(request, filme)
        form = EpisodioForm(request.POST, instance=episodio)
        if form.is_valid():
            form.save()
            filme.save(update_fields=("atualizado_em",))
            messages.success(request, "Episódio atualizado com sucesso.")
        else:
            messages.error(request, "Revise os dados do episódio.")
        return redirect("filme", id=filme.id)

    def _excluir_episodio(self, request, filme):
        self._episodio(request, filme).delete()
        filme.save(update_fields=("atualizado_em",))
        messages.success(request, "Episódio excluído com sucesso.")
        return redirect("filme", id=filme.id)


class Pesquisa(View):
    """Mantém a URL antiga, mas centraliza a busca na página inicial."""

    def _redirecionar(self, request):
        termo = (request.GET.get("pesquisa") or request.POST.get("pesquisa") or "").strip()
        destino = reverse("home")
        if termo:
            destino = f"{destino}?{urlencode({'pesquisa': termo})}"
        return redirect(destino)

    get = _redirecionar
    post = _redirecionar


class Abas(ListView):
    model = Filmes
    template_name = "abas.html"
    context_object_name = "resultado"

    def get_queryset(self):
        self.genero = self.kwargs["genero0"]
        if self.genero not in dict(Filmes.TIPOS):
            raise Http404("Categoria inválida.")
        return Filmes.objects.filter(genero=self.genero).order_by(
            F("atualizado_em").desc(nulls_last=True),
            F("criado_em").desc(nulls_last=True),
            "-id",
        )

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["genero"] = self.genero
        return contexto

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class Propaganda(View):
    def get(self, request, id):
        link = get_object_or_404(MagnetcLinks, id=id)
        return render(request, "propaganda.html", {"link": link})
