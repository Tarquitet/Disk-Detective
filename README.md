# 🕵️ Disk Detective (Portable Cleaner)

[![Language](https://img.shields.io/badge/Lang-Español-blue?style=flat-square)](README_ES.md)
[![Python](https://img.shields.io/badge/Python-3.x-yellow.svg?style=flat-square)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)

A lightweight, **self-contained Python tool** designed to visualize disk usage and list installed software on Windows.

It focuses on **portability**: the script automatically checks for and installs its own dependencies (`ttkbootstrap`, `humanize`) upon the first run, making it perfect for USB drives or quick diagnostics without manual environment setup.

## ✨ Key Features

* **📦 Zero-Config Portability:** Just run the script. It auto-detects missing libraries and installs them via `pip` internally.
* **📂 Folder Weight Visualizer:**
    * Scans any directory to identify heavy subfolders.
    * Displays file count and human-readable sizes (GB, MB).
* **🛡️ Smart App Listing:**
    * Lists installed programs via Windows Registry.
    * **Heuristic Detection:** Automatically flags system dependencies (Visual C++, .NET, Drivers) in **Orange** to prevent accidental uninstallation.
    * **Safety First:** It does *not* uninstall programs directly. It acts as an investigator tool to be used alongside uninstallers like [BCUninstaller](https://www.bcuninstaller.com/).

## 🛠️ Requirements

* **OS:** Windows 10/11
* **Runtime:** Python 3.6 or higher.

## 🚀 Usage

1.  Download the `cleaner.py` file.
2.  Open a terminal (CMD or PowerShell) in the folder.
3.  Run the script:

```bash
python cleaner.py
```

Note: Run as Administrator to scan system folders like "Program Files".
⚠️ Important Note on Dependencies

Windows does not natively track which application uses which specific C++ Redistributable or .NET Framework. This tool detects and highlights these libraries to warn you. Do not delete highlighted libraries unless you are absolutely certain.
📄 License

This project is open-source and available under the MIT License.
