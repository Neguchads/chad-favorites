# 🗺️ Next Steps — Gerenciador de Favoritos

> Backlog de melhorias priorizadas por impacto vs. esforço.

---

## ✅ Alta Prioridade — Implementadas em v1.1

- [x] **Validação de URL antes de abrir** — Segurança: só abre esquemas `http://` e `https://`, bloqueando `file:///`, `javascript:` e handlers do Windows
- [x] **Histórico de arquivos recentes** — UX: salva os últimos 5 arquivos carregados em `recent_files.json`; menu de acesso rápido na interface
- [x] **Ordenação por nome / URL** — Clique no header da coluna Nome ou URL para ordenar crescente/decrescente

---

## ✅ Médio Prazo — Implementadas em v1.2

- [x] **Favicons dos sites** — Ícone 16x16 de cada site exibido na Treeview, buscado via Google S2 em thread daemon (não trava a UI)
- [x] **Exportar favoritos filtrados** — Botão `💾 Exportar filtro` gera HTML padrão Netscape com os resultados da pesquisa atual
- [x] **Barra de status com contador** — Rodapé exibe `X favorito(s) em Y pasta(s)` contado recursivamente; contador de ícones no canto direito

---

## 🟡 Médio Prazo — Pendentes

- [ ] **(sem pendências de médio prazo)**

---

## ✅ Longo Prazo — Implementadas em v1.3

- [x] **Ícone `.ico` no executável** — Gerado com Pillow (6 tamanhos: 16→56px), embutido via PyInstaller `icon=` e exibido na janela com `root.iconbitmap()`
- [x] **Cross-platform (macOS/Linux)** — `darkdetect.theme()` detecta o tema em qualquer OS; fallback `winreg` mantido para Windows sem o pacote

---

## 📋 Histórico de Versões

| Versão | Data | Mudanças |
|---|---|---|
| v1.0 | 2026-04-22 | Versão inicial: parser HTML corrigido, DRM removido |
| v1.1 | 2026-04-22 | Validação de URL, histórico recente, ordenação por coluna, rodapé contador |
| v1.2 | 2026-04-22 | Favicons assíncronos (Pillow + threading), exportar filtro como HTML, status bar detalhada |
| v1.3 | 2026-04-22 | Ícone ICO no executável e janela, detecção de tema cross-platform via darkdetect |
| v1.4 | 2026-04-22 | Remoção da barra de status verde e carregamento automático do último arquivo no histórico |
