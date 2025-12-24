# Batch Folder Renamer

A simple batch folder renaming tool with a minimal GUI built using CustomTkinter (CTk).  

---

## ✨ Features
- 🚀 Automatically remove predefined prefixes.
- 🧠 Clean up suffixes (TV series season numbers).
- 🔄 Format folder names by removing extra spaces and dots.
- 📥 Downloadable `.exe` version (Windows only)


## 🖼️ Screenshots

<img width="520" height="546" alt="Untitled3" src="https://github.com/user-attachments/assets/15727611-bbc9-4b22-a917-bf1661a35e5f" />

## 📥 Download

You can download the latest compiled `.exe` version from the [Releases](https://github.com/TitanComputer/Batch-Folder-Renamer/releases/latest) section.  
No need to install Python — just download and run.

## ⚙️ Usage

If you're using the Python script:
```bash
python main.py
```
Or, run the Batch-Folder-Renamer.exe file directly if you downloaded the compiled version.

### 🖥️ How to Use the GUI

## How to Use

1. **Select a Folder**  
   - Click the **Browse** button and choose the main folder that contains your subfolders.

2. **Configure Prefixes**  
   - In the **Prefix Box**, add the text lines you want the program to remove from the beginning of each folder name.  
   - Example:  
     ```
     Torrenting
     www.UIndex.org -
     ```

3. **Start the Process**  
   - Click the **Start Process** button.  
   - The program will:
     - Remove any defined prefixes.  
     - Remove suffixes starting from `S01`, `s01`, etc. (season markers).  
     - Trim extra characters from the start and end of names.  
     - Replace dots (`.`), underscores (`_`), or dashes (`-`) with spaces.  
     - Capitalize each word (Title Case).  
     - Replace spaces with dashes (`-`).  

---

## 📦 Dependencies

- Python 3.10 or newer
- `CustomTkinter`
- Recommended: Create a virtual environment

Standard libraries only (os, re, etc.)

If you're modifying and running the script directly and use additional packages (like requests or tkinter), install them via:
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```bash
batch-folder-renamer/
│
├── main.py             # Main application entry point
├── assets/
│   └── icon.png        # Project icon
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies
```
## 🎨 Icon Credit
The application icon used in this project is sourced from [Flaticon](https://www.flaticon.com/free-icons/rename).

**Rename icon** created by [juicy_fish](https://www.flaticon.com/authors/juicy-fish) – [Flaticon](https://www.flaticon.com/)

## 🛠 Compiled with Nuitka and UPX
The executable was built using [`Nuitka`](https://nuitka.net/) and [`UPX`](https://github.com/upx/upx) for better performance and compactness, built automatically via GitHub Actions.

You can build the standalone executable using the following command:

```bash
.\venv\Scripts\python.exe -m nuitka --jobs=4 --enable-plugin=upx --upx-binary="YOUR PATH\upx.exe" --enable-plugin=multiprocessing --lto=yes --enable-plugin=tk-inter --windows-console-mode=disable --follow-imports --windows-icon-from-ico="assets/icon.png" --include-data-dir=assets=assets --python-flag=no_site,no_asserts,no_docstrings,static_hashes --onefile --onefile-no-compression --standalone --msvc=latest --output-filename=Batch-Folder-Renamer main.py
```

## 🚀 CI/CD

The GitHub Actions workflow builds the binary on every release and attaches it as an artifact.

## 🤝 Contributing
Pull requests are welcome.
If you have suggestions for improvements or new features, feel free to open an issue.

## ☕ Support
If you find this project useful and would like to support its development, consider donating:

<a href="http://www.coffeete.ir/Titan"><img width="500" height="140" alt="buymeacoffee" src="https://github.com/user-attachments/assets/8ddccb3e-2afc-4fd9-a782-89464ec7dead" /></a>

## 💰 USDT (Tether) – TRC20 Wallet Address:

```bash
TGoKk5zD3BMSGbmzHnD19m9YLpH5ZP8nQe
```
Thanks a lot for your support! 🙏
