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
git clone https://github.com/gustavo-git/chad-favorites.git

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

## 🤝 Contributing & Community Guidelines

We welcome contributions! To maintain a healthy and productive community, please follow these guidelines:

### How to Contribute
1. **Fork** the project.
2. **Create a branch** for your feature (`git checkout -b feature/AmazingFeature`).
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`).
4. **Push** to the branch (`git push origin feature/AmazingFeature`).
5. **Open a Pull Request**.

### Community Rules
- **Respect**: Be kind and respectful to all contributors.
- **Clarity**: Write clear and descriptive commit messages and PR descriptions.
- **Code Quality**: Ensure your code follows Python PEP 8 standards.
- **Issues**: Before starting a major change, open an issue to discuss it.

---

## 🛡️ Security Policy

We take security seriously. 
- **Link Safety**: The application validates all URLs to ensure they use `http` or `https` protocols, preventing the execution of local scripts or malicious schemes.
- **Reporting Vulnerabilities**: If you find any security vulnerability, please do NOT open a public issue. Instead, contact the maintainers directly at [your-email@example.com] or via private message.

---

## ⚖️ License

This project is licensed under the [MIT License](LICENSE).
