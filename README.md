# 📚 Chad Favorites v1.4.3

A professional desktop application for Windows to import, organize, and navigate bookmark HTML files exported from any browser (Chrome, Firefox, Edge, etc.).

---

## ✨ Features

- 📁 **HTML Import** — Full support for the standard Netscape Bookmark File 1 format.
- 🌳 **Hierarchical Tree** — Intuitive subfolder navigation.
- 🔍 **Instant Search** — Filter thousands of bookmarks by title or URL in real-time.
- 🖼️ **Smart Favicons** — Automatic download and disk caching of site icons for instant access.
- 💾 **Filtered Export** — Generate new HTML files containing only your search results.
- 🕐 **Recent History** — Quick access to the last 5 loaded files.
- 🧠 **Auto-Load** — Remembers the last file opened and loads it instantly on startup.
- 🌓 **Dynamic Theme** — Automatic Light/Dark mode detection (Windows, macOS, Linux).
- 🖱️ **Secure Navigation** — Link validation to prevent opening malicious scripts.

---

## 🛠️ Tech Stack & Dependencies

| Library | Purpose |
|---|---|
| `tkinter` | Native GUI |
| `sv_ttk` | Modern Sun Valley theme |
| `beautifulsoup4` | Robust HTML parsing |
| `pillow` | Image processing (Favicons) |
| `requests` | Background icon downloads |
| `darkdetect` | Cross-platform theme detection |

---

## 🚀 Installation & Usage

### 1. Requirements
- Python 3.9+

### 2. Setup
```bash
# Clone the repository
git clone https://github.com/your-user/chad-favorites.git

# Enter folder
cd chad-favorites

# Install dependencies
pip install -r requirements.txt
```

### 3. Running
```bash
python src/favoritos.py
```

### 4. Build Executable (.exe)
```bash
pyinstaller chad-favorites.spec
```

---

## 📂 Project Structure

```text
chad-favorites/
├── src/
│   └── favoritos.py       # Main application logic
├── assets/
│   └── icon.ico           # Official app icon
├── chad-favorites.spec    # PyInstaller build config
├── requirements.txt       # Python dependencies
├── LICENSE                # MIT License
└── README.md              # Documentation
```

---

## ⚖️ License

This project is licensed under the [MIT License](LICENSE).
