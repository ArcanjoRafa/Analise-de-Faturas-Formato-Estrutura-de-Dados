// Página de upload de faturas: seleção de arquivo (clique ou arrastar),
// envio via POST /api/upload e tabela de histórico.

const areaUpload = document.getElementById("area-upload");
const campoArquivo = document.getElementById("campo-arquivo");
const nomeArquivo = document.getElementById("nome-arquivo");
const aviso = document.getElementById("aviso");
const botaoUpload = document.getElementById("botao-upload");
const botaoCancelar = document.getElementById("botao-cancelar");
const corpoHistorico = document.getElementById("corpo-historico");
const toast = document.getElementById("toast");

const ICONE_DOWNLOAD =
    '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor"' +
    ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<path d="M12 4v11"/><path d="M7 10l5 5 5-5"/><path d="M5 20h14"/></svg>';

let arquivoSelecionado = null; // File escolhido pelo clique ou pelo arrastar
let enviando = false;          // trava enquanto o servidor processa
let timerToast = null;

// ---------- seleção do arquivo ----------

function selecionarArquivo(arquivo) {
    if (!arquivo) return;
    if (!arquivo.name.toLowerCase().endsWith(".pdf")) {
        mostrarAviso('"' + arquivo.name + '" não é um PDF. Apenas arquivos .pdf são aceitos.');
        return; // não seleciona arquivo que não é .pdf
    }
    esconderAviso();
    arquivoSelecionado = arquivo;
    nomeArquivo.textContent = arquivo.name;
    botaoUpload.disabled = false;
    botaoCancelar.disabled = false;
}

function limparSelecao() {
    arquivoSelecionado = null;
    campoArquivo.value = "";
    nomeArquivo.textContent = "";
    botaoUpload.disabled = true;
    botaoCancelar.disabled = true;
    botaoUpload.textContent = "Realizar Upload";
}

// clique na área abre o seletor de arquivos do navegador
areaUpload.addEventListener("click", () => campoArquivo.click());
campoArquivo.addEventListener("change", () => selecionarArquivo(campoArquivo.files[0]));

// arrastar: destaca a área; soltar seleciona o arquivo
["dragenter", "dragover"].forEach((tipo) =>
    areaUpload.addEventListener(tipo, (evento) => {
        evento.preventDefault();
        areaUpload.classList.add("arrastando");
    })
);
areaUpload.addEventListener("dragleave", () => areaUpload.classList.remove("arrastando"));
areaUpload.addEventListener("drop", (evento) => {
    evento.preventDefault();
    areaUpload.classList.remove("arrastando");
    selecionarArquivo(evento.dataTransfer.files[0]); // um arquivo por vez
});

// Cancelar: esvazia o campo e desativa os botões (não chama o servidor)
botaoCancelar.addEventListener("click", limparSelecao);
botaoUpload.addEventListener("click", realizarUpload);

// ---------- upload ----------

async function realizarUpload() {
    if (!arquivoSelecionado || enviando) return;
    enviando = true;
    botaoUpload.disabled = true;
    botaoCancelar.disabled = true;
    botaoUpload.textContent = "Processando...";

    const dados = new FormData();
    dados.append("arquivo", arquivoSelecionado);

    try {
        const resposta = await fetch("/api/upload", { method: "POST", body: dados });
        const resultado = await resposta.json();
        mostrarToast(resultado.status || "FALHA", resultado.mensagem || "");
        limparSelecao();              // esvazia o campo
        await carregarHistorico();     // atualiza a tabela
    } catch (erro) {
        mostrarToast("FALHA", "Não foi possível falar com o servidor.");
    } finally {
        enviando = false;
    }
}

// ---------- histórico ----------

async function carregarHistorico() {
    const resposta = await fetch("/api/historico");
    const linhas = await resposta.json();
    corpoHistorico.innerHTML = "";

    if (linhas.length === 0) {
        const tr = document.createElement("tr");
        const td = document.createElement("td");
        td.colSpan = 5;
        td.className = "sem-linhas";
        td.textContent = "Nenhuma tentativa de upload ainda.";
        tr.appendChild(td);
        corpoHistorico.appendChild(tr);
        return;
    }

    for (const linha of linhas) corpoHistorico.appendChild(criarLinha(linha));
}

// "2026-10-27T15:04:05" -> "27/10/2026 15:04"
function formatarData(iso) {
    const d = new Date(iso);
    const dia = String(d.getDate()).padStart(2, "0");
    const mes = String(d.getMonth() + 1).padStart(2, "0");
    const hora = String(d.getHours()).padStart(2, "0");
    const minuto = String(d.getMinutes()).padStart(2, "0");
    return dia + "/" + mes + "/" + d.getFullYear() + " " + hora + ":" + minuto;
}

function criarLinha(linha) {
    const tr = document.createElement("tr");

    const tdNome = document.createElement("td");
    tdNome.textContent = linha.nome_pdf;

    const tdData = document.createElement("td");
    tdData.textContent = formatarData(linha.data_upload);

    const tdStatus = document.createElement("td");
    const badge = document.createElement("span");
    badge.className = "badge status-" + linha.status;
    badge.textContent = linha.status;
    tdStatus.appendChild(badge);

    const tdErro = document.createElement("td");
    tdErro.className = "col-erro";
    tdErro.textContent = linha.erro || ""; // vazio quando não houver

    const tdAcao = document.createElement("td");
    const link = document.createElement("a");
    link.className = "botao-download";
    link.href = "/api/download/" + linha.id;
    link.title = "Baixar " + linha.nome_pdf;
    link.setAttribute("aria-label", "Baixar " + linha.nome_pdf);
    link.innerHTML = ICONE_DOWNLOAD;
    tdAcao.appendChild(link);

    tr.append(tdNome, tdData, tdStatus, tdErro, tdAcao);
    return tr;
}

// ---------- avisos e toast ----------

function mostrarAviso(mensagem) {
    aviso.textContent = mensagem;
    aviso.hidden = false;
}

function esconderAviso() {
    aviso.textContent = "";
    aviso.hidden = true;
}

function mostrarToast(status, mensagem) {
    toast.className = "toast " + status;
    toast.textContent = mensagem;
    toast.hidden = false;
    clearTimeout(timerToast);
    timerToast = setTimeout(() => { toast.hidden = true; }, 6000);
}

// ---------- início: carrega o histórico ao abrir a página ----------

carregarHistorico();
