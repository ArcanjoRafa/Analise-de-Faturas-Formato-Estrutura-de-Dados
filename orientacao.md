# Orientação — Analise_Fatura_Energisa

> **Leia este arquivo antes de qualquer trabalho neste projeto.**
> Sistema Python que extrai dados de faturas de energia da Energisa (PDF) e persiste num PostgreSQL local.
> Gerado em 25/10/2026 no tour de apresentação do projeto.

## 1. O que o sistema faz

1. Lê PDFs de faturas da Energisa de uma pasta (`main.py` aponta para `C:\Users\rafae\Downloads\pdfs_fatura`)
2. Detecta o **formato da fatura** (A ou B) pela largura da página
3. Extrai os dados por **coordenadas (x, y) fixas + regex**: cliente, CPF/CNPJ, UC, endereço, CEP, medidor, leituras, tributos (PIS/PASEP, COFINS, ICMS), itens da fatura, total, mês de referência, vencimento, data de apresentação e sumário elétrico (leituras do medidor)
4. Monta objetos de domínio em `models/` (dataclasses — **tudo como string**)
5. Grava no PostgreSQL com upsert/deduplicação: cliente, UC e medidor são reutilizados se já existirem; a fatura é única por (UC, mês de referência)

## 2. Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12 (venv em `.venv/`) |
| Extração de PDF | PyMuPDF (`fitz`) **e** pdfplumber (usados juntos) |
| ORM | SQLAlchemy 2.x (estilo 2.0: `Mapped`/`mapped_column`, `DeclarativeBase`) |
| Banco | PostgreSQL local — `localhost:5432/postgres`, user `postgres` (credenciais hardcoded em `database/conection.py`) |
| Driver | psycopg2 |

Possui `requirements.txt` na raiz (flask, pymupdf, pdfplumber, sqlalchemy, psycopg2) — criado na execução da ideia 001.

## 3. Mapa do projeto

```
Analise_Fatura_Energisa/
├── main.py                      # entry point: lê a pasta de PDFs e salva tudo no banco
├── test.py                      # experimentos ad-hoc (caminhos hardcoded p/ Downloads)
├── FormatoB.py                  # RASCUNHO: protótipo do formato B (código já absorvido em extractors/)
├── itensdafaturaB.py            # RASCUNHO: protótipo do parser de itens (idem)
├── models/                      # domínio (dataclasses) + orquestrador
│   ├── class_fatura.py          # ★ Fatura: detecta formato, extrai tudo, monta os objetos
│   ├── class_cliente.py         # Cliente(nome_cliente, cpf_cnpj)
│   ├── class_UC.py              # UnidadeConsumidora(numero_uc, endereco, cep)
│   ├── class_valores_fatura.py  # ValoresFatura(mes_ref, vencimento, pagar, apresentacao)
│   ├── class_leitura.py         # Leitura(l_anterior, l_atual, dias, l_proxima)
│   ├── class_medidor.py         # Medidor(numero_medidor) + SumarioEletrico(...)
│   ├── class_tributos.py        # Tributo(nome, base_calc, aliquota, valor)
│   └── class_itensdafatura.py   # ItemDaFatura (10 colunas) + ItensTotal (não usado)
├── extractors/                  # extração de PDF
│   ├── class_leitor_de_fatura.py           # ★ PdfReader (formato A)
│   └── class_leitor_de_fatura_formatoB.py  # PdfReaderFormatoB (herda de PdfReader)
├── database/                    # persistência
│   ├── conection.py             # engine + Session + Base
│   ├── models.py                # ORM — 8 tabelas
│   └── persistencia.py         # ★ salvar_fatura() + conversores (para_decimal/para_data/para_mes_ref)
├── web/                         # páginas Flask (construídas nas ideias 001 e 002)
│   ├── app.py                   # servidor: /, /configuracoes, /clientes, /api/upload, /api/historico,
│   │                           # /api/download/<id>, /api/clientes (GET/POST/DELETE),
│   │                           # /api/clientes/documentos
│   ├── servico_upload.py        # regras de upload + histórico EM MEMÓRIA (só visual)
│   ├── templates/upload.html         # a página (campo de upload + tabela de histórico)
│   ├── templates/configuracoes.html  # Configurações: tema claro/escuro (☀️/🌙)
│   ├── templates/clientes.html       # 👥 Gestao de Clientes: busca, filtro por documento,
│   │                                 # criar via modal e excluir (ideia 002)
│   └── static/css/, static/js/       # estilo, tema compartilhado (tema.js) e comportamento;
│                                      static/js/clientes.js = lógica da página de clientes
├── ideias/                      # ideias aprovadas (Etapa 1) + prompts de execução (Etapa 2)
└── visuals/
    ├── pdf_visual.py            # Visual: menu CLI p/ escolher um PDF e ver a fatura em texto
    └── scripts_sql              # DDL PostgreSQL das tabelas
```
★ = arquivos mais importantes

