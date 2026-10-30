// Menu lateral: expandir e recolher pelo botão de hamburguer (☰).
// O estado fica salvo no navegador (igual ao tema) e vale para as duas páginas.
// Padrão no primeiro acesso: recolhido — o hamburguer expande.

var MENU_SALVO = "menu";

function menuAberto() {
    return localStorage.getItem(MENU_SALVO) === "aberto";
}

function aplicarMenu(aberto) {
    var barra = document.getElementById("sidebar");
    if (!barra) return;
    barra.classList.toggle("recolhida", !aberto);
    localStorage.setItem(MENU_SALVO, aberto ? "aberto" : "recolhido");
}

document.addEventListener("DOMContentLoaded", function () {
    var botao = document.getElementById("botao-menu");
    if (botao) {
        botao.addEventListener("click", function () {
            aplicarMenu(!menuAberto());
        });
    }
    aplicarMenu(menuAberto()); // aplica o estado salvo
});
