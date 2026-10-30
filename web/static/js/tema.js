// Tema claro/escuro compartilhado pelas páginas do sistema.
// O tema fica salvo no navegador (localStorage) e é aplicado no <html data-tema="...">.
// Os botões de tema usam data-tema-botao="claro" ou data-tema-botao="escuro".

var TEMA_SALVO = "tema";

function temaAtual() {
    return localStorage.getItem(TEMA_SALVO) === "escuro" ? "escuro" : "claro";
}

function aplicarTema(tema) {
    document.documentElement.dataset.tema = tema;
    localStorage.setItem(TEMA_SALVO, tema);
    // marca o botão ativo (Sol ou Lua) em todos os alternadores da página
    document.querySelectorAll("[data-tema-botao]").forEach(function (botao) {
        botao.classList.toggle("ativo", botao.dataset.temaBotao === tema);
    });
}

// aplica o tema salvo IMEDIATAMENTE (antes de a página desenhar, evita "flash" errado)
document.documentElement.dataset.tema = temaAtual();

// quando o HTML terminar de carregar, liga os botões de Sol/Lua
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-tema-botao]").forEach(function (botao) {
        botao.addEventListener("click", function () {
            aplicarTema(botao.dataset.temaBotao);
        });
    });
    aplicarTema(temaAtual());
});
