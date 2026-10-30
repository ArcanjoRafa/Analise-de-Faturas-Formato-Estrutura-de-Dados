# PROMPT DE EXECUÇÃO — Ideia 003: Página Auditoria de Faturas

> ⚠️ **NÃO executado ainda.** Este prompt é para ser usado na **Etapa 3** (conversa nova).
> Não reexecute sem conversar com o dono.

**Como usar (Etapa 3):** abra uma **conversa NOVA** no Hermes e cole exatamente:

> Leia C:\Users\rafae\PycharmProjects\Analise_Fatura_Energisa\orientacao.md e depois execute
> C:\Users\rafae\PycharmProjects\Analise_Fatura_Energisa\ideias\003-auditoria-faturas.prompt.md
> do começo ao fim, verificando todos os critérios de aceite com evidências reais.

---

## 0) Contexto obrigatório (leia antes de escrever qualquer código)

- Projeto: `C:\Users\rafae\PycharmProjects\Analise_Fatura_Energisa`
- **Leia `orientacao.md` na raiz antes de tudo.**
- **Limite de acesso:** não acesse NADA fora da pasta do projeto e de `C:\Users\rafae\Downloads\pdfs_fatura` (+ scratch próprio para artefatos de teste).
- **Idioma:** todos os textos (código, comentários, página, mensagens de erro) em **português do Brasil**.
- Stack decidida com o dono: **Flask** no back-end, **HTML/CSS/JS puro** no front. Sem frameworks, sem build, sem npm, sem React.
- Banco: PostgreSQL local (`localhost:5432/postgres`, user `postgres`). ORM em `database/models.py` (classes `Cliente`, `UnidadeConsumidora`, `ValoresFatura`).
- Executar com o venv do projeto: `.venv\Scripts\python.exe`.

---

## 1) Objetivo

Construir a página web **"🛡️✅ Auditoria de Faturas"** (rota `/auditoria`) que:

- Apresenta um bloco de filtros (`InvoiceFilters`) com:
  1. Dropdown de clientes (todos os nomes de `clientes.nome`)
  2. Dropdown de unidades consumidoras (UCs de `unidadeconsumidora.uc` vinculadas ao cliente selecionado — cascata via endpoint)
  3. Date picker "De" (mês de referência inicial, `<input type="month">`)
  4. Date picker "Até" (mês de referência final, `<input type="month">`)
- Abaixo, apresenta uma tabela de resultados (`Results Table`) com colunas:
  - `cliente` | `número uc` | `ref mês/ano` | `valor total` | `vencimento` | `nome pdf`
- Regras de data (foque no mês, não no dia):
  - Nenhum date picker preenchido → mostra todas as faturas
  - Apenas "De" preenchido → `mes_ref` a partir daquele mês (primeiro dia do mês selecionado em diante)
  - Apenas "Até" preenchido → `mes_ref` até aquele mês (último dia do mês selecionado para trás)
  - Ambos preenchidos → `mes_ref` entre os dois meses (inclusive)
- Quando não há resultados, exibir mensagem "Nenhuma fatura encontrada" na tabela.
- Ordenação: por cliente e depois por `mes_ref` (crescente).

---

## 2) Estrutura de arquivos a criar ou modificar

```
web/
  app.py                  # adicionar rota /auditoria e endpoints API de auditoria
templates/
  auditoria.html          # NOVO: página Auditoria de Faturas (sidebar + filtros + tabela)
static/
  css/upload.css          # reutilizar; adicionar estilos específicos se necessário
  js/
    auditoria.js          # NOVO: lógica dos filtros, cascata, date pickers, chamada aos endpoints, renderização
```

A pasta dos PDFs não entra nesta ideia. Não mexe em `main.py`, `models/`, `extractors/`, `database/conection.py` e `database/persistencia.py`.

---

## 3) Banco de dados

**Não criar tabela nova.** Usar as classes ORM existentes:

```python
class Cliente(Base):
    __tablename__ = "clientes"
    id : Mapped[int] = mapped_column(primary_key=True)
    nome : Mapped[str] = mapped_column(TEXT)
    cpf_cnpj : Mapped[str] = mapped_column(String(50))

class UnidadeConsumidora(Base):
    __tablename__ = "unidadeconsumidora"
    id : Mapped[int] = mapped_column(primary_key=True)
    uc : Mapped[str] = mapped_column(String(30))
    cliente_id : Mapped[int] = mapped_column(ForeignKey("clientes.id"))

class ValoresFatura(Base):
    __tablename__ = "fatura"
    id : Mapped[int] = mapped_column(primary_key=True)
    valor_total : Mapped[Decimal] = mapped_column(Numeric(10,2))
    vencimento : Mapped[date] = mapped_column(Date)
    mes_ref : Mapped[date] = mapped_column(Date)
    data_apresentacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    nome_pdf: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    uc_id : Mapped[int] = mapped_column(ForeignKey("unidadeconsumidora.id"))
    medidor_id : Mapped[int] = mapped_column(ForeignKey("medidor.id"))
```

Não é necessário alterar `database/models.py`. Apenas usar as classes existentes nos endpoints.

---

## 4) Endpoints do Flask (`web/app.py`)

Adicionar a `web/app.py` (manter as rotas existentes intactas):

```
GET  /auditoria                    → renderiza templates/auditoria.html
GET  /api/clientes                 → JSON [{id, nome}] de todos os clientes (para o dropdown 1)
GET  /api/ucs?cliente_id=<id>      → JSON [{id, uc}] de UCs do cliente selecionado (dropdown 2, cascata)
GET  /api/faturas                  → JSON lista de faturas filtradas
                                     query params opcionais:
                                       cliente_id → filtra por cliente
                                       uc_id      → filtra por UC
                                       de         → YYYY-MM (mes_ref >= primeiro dia do mês)
                                       ate        → YYYY-MM (mes_ref <= último dia do mês)
                                     resultado: [{cliente, numero_uc, mes_ref (YYYY-MM), valor_total, vencimento (YYYY-MM-DD), nome_pdf}]
```

