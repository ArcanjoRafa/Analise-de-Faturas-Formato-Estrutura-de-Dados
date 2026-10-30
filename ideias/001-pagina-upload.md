# Ideia 001 — Página de Upload de Faturas

**Status:** ✅ Aprovada na Etapa 1 (25/10/2026) — EXECUTADA na Etapa 3 (27/10) — CORRIGIDA pós-execução: histórico em memória, sem tabela no banco
**Prompt de execução:** `001-pagina-upload.prompt.md` (neste mesmo diretório)
**Executor da Etapa 3:** conversa NOVA, lendo `orientacao.md` + o prompt.

## Objetivo

Primeira página web do sistema: upload interativo de PDFs de faturas da Energisa, com
histórico completo de tentativas e botão de download de qualquer registro.

## Layout

```
┌──────────────────────────────┐
│  Arraste o PDF aqui          │  ← campo: arrastar OU clicar (abre o explorador)
│  ou clique para procurar      │
└──────────────────────────────┘
   nome-do-arquivo.pdf
                      [Realizar Upload]  [Cancelar]
──────────────────────────────────────────────────
  HISTÓRICO DE UPLOADS
  Nome do PDF │ Data do upload │ Status │ Erro │ Ação(⬇)
```

## Comportamento aprovado

### Campo de upload
- Arrastar o PDF **ou** clicar no campo (abre o explorador de arquivos)
- Aceita **só .pdf**, um arquivo por vez
- Nome do arquivo aparece logo abaixo do campo
- Botões à direita, um pouco abaixo do nome: **Realizar Upload** e **Cancelar**
- Botões desativados enquanto não houver arquivo no campo
- **Cancelar** esvazia o campo e desativa os botões (não fala com o servidor)
- Durante o processamento: botões travados + indicador "Processando..."

### Histórico (abaixo do campo)
- Toda tentativa de upload vira uma linha, com as colunas: **nome do PDF**,
  **data/hora do upload** (dd/mm/aaaa hh:mm), **status** (SUCESSO / DUPLICADO / FALHA),
  **erro** (preenchido só nas falhas) e **ação** (botão com ícone de download)
- Mais recente no topo; carrega ao abrir a página e atualiza após cada upload
- Download disponível em **todas** as linhas (inclusive falhas e duplicadas)

## Fluxo do upload (duplicado = só o banco — regra corrigida pelo dono)

1. Arquivo chega ao servidor (Flask)
2. **Alocação na pasta** (questão de arquivo, não de status):
   - Nome não existe em `pdfs_fatura` → salva com o nome original
   - Nome existe + conteúdo idêntico (hash SHA-256) → não salva de novo, aproveita o
     arquivo que já está lá
   - Nome existe + conteúdo diferente → salva com **sufixo automático**:
     `nome (2).pdf`, `nome (3).pdf`... (nunca sobrescreve o original)
3. Todo PDF enviado fica alocado em `pdfs_fatura` — inclusive os de FALHA/DUPLICADO
4. Pipeline do projeto — roda **SEMPRE**: `Fatura()` → `salvar_fatura()`
5. **Único critério de duplicado:** os dados extraídos do arquivo (UC + mês de
   referência) já estão no banco → **DUPLICADO**
6. Gravou tudo → **SUCESSO**; qualquer erro → **FALHA** com a mensagem na coluna de erro
7. Registra a linha no histórico com o resultado

> **Regra de ouro:** estar na pasta NÃO é duplicado. O status vem do banco, sempre.

## Decisões tomadas na Etapa 1 (clarify com o dono)

1. **Duplicado de negócio** = mesma UC + mesmo mês de referência (regra que o
   `salvar_fatura` já aplica hoje)
2. **PDFs guardados em pasta de arquivos** (não BLOB) — e a pasta é a **já existente**
   `C:\Users\rafae\Downloads\pdfs_fatura`, fonte oficial dos PDFs do sistema
3. **Servidor web em Flask**; front-end em HTML/CSS/JS puro, sem ferramentas de build
4. **Mesmo nome + conteúdo diferente** → sufixo automático para não sobrescrever (aprovado)
5. Sistema local (localhost), sem login

## Decisões técnicas fechadas na Etapa 2 (para viabilizar a execução)

- ~~Nova tabela `upload_historico`~~ → **REVOGADO pelo dono após a execução**: o
  histórico NÃO vai ao banco nem ao models — vive **em memória** no servidor, como
  visualização da sessão atual (ver "Correção pós-execução")
- **Única modificação em código existente:** `salvar_fatura` passa a **retornar**
  `("SUCESSO", id_da_fatura)` ou `("DUPLICADO", None)` — retrocompatível (o `main.py`
  ignora o retorno). Sem isso a página não consegue distinguir sucesso de duplicado.
- **Estrutura nova em `web/`:** `app.py` (Flask), `servico_upload.py` (regras),
  `templates/upload.html`, `static/css`, `static/js`
- **`requirements.txt`** criado na raiz (hoje as dependências só existem no `.venv`)

## Correção do dono sobre duplicidade (revoga a regra anterior "da pasta")

> "Não posso dar como duplicado simplesmente porque o arquivo está na pasta, mas sim
> pelo fato de os dados extraídos do arquivo estarem contidos no banco."

- **Estar na pasta NÃO marca duplicado.** O único critério é o banco: UC + mês de
  referência (o que o `salvar_fatura` já verifica hoje).
- PDF que está na pasta mas cuja fatura **não** está no banco → upload processa e
  grava → **SUCESSO**
- O dono pode resetar/limpar o banco — a página continua correta, porque o status
  depende só do conteúdo do banco naquele momento
- A pasta continua sendo o estoque de arquivos (todo PDF enviado fica lá, com sufixo
  na colisão de nome) — só não decide mais status
- Custo aceito: toda checagem de duplicidade exige extração (o pipeline roda sempre)

## Correção pós-execução (27/10) — histórico sem banco

> "Adicionar tabela no banco e tabela no models não é pra fazer isso. O histórico
> da página é mais para visualizar." (dono)

- Removidos do código: classe `UploadHistorico` (`database/models.py`), o DDL da
  tabela (`visuals/scripts_sql`) e o uso no serviço da página
- O histórico vive **em memória** em `web/servico_upload.py`: mostra as tentativas
  da sessão atual e zera quando o servidor reinicia — não é registro, é visualização
- Os registros de verdade continuam sendo: **fatura no banco** + **PDF na pasta**
- A tabela física `upload_historico` foi derrubada manualmente pelo dono (27/10) — caso encerrado
- Upload, status (SUCESSO/DUPLICADO/FALHA), erro e download seguem funcionando igual

## O que NÃO muda no projeto

- `models/` e `extractors/` — intocados
- `database/` — só ganha o ORM da tabela nova + o retorno de `salvar_fatura`
- `main.py` — continua funcionando igual (processa a pasta em lote; convive com a página)
