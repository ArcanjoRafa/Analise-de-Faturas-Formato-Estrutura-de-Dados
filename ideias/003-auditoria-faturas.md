# Ideia 003 — Página Auditoria de Faturas

## Contexto
Sistema Analise_Fatura_Energisa (Flask + HTML/CSS/JS puro). Já existem as páginas de upload (`/`) e Gestão de Clientes (`/clientes`). O ORM está em `database/models.py` com as classes `Cliente` (tabela `clientes`), `UnidadeConsumidora` (tabela `unidadeconsumidora`) e `ValoresFatura` (tabela `fatura`). Relação: clientes → unidadeconsumidora (cliente_id) → fatura (uc_id).

## Objetivo
Criar a página "Auditoria de Faturas" (rota `/auditoria`) com emoji Shield Check ao lado do título, contendo um bloco de filtros (`InvoiceFilters`) seguido de uma tabela de resultados (`Results Table`).

## Elementos da página

### InvoiceFilters (bloco de filtros, acima da tabela)
1. Dropdown "Cliente" — lista todos os nomes de `clientes.nome`
2. Dropdown "Unidade Consumidora" — lista as UCs de `unidadeconsumidora.uc` vinculadas ao cliente selecionado no filtro 1 (cascata, recarrega via endpoint do servidor quando o cliente muda)
3. Date picker "De" — mês de referência inicial (`<input type="month">`, foco só em mês/ano)
4. Date picker "Até" — mês de referência final (`<input type="month">`, foco só em mês/ano)

### Regras de data (foque no mês, não no dia)
- Nenhum dos dois date pickers preenchido → mostra todas as faturas
- Apenas "De" preenchido → faturas com `mes_ref` a partir daquele mês (primeiro dia do mês selecionado em diante)
- Apenas "Até" preenchido → faturas com `mes_ref` até aquele mês (último dia do mês selecionado para trás)
- Ambos preenchidos → faturas com `mes_ref` entre os dois meses (inclusive)

### Results Table (tabela abaixo dos filtros)
Colunas:
- `cliente` — nome do cliente (`clientes.nome`)
- `número uc` — número da unidade consumidora (`unidadeconsumidora.uc`)
- `ref mês/ano` — mês de referência da fatura formatado como mm/yyyy (a partir de `fatura.mes_ref`)
- `valor total` — `fatura.valor_total`
- `vencimento` — `fatura.vencimento`
- `nome pdf` — `fatura.nome_pdf`

Ordenação: por cliente e depois por `mes_ref` (crescente).

Estado vazio: quando os filtros não retornam nenhuma fatura, exibir mensagem "Nenhuma fatura encontrada" na tabela.

### Regras de UI (herdar da página de upload/clientes)
- Mesmas cores, fontes e tamanhos de `web/static/css/upload.css` (variáveis `--fundo`, `--superficie`, `--laranja`, `--ambar`, `--texto`, `--texto-suave`, `--borda`, etc.)
- Tema claro/escuro via `data-tema` e `localStorage` (já existente em `static/js/tema.js`)
- Sidebar com links para Upload, Configurações, Clientes e Auditoria (ícone SVG outline no sidebar; emoji 🛡️✅ apenas no título da página h1)
- Título da página: "🛡️✅ Auditoria de Faturas"
- Sem frameworks front-end, sem build, sem npm, sem React

## Critérios de aceite (resumo)
- [ ] Página acessível em `/auditoria`
- [ ] Título "🛡️✅ Auditoria de Faturas" com emoji Shield Check
- [ ] Sidebar com links Upload, Configurações, Clientes e Auditoria (ativo em `/auditoria`)
- [ ] Dropdown de clientes preenchido do banco
- [ ] Dropdown de UCs recarrega dinamicamente conforme o cliente selecionado (endpoint do servidor)
- [ ] Date pickers "De" e "Até" focados em mês/ano
- [ ] Filtro de data segue as regras: nenhum = todas, só "De" = a partir daquele mês, só "Até" = até aquele mês, ambos = intervalo
- [ ] Tabela com colunas cliente | número uc | ref mês/ano | valor total | vencimento | nome pdf
- [ ] Mensagem de vazio quando não há resultados
- [ ] Visual segue `upload.css` (cores, fonte, tamanhos, tema claro/escuro funciona)
- [ ] Navegar entre as páginas pelo sidebar funciona
- [ ] `main.py` continua rodando sem quebrar (regressão)
- [ ] Nada executado nesta etapa; apenas registro da ideia e do prompt para Etapa 3

## Arquivos a criar ou modificar
```
web/
  app.py                  # adicionar rota /auditoria e endpoints API de auditoria
templates/
  auditoria.html          # NOVO: página Auditoria de Faturas (sidebar + filtros + tabela)
static/
  css/upload.css          # reutilizar; adicionar estilos específicos dos filtros/tabela se necessário
  js/
    tema.js               # já existe — não mexer
    menu.js               # já existe (sidebar) — não mexer
    auditoria.js          # NOVO: filtros, cascata de UCs, date pickers, chamada aos endpoints, renderização da tabela
```

Não é necessário alterar `database/models.py`. Apenas usar as classes existentes nos endpoints.

Nada executado nesta etapa; apenas registro da ideia e do prompt para Etapa 3.