## 4. Fluxo de dados (pipeline)

```
Pasta de PDFs (main.py)
 └─ Fatura(pdf)                          [models/class_fatura.py]
     ├─ PdfReader.formato(pdf)           → "A" (largura ≤ 600pt) ou "B" (> 600pt)
     ├─ PdfReader OU PdfReaderFormatoB    [extractors/]
     │    └─ extrai por coordenadas (_LOC_*, _COLUNAS) + regex → tudo string
     └─ monta: Cliente, UC, Leitura, Tributos[PIS, COFINS, ICMS], Medidor,
               SumariosEletricos[], ValoresFatura, ItensFatura[]
 └─ salvar_fatura(fatura, session)       [database/persistencia.py]
     ├─ upsert Cliente (por cpf_cnpj; CPF mascarado c/ X ou * vira busca LIKE —
     │            se não achar, levanta "Cliente nao encontrado!")
     ├─ upsert UC (por número da UC)
     ├─ upsert Medidor (por número)
     ├─ dedup fatura por (uc_id, mes_ref) → devolve ("DUPLICADO", None) se já existir
     └─ insere fatura + sumários + tributos (nomes fixos PIS/COFINS/ICMS) + leitura + itens
        → devolve ("SUCESSO", id da fatura) — o main.py ignora o retorno; a página web usa
```

Conversores em `persistencia.py`:
- `para_decimal`: `"1.234,56"` → `Decimal("1234.56")` (formato pt-BR)
- `para_data`: `"dd/mm/AAAA"` → `date`
- `para_mes_ref`: `"MAI/2026"` → `date(2026, 5, 1)` (dict `MESES`)

Detalhe: em `class_fatura.py`, linhas incompletas do sumário elétrico são completadas com a
constante da linha anterior (com `logging.warning`) antes de virar `SumarioEletrico`;
itens com a linha "LANÇAMENTOS E SERVIÇOS" são descartados.

## 5. O banco de dados (8 tabelas)

`clientes` —(1:N)→ `unidadeconsumidora` —(1:N)→ `fatura` —(1:N)→ {`leitura`, `tributo`, `item_fatura`, `sumarioeletrico`}
`medidor` —(1:N)→ {`fatura`, `sumarioeletrico`}

- Schema criado via `visuals/scripts_sql` (DDL manual, `generated by default as identity`)
- O ORM (`database/models.py`) mapeia as tabelas já existentes
- `fatura` guarda: valor_total, vencimento, mes_ref, data_apresentacao (nullable), nome_pdf (nullable), uc_id, medidor_id

## 6. Como rodar

1. Banco: criar as tabelas com `visuals/scripts_sql` (uma vez)
2. Colocar os PDFs em `C:\Users\rafae\Downloads\pdfs_fatura`
3. `python main.py` — processa todos os PDFs da pasta e salva no banco

`visuals/pdf_visual.py` (`Visual`) é um menu interativo para inspecionar uma fatura em texto
(o uso está comentado em `main.py`; o loop ativo salva todos os PDFs).

