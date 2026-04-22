# 📚 Gerenciador de Favoritos

Aplicação desktop para Windows que importa e navega arquivos HTML de favoritos exportados de navegadores (Chrome, Firefox, Edge). Permite visualizar a estrutura hierárquica de pastas e links, e pesquisar por título ou URL em tempo real.

---

## ✨ Funcionalidades

- 📁 **Importação de HTML** — Carrega arquivos `.html` exportados pelo navegador
- 🌳 **Árvore hierárquica** — Exibe pastas e links na estrutura original
- 🔍 **Pesquisa em tempo real** — Filtra favoritos por título ou URL enquanto digita
- 🖱️ **Duplo clique para abrir** — Abre o link no navegador padrão do sistema
- 🌙 **Tema automático** — Detecta e aplica o tema claro ou escuro do Windows
- 💚 **Interface moderna** — Usa `sv_ttk` para visual nativo e fluente

---

## 🛠️ Dependências

| Biblioteca    | Uso                                         |
|---------------|---------------------------------------------|
| `tkinter`     | Interface gráfica (incluso no Python)       |
| `sv_ttk`      | Tema moderno Sun Valley para ttk            |
| `beautifulsoup4` | Parsing do HTML de favoritos            |

### Instalação das dependências

```bash
pip install sv_ttk beautifulsoup4
```

---

## 🚀 Como Usar

### Executando pelo Python

```bash
python src/favoritos.py
```

### Gerando o executável (.exe)

```bash
pyinstaller favoritos.spec
```

O executável será gerado em `dist/favoritos.exe`.

---

## 📖 Guia de Uso

1. Exporte seus favoritos no navegador:
   - **Chrome**: `⋮` → Favoritos → Gerenciar favoritos → Exportar favoritos
   - **Firefox**: Menu → Favoritos → Gerenciar favoritos → Importar e fazer backup → Exportar favoritos para HTML
   - **Edge**: `⋯` → Favoritos → Gerenciar favoritos → Exportar favoritos

2. Abra a aplicação e clique em **📁 Carregar HTML**
3. Selecione o arquivo `.html` exportado
4. Navegue pelas pastas ou use a barra de **Pesquisar**
5. **Duplo clique** em qualquer link para abri-lo no navegador

---

## 📂 Estrutura do Projeto

```
favorites-search-version2/
├── src/
│   └── favoritos.py       # Código principal da aplicação
├── build/                 # Arquivos temporários do PyInstaller
├── dist/                  # Executável gerado
├── favoritos.spec         # Configuração do PyInstaller
├── .gitignore
└── README.md
```

---

## 🔧 Detalhes Técnicos

- **Parser HTML**: `BeautifulSoup` com `html.parser`. A lógica de parsing usa `find_parent('dl')` para corretamente identificar `<dt>` filhos diretos de cada `<dl>`, contornando a forma como os navegadores omitem tags de fechamento no HTML de favoritos.
- **Tema**: Detectado via registro do Windows (`HKEY_CURRENT_USER\...\Themes\Personalize`). Padrão `dark` em caso de falha.
- **Navegação**: Pastas expandem/colapsam com duplo clique; links abrem via `webbrowser.open()`.

---

## 💻 Requisitos do Sistema

- Windows 10 ou superior
- Python 3.9+ (somente para rodar via script)
