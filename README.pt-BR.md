# 📚 Chad Favorites v1.4.3

Uma aplicação desktop profissional para Windows para importar, organizar e navegar em arquivos HTML de favoritos exportados de qualquer navegador (Chrome, Firefox, Edge, etc).

---

## ✨ Funcionalidades

- 📁 **Importação de HTML** — Suporte total ao formato padrão Netscape Bookmark File 1.
- 🌳 **Árvore Hierárquica** — Navegação intuitiva em subpastas.
- 🔍 **Busca Instantânea** — Filtre milhares de favoritos por título ou URL em tempo real.
- 🖼️ **Favicons Inteligentes** — Download automático e cache em disco de ícones dos sites para acesso imediato.
- 💾 **Exportação Filtrada** — Gere novos arquivos HTML contendo apenas os resultados da sua pesquisa.
- 🕐 **Histórico Recente** — Acesso rápido aos últimos 5 arquivos carregados.
- 🧠 **Auto-Load** — Lembra o último arquivo aberto e o carrega instantaneamente ao iniciar.
- 🌓 **Tema Dinâmico** — Detecção automática do modo Claro/Escuro (Windows, macOS, Linux).
- 🖱️ **Navegação Segura** — Validação de links para evitar a abertura de scripts maliciosos.

---

## 🛠️ Tecnologias & Dependências

| Biblioteca | Finalidade |
|---|---|
| `tkinter` | Interface gráfica nativa |
| `sv_ttk` | Tema moderno Sun Valley |
| `beautifulsoup4` | Parsing robusto de HTML |
| `pillow` | Processamento de imagens (Favicons) |
| `requests` | Downloads de ícones em segundo plano |
| `darkdetect` | Detecção de tema multiplataforma |

---

## 🚀 Instalação & Uso

### 1. Requisitos
- Python 3.9+

### 2. Configuração
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/chad-favorites.git

# Entre na pasta
cd chad-favorites

# Instale as dependências
pip install -r requirements.txt
```

### 3. Execução
```bash
python src/favoritos.py
```

### 4. Gerar Executável (.exe)
```bash
pyinstaller chad-favorites.spec
```

---

## 📂 Estrutura do Projeto

```text
chad-favorites/
├── src/
│   └── favoritos.py       # Lógica principal da aplicação
├── assets/
│   └── icon.ico           # Ícone oficial do app
├── chad-favorites.spec    # Configuração de build do PyInstaller
├── requirements.txt       # Dependências Python
├── LICENSE                # Licença MIT
└── README.md              # Documentação (Inglês)
```

---

## ⚖️ Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
