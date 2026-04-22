# 🧠 Memory — Gerenciador de Favoritos

> Arquivo de memória técnica do projeto. Registra decisões de arquitetura, bugs corrigidos e padrões estabelecidos para consulta futura pela IA ou pelo desenvolvedor.

---

## 📌 Visão Geral

**Projeto:** `chad-favorites`
**Versão atual:** v1.4.3
**Linguagem:** Python 3
**UI:** Tkinter + `sv_ttk` (Sun Valley Theme)
**Parser:** BeautifulSoup 4
**Plataforma:** Windows (exclusivo — usa `winreg`)
**Executável:** Gerado com PyInstaller via `favoritos.spec`
**Backlog:** ver `next_steps.md`

---

## 🗂️ Arquivo Principal

| Arquivo | Função |
|---|---|
| `src/favoritos.py` | Toda a lógica: UI, parsing, pesquisa, abertura de links |
| `chad-favorites.spec` | Configuração do PyInstaller (icon, datas, hiddenimports) |
| `assets/icon.ico` | Ícone da aplicação (6 tamanhos: 16→56px) — gerado com Pillow |
| `src/recent_files.json` | Gerado em runtime — persiste os últimos 5 arquivos carregados |
| `next_steps.md` | Backlog de melhorias priorizadas |
| `memory.md` | Este arquivo — memória técnica do projeto |

---

## 🐛 Bugs Corrigidos

### [2026-04-22] Parser HTML não exibia favoritos

**Sintoma:** Ao carregar o arquivo HTML, a árvore ficava vazia — nenhuma pasta ou link aparecia.

**Causa Raiz:** O método `parse_bookmarks` usava `dl_element.find_all('dt', recursive=False)`, mas o `html.parser` do Python, ao processar HTML de favoritos (que omite tags de fechamento como `</DT>` e `</DL>`), reestrutura o DOM de forma diferente do esperado. Os `<dt>` ficavam aninhados dentro de `<p>` gerados automaticamente, quebrando a busca com `recursive=False`.

**Solução Aplicada:**

```python
# ANTES (quebrado):
for dt in dl_element.find_all('dt', recursive=False):
    h3 = dt.find('h3', recursive=False)
    ...

# DEPOIS (corrigido):
dts = dl_element.find_all('dt')
direct_dts = [dt for dt in dts if dt.find_parent('dl') == dl_element]

for dt in direct_dts:
    h3 = dt.find('h3', recursive=False) or dt.find('h3')
    ...
```

**Padrão estabelecido:** Sempre usar `find_parent('dl') == dl_element` para filtrar `<dt>` filhos diretos de um `<dl>` ao parsear favoritos de navegadores.

---

## 🚫 Sistema Removido: DRM / Credencial

**Data:** 2026-04-22
**Motivo:** A pedido do desenvolvedor — o sistema de licença impedia o uso normal da aplicação em qualquer máquina diferente da original.

**O que foi removido:**
- Constante `MASTER_SIGNATURE` (hash SHA-256 hardcoded)
- Função `verify_identity()` (validava MAC + hostname + dados pessoais)
- Atributo `self.is_pro_mode` na classe `BookmarkManager`
- Lógica condicional de título e cor do header baseada em licença
- Arquivos: `src/forjar_credencial.py`, `prime_sigil_credential.txt`

**Estado atual:** Aplicação totalmente aberta, sem restrições. Header verde fixo com texto "Pronto para uso".

---

## 🏛️ Decisões de Arquitetura

### Tema automático (Claro/Escuro)
- Detectado via `winreg` (`AppsUseLightTheme`)
- Fallback: `dark` em caso de exceção
- Tema aplicado com `sv_ttk.set_theme()`

### Abertura de links — com validação de segurança (v1.1)
- `webbrowser.open(url)` — usa o navegador padrão do sistema
- **Validação obrigatória:** `urlparse(url).scheme` deve ser `http` ou `https`
- Links com esquemas `file:///`, `javascript:`, `ms-appinstaller:` etc. exibem `messagebox.showwarning` e são bloqueados
- Duplo clique em pasta: toggle expand/collapse
- Duplo clique em link: abre no navegador (se URL válida)

### Pesquisa
- Pesquisa flat sobre `self.all_bookmarks` (lista plana de todos os links)
- Pesquisa simultânea em `title` e `url`
- Limpa a árvore e monta uma sub-árvore de resultados em `🔍 Resultados da Pesquisa`
- Ao apagar o campo, reconstrói a árvore completa via `build_tree()`
- Rodapé exibe contador de resultados durante a pesquisa

### Histórico de arquivos recentes (v1.1)
- Persistido em `src/recent_files.json` via `json.dump/load`
- Máximo de 5 entradas (`MAX_RECENT = 5`)
- Arquivos inexistentes são filtrados no carregamento
- Menu `🕐 Recentes ▾` (Menubutton + tk.Menu) na barra de controles
- Opção "🗑 Limpar histórico" no final do menu
- Título da janela atualiza para `Gerenciador de Favoritos — nome_do_arquivo.html`

