(() => {
    const form = document.querySelector("#catalogo-search-form");
    const input = document.querySelector("#catalogo-search-input");
    const main = document.querySelector("#conteudo");

    if (!form || !input || !main) return;

    let timer;
    let controller;

    async function atualizarCatalogo(url, atualizarHistorico = true) {
        controller?.abort();
        controller = new AbortController();

        let resultados = document.querySelector("#catalogo-resultados");
        resultados?.classList.add("is-loading");
        resultados?.setAttribute("aria-busy", "true");

        try {
            const resposta = await fetch(url, {
                headers: { "X-Requested-With": "XMLHttpRequest" },
                signal: controller.signal,
            });
            if (!resposta.ok) throw new Error(`Erro HTTP ${resposta.status}`);

            const html = await resposta.text();
            resultados = document.querySelector("#catalogo-resultados");
            if (resultados) resultados.outerHTML = html;
            else main.innerHTML = html;

            if (atualizarHistorico) history.replaceState({}, "", url);
        } catch (erro) {
            if (erro.name !== "AbortError") form.submit();
        }
    }

    function urlDaPesquisa() {
        const url = new URL(form.action, window.location.origin);
        const termo = input.value.trim();
        if (termo) url.searchParams.set("pesquisa", termo);
        return url;
    }

    form.addEventListener("submit", (evento) => {
        evento.preventDefault();
        clearTimeout(timer);
        atualizarCatalogo(urlDaPesquisa());
    });

    input.addEventListener("input", () => {
        clearTimeout(timer);
        timer = setTimeout(() => atualizarCatalogo(urlDaPesquisa()), 350);
    });

    document.addEventListener("click", (evento) => {
        const link = evento.target.closest("[data-catalogo-link]");
        if (!link) return;
        evento.preventDefault();
        const url = new URL(link.href, window.location.origin);
        input.value = url.searchParams.get("pesquisa") || "";
        atualizarCatalogo(url);
    });
})();
