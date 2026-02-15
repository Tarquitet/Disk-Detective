# 🕵️ Disk Detective (Limpiador Portable)

[![Language](https://img.shields.io/badge/Lang-English-red?style=flat-square)](README.md)
[![Python](https://img.shields.io/badge/Python-3.x-yellow.svg?style=flat-square)](https://www.python.org/)

Una herramienta ligera y **autocontenida en Python** diseñada para visualizar el uso del disco y listar el software instalado en Windows.

Su enfoque es la **portabilidad**: el script detecta automáticamente si faltan librerías y las instala por sí mismo. Ideal para llevar en una USB o diagnósticos rápidos.

![1771192499421](images/README_ES/1771192499421.png)

## ✨ Características Principales

- **📦 Portabilidad Zero-Config:** Solo ejecuta el script. Si faltan dependencias, él mismo las descarga.
- **📂 Visualizador de Peso de Carpetas:**
  - Escanea cualquier directorio para identificar subcarpetas pesadas.
  - Muestra conteo de archivos y tamaños legibles (GB, MB).
- **🛡️ Listado Inteligente de Apps:**
  - Lista programas instalados consultando el Registro de Windows.
  - **Detección Heurística:** Marca automáticamente las dependencias del sistema (Visual C++, .NET, Drivers) en color **Naranja** para evitar desinstalaciones accidentales.
  - **Seguridad:** No desinstala programas directamente. Úsalo junto a desinstaladores como [BCUninstaller](https://www.bcuninstaller.com/).

## 🛠️ Requisitos

- **Sistema Operativo:** Windows 10/11
- **Runtime:** Python 3.6 o superior.

## 🚀 Cómo usar

1. Descarga el archivo `cleaner.py`.
2. Abre una terminal (CMD o PowerShell) en la carpeta.
3. Ejecuta el comando:

```bash
python cleaner.py
```

Nota: Ejecuta como Administrador para poder escanear carpetas del sistema.
⚠️ Nota Importante sobre Librerías

Windows no rastrea qué aplicación usa qué versión de "Visual C++" o ".NET". Esta herramienta resalta estas librerías para advertirte. No las borres a menos que sepas lo que haces.
📄 Licencia

Este proyecto es de código abierto bajo la Licencia MIT.
