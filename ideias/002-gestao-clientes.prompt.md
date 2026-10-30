# PROMPT DE EXECUÇÃO — Ideia 002: Página Gestão de Clientes

> ⚠️ **NÃO executado ainda.** Este prompt é para ser usado na **Etapa 3** (conversa nova).
> Não reexecute sem conversar com o dono.

**Como usar (Etapa 3):** abra uma **conversa NOVA** no Hermes e cole exatamente:

> Leia C:\Users\rafae\PycharmProjects\Analise_Fatura_Energisa\orientacao.md e depois execute
> C:\Users\rafae\PycharmProjects\Analise_Fatura_Energisa\ideias\002-gestao-clientes.prompt.md
> do começo ao fim, verificando todos os critérios de aceite com evidências reais.

---

## 0) Contexto obrigatório (leia antes de escrever qualquer código)

- Projeto: `C:\Users\rafae\PycharmProjects\Analise_Fatura_Energisa`
- **Leia `orientacao.md` na raiz antes de tudo.**
- **Limite de acesso:** não acesse NADA fora da pasta do projeto e de `C:\Users\rafae\Downloads\pdfs_fatura` (+ scratch próprio para artefatos de teste).
- **Idioma:** todos os textos (código, comentários, página, mensagens de erro) em **português do Brasil**.
- Stack decidida com o dono: **Flask** no back-end, **HTML/CSS/JS puro** no front. Sem frameworks, sem build, sem npm, sem React.
- Banco: PostgreSQL local (`localhost:5432/postgres`, user `postgres`). Tabela `clientes` já existe com `id`, `nome`, `cpf_cnpj`. ORM em `database/models.py` (classe `Cliente`).

## 1) Objetivo

Construir a página web **"👥 Gestao de Clientes"** (rota `/clientes`) que:
- Lista todos os clientes da tabela `clientes` do banco
- Tem um campo "Número de documento" (filtro distinto, apenas CPF/CNPJ)
- Tem um campo de busca acima da tabela (nome OU CPF/CNPJ)
- Tem um botão "Criar novo cliente" alinhado à direita na mesma linha do campo de busca
- Ao clicar em "Criar novo cliente", abre um modal na mesma página com campos Nome e CPF/CNPJ e botões Criar / Cancelar
- A tabela tem colunas: Nome do Titular | Documento CPF/CNPJ | Ações (somente excluir)
- Excluir remove o cliente do banco e da linha da tabela
- Visual idêntico ao padrão da página de upload (mesmas cores, fontes, tamanhos, tema claro/escuro)

## 2) Estrutura de arquivos a criar ou modificar

```
web/
  __init__.py             # vazio — torna 'web' um pacote (criar se não existir)
  app.py                  # adicionar rota /clientes e endpoints API de clientes
  templates/
    clientes.html         # NOVO: página Gestão de Clientes (sidebar + busca + tabela + modal)
  static/
    css/upload.css        # reutilizar; adicionar estilos específicos do modal se necessário
    js/
      tema.js             # já existe (tema claro/escuro) — não mexer
      menu.js             # já existe (sidebar) — não mexer
      clientes.js         # NOVO: busca, filtro documento, modal, criar, excluir
```

A pasta dos PDFs não entra nesta ideia. Não mexe em `main.py`, `models/`, `extractors/`, `database/conection.py` e `database/persistencia.py`.

## 3) Banco de dados

**Não criar tabela nova.** A tabela `clientes` já existe no banco e no ORM:
```python
class Cliente(Base):
    __tablename__ = "clientes"
    id : Mapped[int] = mapped_column(primary_key=True)
    nome : Mapped[str] = mapped_column(TEXT)
    cpf_cnpj : Mapped[str] = mapped_column(String(50))
```

Não é necessário alterar `database/models.py`. Apenas usar a classe `Cliente` existente nos endpoints.

## 4) Endpoints do Flask (`web/app.py`)

Adicionar a `web/app.py` (manter as rotas existentes intactas):

```
GET  /clientes                    → renderiza templates/clientes.html
GET  /api/clientes                → JSON lista de clientes [{id, nome, cpf_cnpj}]
                                    aceita query params opcionais:
                                      q       → busca em nome ILIKE OU cpf_cnpj ILIKE
                                      documento → filtra apenas por cpf_cnpj ILIKE
POST /api/clientes                → recebe JSON {nome, cpf_cnpj}
                                    valida campos não vazios
                                    verifica se cpf_cnpj já existe → se sim, retorna 409
                                    insere no banco e retorna o cliente criado com 201
DELETE /api/clientes/<int:id>     → exclui o cliente do banco; retorna 204 ou 404 se não existir
```

No topo de `app.py`, manter o bootstrap de path:
```python
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
```

Importar `Cliente` de `database.models` e a `Session`/`engine` de `database.conection`.

Rodar: `app.run(host="127.0.0.1", port=5000, debug=True)`.

## 5) Front-end (`clientes.html` + `clientes.js` + CSS)