No topo de `app.py`, manter o bootstrap de path:

```python
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
```

Importar `Cliente`, `UnidadeConsumidora`, `ValoresFatura` de `database.models` e a `Session` de `database.conection`.

Rodar: `app.run(host="127.0.0.1", port=5000, debug=True)`.

---

## 5) Front-end (`auditoria.html` + `auditoria.js` + CSS)

### `templates/auditoria.html`
- Estrutura igual a `upload.html`/`clientes.html`: `<aside class="sidebar">` + `<main class="container">`
- Sidebar com links: Upload (`/`), Configurações (`/configuracoes`), Clientes (`/clientes`), Auditoria (`/auditoria`, ativo). Ícones SVG outline.
- `<h1><svg ...>🛡️✅</svg> Auditoria de Faturas</h1>` — emoji Shield Check ao lado do título (somente no h1, não no sidebar).
- Bloco `InvoiceFilters` acima da tabela:
  - Dropdown "Cliente"
  - Dropdown "Unidade Consumidora" (desativado até um cliente ser selecionado)
  - Date picker "De" (`<input type="month">`)
  - Date picker "Até" (`<input type="month">`)
- Tabela `Results Table`:
  - `<thead>`: cliente | número uc | ref mês/ano | valor total | vencimento | nome pdf
  - `<tbody>`: preenchido via JS com os dados de `/api/faturas`
  - Quando vazio: linha com mensagem "Nenhuma fatura encontrada"
- Toast/mensagem de resultado (sucesso/erro) abaixo do h1.

### `static/js/auditoria.js`
- `carregarClientes()` → `GET /api/clientes`, preenche dropdown 1
- Ao mudar dropdown 1 → `GET /api/ucs?cliente_id=<id>`, preenche dropdown 2
- `carregarFaturas(cliente_id?, uc_id?, de?, ate?)` → `GET /api/faturas` e renderiza tabela
- Formatar `mes_ref` como mm/yyyy para exibição
- Formatar `valor_total` no formato pt-BR (ex.: 1.234,56)
- Formatar `vencimento` como dd/mm/AAAA
- Tratar erros com mensagens em pt-BR

### CSS
- Reutilizar `web/static/css/upload.css` (variáveis, `.botao`, tabela, sidebar, tema).
- Se necessário, adicionar estilos específicos dos filtros no mesmo `upload.css` ou criar `web/static/css/auditoria.css` importado em `auditoria.html`.

---

## 6) Dependências

- Flask já instalado no `.venv` (da ideia 001). Verificar que `flask` está em `requirements.txt`.
- Nenhuma dependência nova.

---

## 7) Verificação obrigatória (execute de verdade — resultado inventado não vale)

Teste pelo navegador (use a ferramenta de browser):

1. `.venv\Scripts\python.exe web/app.py` sobe sem erro; `http://127.0.0.1:5000/auditoria` abre a página "🛡️✅ Auditoria de Faturas".
2. O dropdown de clientes é preenchido com nomes do banco.
3. Selecionar um cliente recarrega o dropdown de UCs só com as UCs daquele cliente.
4. Nenhum filtro de data selecionado → tabela mostra todas as faturas.
5. Só "De" selecionado → mostra faturas a partir daquele mês.
6. Só "Até" selecionado → mostra faturas até aquele mês.
7. Ambos selecionados → mostra faturas no intervalo.
8. Tabela exibe colunas: cliente, número uc, ref mês/ano (mm/yyyy), valor total, vencimento, nome pdf.
9. Quando não há resultados, aparece a mensagem "Nenhuma fatura encontrada".
10. Visual segue `upload.css` (mesmas cores, fonte, tamanhos, tema claro/escuro funciona).
11. Navegar entre Upload, Configurações, Clientes e Auditoria pelo sidebar funciona.
12. `.venv\Scripts\python.exe main.py` continua rodando sem quebrar (regressão).
13. Não remover ou alterar dados do usuário no banco. Não rode `git commit` — deixe as mudanças no working tree.

---

## 8) Critérios de aceite (verifique um a um e reporte com evidência real)

- [ ] `python web/app.py` sobe e a página abre em `http://127.0.0.1:5000/auditoria`
- [ ] Título "🛡️✅ Auditoria de Faturas" com emoji Shield Check
- [ ] Sidebar com links Upload, Configurações, Clientes e Auditoria
- [ ] Dropdown de clientes preenchido do banco
- [ ] Dropdown de UCs recarrega dinamicamente conforme o cliente selecionado (endpoint do servidor)
- [ ] Date pickers "De" e "Até" focados em mês/ano (`<input type="month">`)
- [ ] Filtro de data segue as regras: nenhum = todas, só "De" = a partir daquele mês, só "Até" = até aquele mês, ambos = intervalo
- [ ] Tabela com colunas cliente | número uc | ref mês/ano | valor total | vencimento | nome pdf
- [ ] Mensagem de vazio "Nenhuma fatura encontrada" quando não há resultados
- [ ] Visual segue `upload.css` (cores, fonte, tamanhos, tema claro/escuro)
- [ ] `main.py` continua rodando sem quebrar
- [ ] Artefatos de teste removidos; nada do usuário foi apagado ou alterado
- [ ] Relatório final ao dono: o que foi feito, evidência de cada teste, pendências honestas
