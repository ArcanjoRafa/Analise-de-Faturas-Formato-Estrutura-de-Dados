# Ideia 002 — Página Gestão de Clientes

## Contexto
Sistema Analise_Fatura_Energisa (Flask + HTML/CSS/JS puro). Já existe a página de upload de faturas em `web/`. A tabela `clientes` já existe no PostgreSQL com colunas `id`, `nome` (TEXT) e `cpf_cnpj` (String(50)). O ORM está em `database/models.py` (classe `Cliente`).

## Objetivo
Criar a página "👥 Gestao de Clientes" que lista todos os clientes do banco, permite buscar por nome ou CPF/CNPJ, filtrar por número de documento, criar novos clientes via modal na mesma página e excluir clientes da lista.

## Regras de UI (herdar da página de upload)
- Mesmas cores, fontes e tamanhos de `web/static/css/upload.css` (variáveis `--fundo`, `--superficie`, `--laranja`, `--ambar`, `--texto`, `--texto-suave`, `--borda`, etc.)
- Tema claro/escuro via `data-tema` e `localStorage` (já existente em `static/js/tema.js`)
- Sidebar com links para Upload, Configurações e Clientes (ícone SVG outline no sidebar; emoji 👥 apenas no título da página h1)
- Título da página: "👥 Gestao de Clientes"

## Elementos da página
1. Campo "Número de documento" — filtro distinto, apenas CPF/CNPJ
2. Campo de busca acima da tabela — busca por Nome do Titular OU Documento CPF/CNPJ
3. Botão "Criar novo cliente" — alinhado à direita, na mesma linha do campo de busca
4. Tabela principal com colunas: Nome do Titular | Documento CPF/CNPJ | Ações (somente excluir)
5. Modal ao clicar em "Criar novo cliente": campos Nome e CPF/CNPJ, botões Criar e Cancelar

## Regras de negócio
- Busca no back-end (Flask + SQLAlchemy `ilike` sobre `nome` e `cpf_cnpj`)
- Criar cliente valida que nome e CPF/CNPJ não estejam vazios
- Evitar duplicidade de CPF/CNPJ no back-end antes de inserir
- Exclusão remove o cliente do banco e da tabela na tela
- Sem frameworks front-end, sem build, sem npm, sem React

## Critérios de aceite (resumo)
- Página acessível em `/clientes`
- Tabela lista clientes do banco (`clientes.nome`, `clientes.cpf_cnpj`)
- Campo "Número de documento" filtra só por CPF/CNPJ
- Campo de busca filtra por nome OU CPF/CNPJ
- Modal cria cliente e ele aparece na tabela e no banco
- Botão excluir remove o cliente do banco e da linha da tabela
- Visual segue o padrão de `upload.css` (cores, fonte, tamanhos, tema claro/escuro)
- Nada executado nesta etapa; apenas registro da ideia e do prompt para Etapa 3