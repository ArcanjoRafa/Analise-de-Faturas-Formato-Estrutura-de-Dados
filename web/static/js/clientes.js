// Página Gestão de Clientes: listagem, busca, filtro por documento, criar e excluir clientes.

const corpoTabela = document.getElementById("corpo-clientes");
const campoBusca = document.getElementById("campo-busca");
const botaoCriar = document.getElementById("botao-criar");
const listaDocumentos = document.getElementById("lista-documentos");
const toast = document.getElementById("toast");

// Modal
const modal = document.getElementById("modal");
const modalOverlay = document.getElementById("modal-overlay");
const modalNome = document.getElementById("modal-nome");
const modalDocumento = document.getElementById("modal-documento");
const botaoModalCriar = document.getElementById("modal-criar");
const botaoModalCancelar = document.getElementById("modal-cancelar");
const modalErro = document.getElementById("modal-erro");

let enviando = false;
let timerToast = null;
let timerBusca = null;
let documentosSelecionados = new Set(); // CPF/CNPJ marcados no filtro lateral

function mostrarToast(status, mensagem) {
    toast.className = "toast " + status;
    toast.textContent = mensagem;
    toast.hidden = false;
    clearTimeout(timerToast);
    timerToast = setTimeout(() => { toast.hidden = true; }, 6000);
}

function esconderModalErro() {
    modalErro.textContent = "";
    modalErro.hidden = true;
}

async function carregarDocumentos() {
    const resposta = await fetch("/api/clientes/documentos");
    if (!resposta.ok) throw new Error("Falha ao carregar documentos (" + resposta.status + ").");
    const documentos = await resposta.json();

    listaDocumentos.innerHTML = "";
    if (documentos.length === 0) {
        const p = document.createElement("p");
        p.className = "sem-linhas";
        p.textContent = "Nenhum documento cadastrado.";
        listaDocumentos.appendChild(p);
        return;
    }

    for (const doc of documentos) {
        const label = document.createElement("label");
        label.style.display = "block";
        label.style.marginBottom = "6px";

        const cb = document.createElement("input");
        cb.type = "checkbox";
        cb.value = doc.cpf_cnpj;
        cb.style.marginRight = "8px";
        cb.addEventListener("change", function () {
            if (this.checked) documentosSelecionados.add(doc.cpf_cnpj);
            else documentosSelecionados.delete(doc.cpf_cnpj);
            carregarClientes();
        });

        label.appendChild(cb);
        label.appendChild(document.createTextNode(doc.cpf_cnpj));
        listaDocumentos.appendChild(label);
    }
}

async function carregarClientes() {
    const params = new URLSearchParams();
    if (campoBusca.value.trim()) params.set("q", campoBusca.value.trim());
    documentosSelecionados.forEach(function (doc) {
        params.append("documento", doc);
    });

    const resposta = await fetch("/api/clientes?" + params.toString());
    if (!resposta.ok) throw new Error("Falha ao carregar clientes (" + resposta.status + ").");
    const clientes = await resposta.json();

    corpoTabela.innerHTML = "";
    if (clientes.length === 0) {
        const tr = document.createElement("tr");
        const td = document.createElement("td");
        td.colSpan = 3;
        td.className = "sem-linhas";
        td.textContent = "Nenhum cliente encontrado.";
        tr.appendChild(td);
        corpoTabela.appendChild(tr);
        return;
    }

    for (const cliente of clientes) corpoTabela.appendChild(criarLinha(cliente));
}

function criarLinha(cliente) {
    const tr = document.createElement("tr");

    const tdNome = document.createElement("td");
    tdNome.textContent = cliente.nome;

    const tdDoc = document.createElement("td");
    tdDoc.textContent = cliente.cpf_cnpj;

    const tdAcao = document.createElement("td");
    const botao = document.createElement("button");
    botao.type = "button";
    botao.className = "botao-excluir";
    botao.title = "Excluir " + cliente.nome;
    botao.setAttribute("aria-label", "Excluir " + cliente.nome);
    botao.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>';
    botao.addEventListener("click", () => excluirCliente(cliente.id, cliente.nome));
    tdAcao.appendChild(botao);

    tr.append(tdNome, tdDoc, tdAcao);
    return tr;
}

async function excluirCliente(id, nome) {
    if (!confirm("Tem certeza que deseja excluir o cliente \"" + nome + "\"?")) return;

    try {
        const resposta = await fetch("/api/clientes/" + id, { method: "DELETE" });
        if (resposta.status === 404) {
            mostrarToast("FALHA", "Cliente não encontrado.");
            await carregarClientes();
            return;
        }
        if (!resposta.ok) throw new Error("Falha ao excluir (" + resposta.status + ").");
        mostrarToast("SUCESSO", "Cliente excluído.");
        await carregarClientes();
        await carregarDocumentos(); // atualiza a lista de documentos do filtro lateral
    } catch (erro) {
        mostrarToast("FALHA", "Não foi possível excluir o cliente.");
    }
}

// ---------- criar cliente ----------
function abrirModal() {
    modalNome.value = "";
    modalDocumento.value = "";
    esconderModalErro();
    modal.hidden = false;
    modalNome.focus();
}

function fecharModal() {
    modal.hidden = true;
}

botaoCriar.addEventListener("click", abrirModal);
botaoModalCancelar.addEventListener("click", fecharModal);
modalOverlay.addEventListener("click", fecharModal);

botaoModalCriar.addEventListener("click", async function () {
    if (enviando) return;
    const nome = modalNome.value.trim();
    const documento = modalDocumento.value.trim();

    if (!nome || !documento) {
        modalErro.textContent = "Preencha Nome e CPF/CNPJ.";
        modalErro.hidden = false;
        return;
    }

    enviando = true;
    botaoModalCriar.disabled = true;
    botaoModalCriar.textContent = "Criando...";

    try {
        const resposta = await fetch("/api/clientes", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nome: nome, cpf_cnpj: documento }),
        });
        const resultado = await resposta.json();

        if (resposta.status === 409) {
            modalErro.textContent = resultado.mensagem || "CPF/CNPJ já cadastrado.";
            modalErro.hidden = false;
            return;
        }
        if (!resposta.ok) throw new Error("Falha ao criar (" + resposta.status + ").");

        fecharModal();
        mostrarToast("SUCESSO", "Cliente criado com sucesso.");
        await carregarClientes();
        await carregarDocumentos(); // o novo documento aparece no filtro lateral
    } catch (erro) {
        mostrarToast("FALHA", "Não foi possível criar o cliente.");
    } finally {
        enviando = false;
        botaoModalCriar.disabled = false;
        botaoModalCriar.textContent = "Criar";
    }
});

// ---------- busca e filtro ----------
function agendarRecarga() {
    clearTimeout(timerBusca);
    timerBusca = setTimeout(carregarClientes, 300);
}

campoBusca.addEventListener("input", agendarRecarga);

// ---------- início ----------
carregarClientes();
carregarDocumentos();