### Ordenação por coluna (v1.1)
- Estado mantido em `self._sort_state = {"col": None, "reverse": False}`
- Clique no header alterna entre `▲` (A→Z) e `▼` (Z→A)
- Clique em coluna diferente reinicia a direção
- Ordena apenas os itens raiz (`tree.get_children("")`) — pastas e nós de pesquisa
- Chave de ordenação: `text.lower()` para Nome, `values[0].lower()` para URL
- Indicador visual nos headers atualizado dinamicamente

---

## 📦 Empacotamento (PyInstaller)

- **Comando obrigatório:** `pyinstaller --clean favoritos.spec`
  - O `--clean` é essencial: sem ele, o PyInstaller reutiliza cache do build anterior e o `.exe` não reflete as mudanças no código
- Saída: `dist/favoritos.exe`
- Modo: `console=False` (sem janela de terminal)
- UPX ativado para compressão
- `sv_ttk` e `beautifulsoup4` devem estar instalados no ambiente usado pelo PyInstaller

> ⚠️ **Gotcha:** Exit code 1 no PowerShell após o build **não indica falha do PyInstaller** — é causado por erros no perfil do PS (`Microsoft.PowerShell_profile.ps1`). Confirmar sucesso pela mensagem `Build complete!` no output.

---

### Favicons assíncronos (v1.2)
- Buscados via `https://www.google.com/s2/favicons?sz=16&domain={domain}`
- Download em `threading.Thread(daemon=True)` para não bloquear a UI
- Atualizações na Treeview feitas via `root.after(0, ...)` (thread-safe)
- Cache em `self._favicon_cache: dict[domain -> ImageTk.PhotoImage]`
- Ícone padrão cinza 16x16 exibido enquanto favicon carrega
- **Atenção PyInstaller:** requer `hiddenimports=['PIL', 'PIL.Image', 'PIL.ImageTk', 'requests', 'urllib3']` no `.spec`

### Exportar favoritos filtrados (v1.2)
- Botão `💾 Exportar filtro` habilitado apenas quando há pesquisa ativa com resultados
- Abre `filedialog.asksaveasfilename` com nome pré-preenchido `favoritos_{query}.html`
- Gera HTML formato padrão Netscape Bookmark File 1 (compatível com qualquer navegador)
- Escapa `<` e `>` nos títulos dos links antes de escrever

### Ícone da aplicação (v1.3)
- Gerado com `Pillow` a partir de PNG, 6 tamanhos: `(16,16)` a `(256,256)`
- Salvo em `assets/icon.ico`
- Embutido no `.exe` via `icon='assets/icon.ico'` no spec
- Copiado junto ao bundle via `datas=[('assets/icon.ico', 'assets')]`
- Aplicado à janela com `root.iconbitmap(ICON_PATH)` no `__init__`
- Resolução de path: `sys._MEIPASS` quando rodando como `.exe`, fallback para diretório relativo ao script

### Detecção de tema cross-platform (v1.3)
- **Prioridade 1:** `darkdetect.theme()` — funciona em Windows, macOS e Linux
- **Prioridade 2:** `winreg` — fallback para Windows sem `darkdetect`
- **Prioridade 3:** retorna `"dark"` como padrão seguro
- Import de `darkdetect` com `try/except` — nunca quebra se não instalado
- `winreg` movido para import dinâmico dentro do fallback (não falha em macOS/Linux)

---

## ✅ Implementadas (completo)
- [x] Validação de URL antes de abrir (`http`/`https` only)
- [x] Histórico de arquivos recentes (persistido em JSON)
- [x] Ordenação por coluna (Nome / URL)
- [x] Rodapé com contador detalhado (pastas + links)
- [x] Título da janela com nome do arquivo carregado
- [x] Favicons assíncronos via Google S2 + Pillow
- [x] Exportar favoritos filtrados como HTML Netscape
- [x] Ícone `.ico` no executável e na janela
- [x] Detecção de tema cross-platform via `darkdetect`
- [x] Remoção da barra de status verde ("Pronto para uso") do topo
- [x] Carregamento automático do último arquivo carregado na inicialização do app

---

## 🚀 Estratégia para GitHub (v1.4.3+)
Para manter a privacidade e o profissionalismo ao subir para o GitHub:
- **`memory.md` e `next_steps.md`**: Adicionados ao `.gitignore`. Eles permanecem na máquina local como histórico de desenvolvimento, mas não são públicos.
- **`recent_files.json` e `favicons/`**: Adicionados ao `.gitignore`. Contêm dados privados do usuário e cache local.
- **`requirements.txt` e `LICENSE`**: Criados para seguir os padrões da comunidade.
- **`README.md`**: Totalmente reformulado para destacar as funcionalidades premium e guiar novos usuários.

