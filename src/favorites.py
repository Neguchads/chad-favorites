import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from bs4 import BeautifulSoup
import webbrowser
import sv_ttk
import json
import os
import sys
import threading
import io
from urllib.parse import urlparse

import requests
from PIL import Image, ImageTk

try:
    import darkdetect
    HAS_DARKDETECT = True
except ImportError:
    HAS_DARKDETECT = False

# -------------------------------------------------------
# Constantes
# -------------------------------------------------------
if getattr(sys, 'frozen', False):
    # Em modo executável, usamos a pasta AppData do usuário para persistência garantida
    _APP_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), "ChadFavorites")
else:
    _APP_DIR = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(_APP_DIR):
    try:
        os.makedirs(_APP_DIR, exist_ok=True)
    except Exception:
        _APP_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))

RECENT_FILES_PATH = os.path.join(_APP_DIR, "recent_files.json")
FAVICONS_DIR = os.path.join(_APP_DIR, "favicons")
MAX_RECENT = 5
FAVICON_SIZE = (16, 16)
FAVICON_API = "https://www.google.com/s2/favicons?sz=16&domain={domain}"

# Garante que a pasta de favicons existe
os.makedirs(FAVICONS_DIR, exist_ok=True)

# Ícone da aplicação — relativo ao executável ou ao script
_BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
ICON_PATH = os.path.join(os.path.dirname(_BASE_DIR), "assets", "icon.ico")
if not os.path.exists(ICON_PATH):
    # Fallback: mesmo diretório do script
    ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "icon.ico")


# -------------------------------------------------------
# Utilitários de sistema
# -------------------------------------------------------

def get_system_theme():
    """Detecta o tema do sistema (claro/escuro) — multiplataforma"""
    # darkdetect funciona em Windows, macOS e Linux
    if HAS_DARKDETECT:
        try:
            result = darkdetect.theme()
            if result is not None:
                return "dark" if result.lower() == "dark" else "light"
        except Exception:
            pass

    # Fallback Windows via winreg
    try:
        import winreg
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        val, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return "light" if val == 1 else "dark"
    except Exception:
        pass

    return "dark"


