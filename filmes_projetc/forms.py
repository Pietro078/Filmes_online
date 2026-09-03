from django import forms

from .models import Filmes, MagnetcLinks, link_series


class FilmeForm(forms.Form):
    nome = forms.CharField(max_length=200, label="Nome no TMDB")
    genero = forms.ChoiceField(choices=Filmes.TIPOS, label="Tipo")
    link_1080p_dub = forms.CharField(required=False, label="1080p dublado")
    link_720p_dub = forms.CharField(required=False, label="720p dublado")
    link_1080p_eng = forms.CharField(required=False, label="1080p legendado")
    link_720p_eng = forms.CharField(required=False, label="720p legendado")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-control"

    def clean(self):
        dados = super().clean()
        campos = (
            "link_1080p_dub",
            "link_720p_dub",
            "link_1080p_eng",
            "link_720p_eng",
        )
        if (
            dados.get("genero") == Filmes.TIPO_FILME
            and not any(dados.get(campo, "").strip() for campo in campos)
        ):
            self.add_error("link_1080p_dub", "Informe pelo menos um link.")
        return dados

    @property
    def links(self):
        return {
            campo: self.cleaned_data.get(campo, "").strip()
            for campo in (
                "link_1080p_dub",
                "link_720p_dub",
                "link_1080p_eng",
                "link_720p_eng",
            )
        }


class EpisodioForm(forms.ModelForm):
    class Meta:
        model = link_series
        fields = ("ep_name", "link_eps")
        labels = {"ep_name": "Nome do episódio", "link_eps": "Link"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs["class"] = "form-control"

    def clean_ep_name(self):
        return self.cleaned_data["ep_name"].strip()

    def clean_link_eps(self):
        link = self.cleaned_data["link_eps"].strip()
        if not link:
            raise forms.ValidationError("Informe o link do episódio.")
        return link
