// Página Auditoria de Faturas: filtros de cliente, UC (cascata) e período
// de referência, com consulta aos endpoints /api/clientes, /api/ucs e /api/faturas.

const filtroCliente = document.getElementById("filtro-cliente");
const filtroUc = document.getElementById("filtro-uc");
const filtroDe = document.getElementById("filtro-de");
const filtroAte = document.getElementById("filtro-ate");
const filtroStatus = document.getElementById("filtro-status");
const corpoTabela = document.getElementById("corpo-faturas");
const toast = document.getElementById("toast");

let carregando = false;
let timerToast = null;

function mostrarToast(status, mensagem) {
    toast.className = "toast " + status;
    toast.textContent = mensagem;
    toast.hidden = false;
    clearTimeout(timerToast);
    timerToast = setTimeout(() => { toast.hidden = true; }, 6000);
}

// ---------- clientes (dropdown 1) ----------

async function carregarClientes() {
    const resposta = await fetch("/api/clientes");
    if (!resposta.ok) throw new Error("Falha ao carregar clientes (" + resposta.status + ").");
    const clientes = await resposta.json();

    filtroCliente.innerHTML = '<option value="">Todos os clientes</option>';
    for (const cliente of clientes) {
        const option = document.createElement("option");
        option.value = cliente.id;
        option.textContent = cliente.nome;
        filtroCliente.appendChild(option);
    }
}

// ---------- UCs do cliente selecionado (dropdown 2, cascata) ----------

async function carregarUcs(clienteId) {
    filtroUc.disabled = !clienteId;
    filtroUc.innerHTML = '<option value="">Selecione um cliente primeiro</option>';
    filtroUc.value = "";
    if (!clienteId) return;

    const resposta = await fetch("/api/ucs?cliente_id=" + clienteId);
    if (!resposta.ok) throw new Error("Falha ao carregar UCs (" + resposta.status + ").");
    const ucs = await resposta.json();

    for (const uc of ucs) {
        const option = document.createElement("option");
        option.value = uc.id;
        option.textContent = uc.uc;
        filtroUc.appendChild(option);
    }
}

// ---------- faturas (tabela de resultados) ----------

async function carregarFaturas() {
    if (carregando) return;
    carregando = true;
    try {
        const params = new URLSearchParams();
        if (filtroCliente.value) params.set("cliente_id", filtroCliente.value);
        if (filtroUc.value) params.set("uc_id", filtroUc.value);
        if (filtroDe.value) params.set("de", filtroDe.value);
        if (filtroAte.value) params.set("ate", filtroAte.value);
        if (filtroStatus.value) params.set("status", filtroStatus.value);

        const resposta = await fetch("/api/faturas?" + params.toString());
        if (!resposta.ok) throw new Error("Falha ao carregar faturas (" + resposta.status + ").");
        const faturas = await resposta.json();

        corpoTabela.innerHTML = "";
        if (faturas.length === 0) {
            const tr = document.createElement("tr");
            const td = document.createElement("td");
            td.colSpan = 7;
            td.className = "sem-linhas";
            td.textContent = "Nenhuma fatura encontrada";
            tr.appendChild(td);
            corpoTabela.appendChild(tr);
            return;
        }

        for (const fatura of faturas) corpoTabela.appendChild(criarLinha(fatura));
    } finally {
        carregando = false;
    }
}

function criarLinha(fatura) {
    const tr = document.createElement("tr");

    const tdCliente = document.createElement("td");
    tdCliente.className = "col-cliente";
    tdCliente.textContent = fatura.cliente;

    const tdUc = document.createElement("td");
    tdUc.className = "col-uc";
    tdUc.textContent = fatura.numero_uc;

    const tdMes = document.createElement("td");
    tdMes.textContent = formatarMesRef(fatura.mes_ref);

    const tdValor = document.createElement("td");
    tdValor.textContent = formatarValor(fatura.valor_total);

    const tdVenc = document.createElement("td");
    tdVenc.textContent = formatarVencimento(fatura.vencimento);

    const tdPdf = document.createElement("td");
    tdPdf.textContent = fatura.nome_pdf || "—";

    const tdStatus = document.createElement("td");
    tdStatus.appendChild(criarIndicadorStatus(fatura.status));

    tr.append(tdCliente, tdUc, tdMes, tdValor, tdVenc, tdPdf, tdStatus);
    return tr;
}

function criarIndicadorStatus(status) {
    const span = document.createElement("span");
    span.className = "status-indicador";

    if (status === "necessita_analise") {
        span.classList.add("status-analise");
        span.innerHTML = '<span class="icone-status" aria-hidden="true">🛑</span> necessita análise';
    } else {
        span.classList.add("status-validado");
        span.innerHTML = '<span class="icone-status" aria-hidden="true">Ⓥ</span> validado';
    }
    return span;
}

// "2026-10" -> "10/2026"
function formatarMesRef(ym) {
    const partes = String(ym).split("-");
    return partes[1] + "/" + partes[0];
}

// 2627.4 -> "2.627,40" (pt-BR, sem moeda)
function formatarValor(valor) {
    return Number(valor).toLocaleString("pt-BR", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
}

// "2026-10-16" -> "16/10/2026"
function formatarVencimento(iso) {
    const partes = String(iso).split("-");
    return partes[2] + "/" + partes[1] + "/" + partes[0];
}

// ---------- eventos ----------

filtroCliente.addEventListener("change", async function () {
    try {
        await carregarUcs(filtroCliente.value ? filtroCliente.value : null);
    } catch (erro) {
        mostrarToast("FALHA", erro.message);
    }
    await carregarFaturasComTratamento();
});

filtroUc.addEventListener("change", carregarFaturasComTratamento);
filtroDe.addEventListener("change", carregarFaturasComTratamento);
filtroAte.addEventListener("change", carregarFaturasComTratamento);
filtroStatus.addEventListener("change", carregarFaturasComTratamento);

async function carregarFaturasComTratamento() {
    try {
        await carregarFaturas();
    } catch (erro) {
        mostrarToast("FALHA", erro.message);
    }
}

// ---------- início ----------

carregarClientes().then(function () {
    carregarUcs(null);
    carregarFaturasComTratamento();
});