def load_recent_files():
    """Carrega a lista de arquivos recentes do disco"""
    try:
        with open(RECENT_FILES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [p for p in data if os.path.exists(p)]
    except Exception:
        return []


def save_recent_files(files):
    """Persiste a lista de arquivos recentes no disco"""
    try:
        # Garante que a pasta existe antes de salvar
        os.makedirs(os.path.dirname(RECENT_FILES_PATH), exist_ok=True)
        with open(RECENT_FILES_PATH, "w", encoding="utf-8") as f:
            json.dump(files, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar histórico: {e}")


# -------------------------------------------------------
# Classe principal
# -------------------------------------------------------

class BookmarkManager:
    def __init__(self, root):
        self.root = root
        self.app_title = "Chad Favorites"
        self.root.title(self.app_title)
        self.root.geometry("1000x700")

        # Ícone da janela e taskbar
        try:
            self.root.iconbitmap(ICON_PATH)
        except Exception:
            pass

        self.all_bookmarks = []       # lista plana de {title, url}
        self.html_content = ""
        self.recent_files = load_recent_files()
        self._sort_state = {"col": None, "reverse": False}

        # Cache de favicons: domain -> ImageTk.PhotoImage
        self._favicon_cache: dict = {}
        # Ícone padrão usado quando favicon não está disponível
        self._default_icon: ImageTk.PhotoImage | None = None

        # Itens pendentes de favicon: iid -> domain
        self._pending_favicons: dict = {}

        self.setup_ui()
        self._make_default_icon()

        # Carrega automaticamente o último arquivo, se houver
        if self.recent_files:
            self.load_html(filepath=self.recent_files[0])

    # -------------------------------------------------------
    # UI
    # -------------------------------------------------------

    def setup_ui(self):
        sv_ttk.set_theme(get_system_theme())

        style = ttk.Style()
        style.configure("Treeview", font=('Segoe UI', 10), rowheight=20)
        style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'))

        # Frame de controles
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill=tk.X)

        btn_load = ttk.Button(top_frame, text="📁 Load HTML",
                              command=self.load_html, style="Accent.TButton")
        btn_load.pack(side=tk.LEFT, padx=(0, 5))

        # Recentes
        self.btn_recent = ttk.Menubutton(top_frame, text="🕐 Recent ▾")
        self.btn_recent.pack(side=tk.LEFT, padx=(0, 5))
        self.recent_menu = tk.Menu(self.btn_recent, tearoff=0)
        self.btn_recent["menu"] = self.recent_menu
        self._rebuild_recent_menu()

        # Exportar
        self.btn_export = ttk.Button(top_frame, text="💾 Export Filter",
                                     command=self.export_filtered, state="disabled")
        self.btn_export.pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(top_frame, text="Search:", font=('Segoe UI', 10)).pack(side=tk.LEFT)
        self.entry_search = ttk.Entry(top_frame, width=45, font=('Segoe UI', 10))
        self.entry_search.pack(side=tk.LEFT, padx=10)
        self.entry_search.bind("<KeyRelease>", self.filter_bookmarks)

        # Treeview
        columns = ("url",)
        self.tree = ttk.Treeview(self.root, columns=columns, selectmode="browse")

        self.tree.heading("#0", text="Name ↕", anchor=tk.W,
                          command=lambda: self._sort_tree("#0"))
        self.tree.heading("url", text="Address (URL) ↕", anchor=tk.W,
                          command=lambda: self._sort_tree("url"))

        self.tree.column("#0", width=400, stretch=tk.NO)
        self.tree.column("url", width=550)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 0))
        self.tree.bind("<Double-1>", self.on_double_click)

        scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Rodapé de status detalhado
        footer_frame = ttk.Frame(self.root, padding=(10, 4))
        footer_frame.pack(fill=tk.X)
        self.footer_label = ttk.Label(footer_frame, text="", font=('Segoe UI', 8))
        self.footer_label.pack(side=tk.LEFT)
        self.favicon_status = ttk.Label(footer_frame, text="", font=('Segoe UI', 8))
        self.favicon_status.pack(side=tk.RIGHT, padx=10)

    # -------------------------------------------------------
    # Ícone padrão (globo cinza 16x16)
    # -------------------------------------------------------

    def _make_default_icon(self):
        try:
            img = Image.new("RGBA", FAVICON_SIZE, (180, 180, 180, 200))
            self._default_icon = ImageTk.PhotoImage(img)
        except Exception:
            self._default_icon = None

    # -------------------------------------------------------
    # Arquivos Recentes
    # -------------------------------------------------------

    def _rebuild_recent_menu(self):
        self.recent_menu.delete(0, tk.END)
        if not self.recent_files:
            self.recent_menu.add_command(label="(no recent files)", state="disabled")
        else:
            for path in self.recent_files:
                self.recent_menu.add_command(
                    label=os.path.basename(path),
                    command=lambda p=path: self.load_html(filepath=p)
                )
            self.recent_menu.add_separator()
            self.recent_menu.add_command(label="🗑 Clear history", command=self._clear_recent)

    def _add_to_recent(self, filepath):
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)
        self.recent_files.insert(0, filepath)
        self.recent_files = self.recent_files[:MAX_RECENT]
        save_recent_files(self.recent_files)
        self._rebuild_recent_menu()

    def _clear_recent(self):
        self.recent_files = []
        save_recent_files(self.recent_files)
        self._rebuild_recent_menu()

    # -------------------------------------------------------
    # Carregamento de HTML
    # -------------------------------------------------------

    def load_html(self, filepath=None):
        if filepath is None:
            filepath = filedialog.askopenfilename(filetypes=[("HTML Files", "*.html")])
        if not filepath:
            return

        if not os.path.exists(filepath):
            messagebox.showerror("File not found",
                                 f"The file no longer exists:\n{filepath}")
            return

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            self.html_content = file.read()

        self._add_to_recent(filepath)
        self.root.title(f"{self.app_title} — {os.path.basename(filepath)}")
        self.build_tree()

    # -------------------------------------------------------
    # Construção da Árvore
    # -------------------------------------------------------

    def build_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.all_bookmarks.clear()
        self._pending_favicons.clear()
        self._sort_state = {"col": None, "reverse": False}
        self.btn_export.config(state="disabled")

        if not self.html_content:
            return

        soup = BeautifulSoup(self.html_content, 'html.parser')
        main_dl = soup.find('dl')
        if main_dl:
            self.parse_bookmarks(main_dl, "")

        self._update_footer()
        # Dispara o carregamento de favicons em background
        self._start_favicon_loader()

    def parse_bookmarks(self, dl_element, parent_node):
        """Função recursiva para ler as pastas (H3) e os links (A)"""
        dts = dl_element.find_all('dt')
        direct_dts = [dt for dt in dts if dt.find_parent('dl') == dl_element]

        for dt in direct_dts:
            h3 = dt.find('h3', recursive=False) or dt.find('h3')
            if h3:
                folder_name = f"📁 {h3.text.strip()}"
                folder_node = self.tree.insert(parent_node, 'end',
                                               text=folder_name, open=False)
                next_dl = dt.find('dl', recursive=False) or dt.find('dl')
                if next_dl:
                    self.parse_bookmarks(next_dl, folder_node)
            else:
                a = dt.find('a', recursive=False) or dt.find('a')
                if a:
                    title = a.text.strip()
                    url = a.get('href', '')
                    iid = self.tree.insert(parent_node, 'end',
                                           text=f"  {title}",
                                           values=(url,),
                                           image=self._default_icon or "")
                    self.all_bookmarks.append({"title": title, "url": url, "iid": iid})
                    # Agenda favicon para esse item
                    parsed = urlparse(url)
                    if parsed.scheme in ('http', 'https') and parsed.netloc:
                        self._pending_favicons[iid] = parsed.netloc

    # -------------------------------------------------------
    # Favicons — download assíncrono
    # -------------------------------------------------------

    def _start_favicon_loader(self):
        if not self._pending_favicons:
            return
        self.favicon_status.config(text="⏳ Loading icons...")
        t = threading.Thread(target=self._load_favicons_worker, daemon=True)
        t.start()

    def _load_favicons_worker(self):
        """Roda em thread separada — não toca na UI diretamente"""
        session = requests.Session()
        total = len(self._pending_favicons)
        done = 0

        for iid, domain in list(self._pending_favicons.items()):
            try:
                icon = self._fetch_favicon(session, domain)
            except Exception:
                icon = None
            # Agenda a atualização na thread principal via after()
            self.root.after(0, self._apply_favicon, iid, domain, icon)
            done += 1
            self.root.after(0, self.favicon_status.config,
                            {"text": f"⏳ Icons: {done}/{total}"})

        self.root.after(0, self.favicon_status.config, {"text": f"✅ {total} icon(s) loaded"})

    def _fetch_favicon(self, session, domain):
        """Busca o favicon (Cache em memória -> Cache em disco -> Download)"""
        if domain in self._favicon_cache:
            return self._favicon_cache[domain]

        # 1. Tenta carregar do cache em disco
        local_path = os.path.join(FAVICONS_DIR, f"{domain}.png")
        if os.path.exists(local_path):
            try:
                img = Image.open(local_path).resize(FAVICON_SIZE, Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self._favicon_cache[domain] = photo
                return photo
            except Exception:
                pass

        # 2. Se não existir no disco, faz o download
        url = FAVICON_API.format(domain=domain)
        resp = session.get(url, timeout=5)
        resp.raise_for_status()

        img_data = io.BytesIO(resp.content)
        img = Image.open(img_data).resize(FAVICON_SIZE, Image.LANCZOS)
        
        # Salva no disco para a próxima vez
        try:
            img.save(local_path, "PNG")
        except Exception:
            pass

        photo = ImageTk.PhotoImage(img)
        self._favicon_cache[domain] = photo
        return photo

    def _apply_favicon(self, iid, domain, icon):
        """Atualiza o ícone do item na Treeview (roda na thread principal)"""
        try:
            if icon and self.tree.exists(iid):
                self.tree.item(iid, image=icon)
        except Exception:
            pass

    # -------------------------------------------------------
    # Pesquisa
    # -------------------------------------------------------

    def filter_bookmarks(self, event=None):
        query = self.entry_search.get().lower()

        if not query:
            self.build_tree()
            self.btn_export.config(state="disabled")
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        result_node = self.tree.insert("", 'end', text="🔍 Search Results", open=True)
        count = 0
        for bm in self.all_bookmarks:
            if query in bm['title'].lower() or query in bm['url'].lower():
                domain = urlparse(bm['url']).netloc
                icon = self._favicon_cache.get(domain, self._default_icon or "")
                self.tree.insert(result_node, 'end',
                                 text=f"  {bm['title']}",
                                 values=(bm['url'],),
                                 image=icon)
                count += 1

        self.footer_label.config(
            text=f"{count} result(s) for \"{self.entry_search.get()}\""
        )
        # Habilita exportar apenas se há resultados
        self.btn_export.config(state="normal" if count > 0 else "disabled")

    # -------------------------------------------------------
    # Exportar favoritos filtrados
    # -------------------------------------------------------

    def export_filtered(self):
        """Salva os favoritos visíveis no resultado de pesquisa como HTML"""
        query = self.entry_search.get().strip()
        if not query:
            messagebox.showinfo("Export", "No active filter. Search for something before exporting.")
            return

        results = [
            bm for bm in self.all_bookmarks
            if query.lower() in bm['title'].lower() or query.lower() in bm['url'].lower()
        ]

        if not results:
            messagebox.showinfo("Export", "No results to export.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML Files", "*.html")],
            initialfile=f"bookmarks_{query.replace(' ', '_')}.html",
            title="Save filtered bookmarks"
        )
        if not filepath:
            return

        lines = [
            "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
            "<!-- This is an automatically generated file. -->",
            "<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html; charset=UTF-8\">",
            f"<TITLE>Bookmarks — {query}</TITLE>",
            f"<H1>Filtered bookmarks: {query}</H1>",
            "<DL><p>",
        ]
        for bm in results:
            title = bm['title'].replace("<", "&lt;").replace(">", "&gt;")
            url = bm['url']
            lines.append(f'    <DT><A HREF="{url}">{title}</A>')
        lines.append("</DL><p>")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        messagebox.showinfo(
            "Export completed",
            f"{len(results)} bookmark(s) exported to:\n{filepath}"
        )

    # -------------------------------------------------------
    # Ordenação por coluna
    # -------------------------------------------------------

    def _sort_tree(self, col):
        """Ordena os itens raiz da árvore pela coluna clicada"""
        if self._sort_state["col"] == col:
            self._sort_state["reverse"] = not self._sort_state["reverse"]
        else:
            self._sort_state["col"] = col
            self._sort_state["reverse"] = False

        reverse = self._sort_state["reverse"]

        def get_key(iid):
            if col == "#0":
                return self.tree.item(iid, "text").lower()
            else:
                vals = self.tree.item(iid, "values")
                return vals[0].lower() if vals else ""

        children = list(self.tree.get_children(""))
        children.sort(key=get_key, reverse=reverse)

        for idx, iid in enumerate(children):
            self.tree.move(iid, "", idx)

        arrow = " ▲" if not reverse else " ▼"
        self.tree.heading("#0", text=f"Nome{arrow if col == '#0' else ' ↕'}")
        self.tree.heading("url", text=f"Endereço (URL){arrow if col == 'url' else ' ↕'}")

    # -------------------------------------------------------
    # Abertura de links — com validação de segurança
    # -------------------------------------------------------

    def on_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item[0])
        values = item.get('values')

        if values:
            url = values[0]
            parsed = urlparse(url)
            if parsed.scheme in ('http', 'https'):
                webbrowser.open(url)
            else:
                messagebox.showwarning(
                    "URL blocked",
                    f"This link cannot be opened for security reasons:\n\n{url}\n\n"
                    f"Scheme not allowed: '{parsed.scheme}'"
                )
        else:
            is_open = self.tree.item(selected_item[0], "open")
            self.tree.item(selected_item[0], open=not is_open)

    # -------------------------------------------------------
    # Rodapé de status detalhado
    # -------------------------------------------------------

    def _count_recursive(self, parent=""):
        """Conta pastas e links em toda a árvore recursivamente"""
        folders = links = 0
        for iid in self.tree.get_children(parent):
            vals = self.tree.item(iid, "values")
            if vals:
                links += 1
            else:
                folders += 1
            sub_f, sub_l = self._count_recursive(iid)
            folders += sub_f
            links += sub_l
        return folders, links

    def _update_footer(self):
        folders, links = self._count_recursive()
        self.footer_label.config(
            text=f"{links} bookmark(s) in {folders} folder(s)"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = BookmarkManager(root)
    root.mainloop()