### `templates/clientes.html`
- Estrutura igual a `upload.html`: `<aside class="sidebar">` + `<main class="container">`
- Sidebar com links: Upload (`/`), Configurações (`/configuracoes`), Clientes (`/clientes`, ativo). Ícones SVG outline (igual ao existente).
- `<h1><svg ...>👥</svg> Gestao de Clientes</h1>` — emoji 👥 ao lado do título (somente no h1, não no sidebar).
- Acima da tabela, uma linha com:
  - Campo "Número de documento" (input texto, placeholder "CPF/CNPJ")
  - Campo de busca (input texto, placeholder "Buscar por nome ou CPF/CNPJ")
  - Botão "Criar novo cliente" (gradiente laranja/âmbar, classe `.botao.primario`) alinhado à direita
- Tabela:
  - `<thead>`: Nome do Titular | Documento CPF/CNPJ | Ações
  - `<tbody>`: preenchido via JS com os clientes do banco
  - Coluna Ações: botão com ícone de lixeira (excluir) para cada linha
- Modal (hidden por padrão):
  - Overlay + caixa centralizada
  - Título: "Novo cliente"
  - Campo Nome (input)
  - Campo CPF/CNPJ (input)
  - Rodapé: botão Cancelar (secundário) + botão Criar (primário laranja/âmbar)
- Toast/mensagem de resultado (sucesso/erro) abaixo do h1 ou fixo.

### `static/js/clientes.js`
- `carregarClientes(q?, documento?)` → `GET /api/clientes` e renderiza a tabela
- Busca por nome ou documento: chama o endpoint com `q`
- Filtro "Número de documento": chama o endpoint com `documento`
- Abrir modal ao clicar em "Criar novo cliente"
- Enviar novo cliente: `POST /api/clientes` com JSON; ao sucesso, recarrega lista e fecha modal
- Excluir: `DELETE /api/clientes/<id>` com confirmação (`confirm()`); ao sucesso, remove a linha
- Formatar dados para exibição; tratar erros com mensagens em pt-BR

### CSS
- Reutilizar `web/static/css/upload.css` (variáveis, `.botao`, `.botao.primario`, tabela, sidebar, tema).
- Se necessário, adicionar estilos específicos do modal no mesmo `upload.css` ou criar `web/static/css/clientes.css` importado em `clientes.html`.

## 6) Dependências

- Flask já instalado no `.venv` (da ideia 001). Verificar que `flask` está em `requirements.txt`.
- Nenhuma dependência nova.

## 7) Verificação obrigatória (execute de verdade — resultado inventado não vale)

Teste pelo navegador (use a ferramenta de browser):

1. `python web/app.py` sobe sem erro; `http://127.0.0.1:5000/clientes` abre a página "👥 Gestao de Clientes".
2. A tabela exibe os clientes já cadastrados no banco (colunas Nome do Titular e Documento CPF/CNPJ).
3. O campo "Número de documento" filtra apenas por CPF/CNPJ.
4. O campo de busca filtra por nome OU CPF/CNPJ.
5. Clicar em "Criar novo cliente" abre o modal; preencher Nome e CPF/CNPJ e clicar em Criar → cliente aparece na tabela e no banco (`SELECT * FROM clientes`).
6. Tentar criar cliente com CPF/CNPJ já existente → erro exibido, não duplica.
7. Clicar em Cancelar no modal → fecha sem criar.
8. Clicar no ícone de excluir → confirmação → cliente some da tabela e do banco.
9. Visual segue o padrão de `upload.css` (mesmas cores, fonte, tamanhos, tema claro/escuro funciona).
10. Navegar entre Upload, Configurações e Clientes pelo sidebar funciona.
11. `python main.py` continua rodando sem quebrar (regressão).
12. Não remover ou alterar dados do usuário no banco. Não rode `git commit` — deixe as mudanças no working tree.

## 8) Critérios de aceite (verifique um a um e reporte com evidência real)

- [ ] `python web/app.py` sobe e a página abre em `http://127.0.0.1:5000/clientes`
- [ ] Título "👥 Gestao de Clientes" com emoji
- [ ] Sidebar com links Upload, Configurações e Clientes
- [ ] Campo "Número de documento" distinto do campo de busca
- [ ] Tabela com colunas Nome do Titular | Documento CPF/CNPJ | Ações (excluir)
- [ ] Botão "Criar novo cliente" alinhado à direita na mesma linha dos campos
- [ ] Modal com Nome, CPF/CNPJ, botões Criar e Cancelar
- [ ] Criar cliente grava no banco e aparece na tabela
- [ ] CPF/CNPJ duplicado é rejeitado com mensagem
- [ ] Excluir remove do banco e da tabela
- [ ] Busca por nome ou CPF/CNPJ funciona no back-end
- [ ] Filtro por número de documento funciona no back-end
- [ ] Visual segue `upload.css` (cores, fonte, tamanhos, tema claro/escuro)
- [ ] `main.py` continua rodando sem quebrar
- [ ] Artefatos de teste removidos; nada do usuário foi apagado ou alterado
- [ ] Relatório final ao dono: o que foi feito, evidência de cada teste, pendências honestas