**Páginas web** (`python web/app.py` → http://127.0.0.1:5000):
- `/` — Upload de PDF (arrastar ou clicar) → pipeline `Fatura()`/`salvar_fatura()` → status
  SUCESSO / DUPLICADO (UC + mês de referência já no banco) / FALHA (mensagem na coluna de erro)
- `/clientes` — 👥 Gestao de Clientes (ideia 002): lista clientes do banco (`clientes.nome`,
  `clientes.cpf_cnpj`), campo "Número de documento" (filtro só CPF/CNPJ), campo de busca
  (nome OU CPF/CNPJ), botão "Criar novo cliente" com modal (Nome + CPF/CNPJ), exclusão por
  linha. Endpoints: `GET/POST/DELETE /api/clientes` e `GET /api/clientes/documentos`.
- `/configuracoes` — tema claro/escuro (salvo no `localStorage` do navegador,
  aplicado por `static/js/tema.js`).

**Comportamento comum a todas as páginas**:
- **Duplicidade de fatura é decidida só pelo banco** — estar na pasta NÃO é duplicado
  (regra do dono); a pasta só guarda os arquivos, com sufixo " (2)", " (3)"... quando o
  nome é igual e o conteúdo diferente
- **Histórico de uploads em memória** (decisão do dono): mostra as tentativas da sessão
  atual e zera quando o servidor reinicia — NÃO vai ao banco nem ao models; é só
  visualização
- Botão de download serve o PDF de `pdfs_fatura` com o nome original do upload
- Ações em gradiente laranja + âmbar; ícones SVG outline (line style)

## 7. Convenções do projeto

- Classes de domínio em `models/class_*.py` como `@dataclass`, **valores sempre como string** — conversão de tipo só na persistência
- Extração orientada a **coordenadas fixas** (constantes `_LOC_*` e `_COLUNAS`) — cada formato de fatura tem as suas
- Formato B herda de `PdfReader` (sobrescreve coordenadas e alguns métodos)
- Ícones das páginas em **SVG outline (line style)** — `fill="none" stroke="currentColor"` — nunca emoji como ícone (decisão do dono)
- Mensagens de commit genéricas em pt-BR ("mudanças concluidas" etc.)
- Sem testes automatizados; `test.py` é experimento manual

## 8. Pontos de atenção (NÃO mexer sem discutir com o dono)

- Caminho dos PDFs hardcoded em `main.py` e `test.py`
- Senha do banco hardcoded em `database/conection.py`
- `__pycache__/*.pyc` rastreado no git (deveria estar no `.gitignore`)
- `visuals/scripts_sql` **desatualizado em relação ao ORM**: no DDL faltam `data_apresentacao` e `nome_pdf` em `fatura`, e `mes_ref` é `varchar(50)` lá, mas `Date` no ORM
- `scripts_sql` comenta "-- Banco: fatura", mas a conexão usa o banco padrão `postgres`
- `PdfReader.itens_num()` chama `self.itens_fatura()`, que não existe (o método é `extrair_itens_fatura()`) — nunca chamado
- `FormatoB.py` e `itensdafaturaB.py` são rascunhos no root — código parcialmente duplicado em `extractors/`
- `ItensTotal` (models/class_itensdafatura.py) não é usado em nenhum lugar

## 9. Fluxo de trabalho com o Hermes (combinado com o dono)

1. **Etapa 1 — Discutir**: conversamos sobre a página (o que faz, como fica), avaliamos viabilidade. **Nada é executado.**
2. **Etapa 2 — Salvar**: a ideia aprovada vira arquivo em `ideias/` + um prompt de execução autossuficiente (`ideias/NNN-nome.prompt.md`)
3. **Etapa 3 — Executar**: numa **conversa nova**, o prompt é executado e a página é construída

Regra de ouro: **conversa é descartável, arquivo é permanente.**
Toda conversa nova neste projeto começa lendo este `orientacao.md`.
Não acessar nada fora da pasta deste projeto.
