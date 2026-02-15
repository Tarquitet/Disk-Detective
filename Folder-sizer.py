import sys
import subprocess
import os
import threading
import ctypes
import winreg

# --- BLOQUE DE AUTO-INSTALACIÓN Y PORTABILIDAD ---
def install_and_import(package, import_name=None):
    if import_name is None:
        import_name = package
    try:
        return __import__(import_name)
    except ImportError:
        print(f"[!] Instalando dependencia necesaria: {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            return __import__(import_name)
        except Exception as e:
            print(f"[x] Error instalando {package}: {e}")
            sys.exit(1)

# Instalamos librerías externas
tk = install_and_import("tkinter")
ttk = install_and_import("tkinter.ttk", "tkinter")
humanize = install_and_import("humanize")
tb = install_and_import("ttkbootstrap")

from tkinter import filedialog, messagebox
from ttkbootstrap.constants import *

# --- LÓGICA DEL SISTEMA ---

class SystemAnalyzer:
    @staticmethod
    def get_folder_size(start_path):
        """Calcula el tamaño total de una carpeta recursivamente."""
        total_size = 0
        file_count = 0
        try:
            for dirpath, dirnames, filenames in os.walk(start_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        try:
                            total_size += os.path.getsize(fp)
                            file_count += 1
                        except OSError:
                            continue
        except PermissionError:
            pass
        return total_size, file_count

    @staticmethod
    def get_installed_programs():
        """Obtiene lista de programas instalados desde el Registro."""
        programs = []
        uninstall_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        
        for p in uninstall_paths:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, p)
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        try:
                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            try:
                                size = winreg.QueryValueEx(subkey, "EstimatedSize")[0]
                            except FileNotFoundError:
                                size = 0
                            programs.append({"name": name, "size": size})
                        except FileNotFoundError:
                            pass
                    except OSError:
                        continue
            except OSError:
                continue
        
        return sorted(programs, key=lambda x: x['name'].lower())

# --- INTERFAZ GRÁFICA ---

class CleanerApp(tb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Analizador de Espacio y Software - Modo Portable")
        self.geometry("950x650")
        
        self.tabs = tb.Notebook(self)
        self.tabs.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        self.tab_folders = tb.Frame(self.tabs)
        self.tabs.add(self.tab_folders, text="🔍 Peso de Carpetas")
        self.setup_folder_tab()
        
        self.tab_apps = tb.Frame(self.tabs)
        self.tabs.add(self.tab_apps, text="📦 Software Instalado")
        self.setup_apps_tab()

    def create_scrolled_treeview(self, parent, columns):
        """Crea un Treeview con barra de desplazamiento manual."""
        frame = tb.Frame(parent)
        frame.pack(fill=BOTH, expand=YES)
        
        # Scrollbar
        scroll = tb.Scrollbar(frame, orient="vertical", bootstyle="round")
        scroll.pack(side=RIGHT, fill=Y)
        
        # Treeview
        tree = tb.Treeview(frame, columns=columns, show="headings", yscrollcommand=scroll.set, bootstyle="info")
        tree.pack(side=LEFT, fill=BOTH, expand=YES)
        
        scroll.config(command=tree.yview)
        return tree

    def setup_folder_tab(self):
        control_panel = tb.Frame(self.tab_folders)
        control_panel.pack(fill=X, pady=10)
        
        btn_scan = tb.Button(control_panel, text="Seleccionar Carpeta", bootstyle="primary", command=self.start_scan)
        btn_scan.pack(side=LEFT, padx=10)
        
        self.lbl_status = tb.Label(control_panel, text="Listo", bootstyle="inverse-secondary")
        self.lbl_status.pack(side=LEFT, padx=10)

        cols = ("Carpeta", "Archivos", "Peso", "Bytes_Raw") # Bytes_Raw oculta para ordenar
        self.tree_files = self.create_scrolled_treeview(self.tab_folders, cols)
        
        self.tree_files.heading("Carpeta", text="Nombre")
        self.tree_files.heading("Archivos", text="Archivos")
        self.tree_files.heading("Peso", text="Tamaño")
        
        self.tree_files.column("Carpeta", width=400)
        self.tree_files.column("Archivos", width=100, anchor="center")
        self.tree_files.column("Peso", width=150, anchor="e")
        self.tree_files["displaycolumns"] = ("Carpeta", "Archivos", "Peso") # Ocultamos raw bytes

    def setup_apps_tab(self):
        panel = tb.Frame(self.tab_apps)
        panel.pack(fill=X, pady=10)
        
        btn_refresh = tb.Button(panel, text="Escanear Programas", bootstyle="success", command=self.load_apps)
        btn_refresh.pack(side=LEFT, padx=10)
        
        lbl_warn = tb.Label(panel, text="⚠️ Cuidado con borrar 'Redistributables' (C++, .NET)", bootstyle="warning")
        lbl_warn.pack(side=LEFT, padx=10)

        cols = ("Programa", "Estado")
        self.tree_apps = self.create_scrolled_treeview(self.tab_apps, cols)
        
        self.tree_apps.heading("Programa", text="Nombre del Software")
        self.tree_apps.heading("Estado", text="Tipo Detectado")
        self.tree_apps.column("Programa", width=600)
        self.tree_apps.column("Estado", width=250)

    def start_scan(self):
        path = filedialog.askdirectory()
        if not path: return
            
        for item in self.tree_files.get_children():
            self.tree_files.delete(item)
            
        self.lbl_status.config(text=f"Analizando: {path}...")
        threading.Thread(target=self.scan_logic, args=(path,), daemon=True).start()

    def scan_logic(self, path):
        try:
            items = os.listdir(path)
            data = []
            
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    size, count = SystemAnalyzer.get_folder_size(full_path)
                    data.append((item, count, size))
                elif os.path.isfile(full_path):
                    size = os.path.getsize(full_path)
                    data.append((item, 1, size))
            
            # Ordenar por tamaño (bytes) descendente
            data.sort(key=lambda x: x[2], reverse=True)
            self.after(0, lambda: self.update_tree_files(data))
            
        except Exception as e:
            self.lbl_status.config(text=f"Error: {e}")

    def update_tree_files(self, data):
        for name, count, size in data:
            human_size = humanize.naturalsize(size)
            self.tree_files.insert("", END, values=(name, count, human_size, size))
        self.lbl_status.config(text="Análisis completado.")

    def load_apps(self):
        for item in self.tree_apps.get_children():
            self.tree_apps.delete(item)
            
        apps = SystemAnalyzer.get_installed_programs()
        
        for app in apps:
            name = app['name']
            tipo = "Aplicación"
            # Palabras clave de dependencias comunes en Windows
            keywords = ["redistributable", "c++", ".net", "framework", "runtime", "driver", "sdk", "library", "directx", "vulkan"]
            
            if any(k in name.lower() for k in keywords):
                tipo = "⚠️ LIBRERÍA / DEPENDENCIA"
            
            # Insertar con etiqueta de color si es dependencia
            item_id = self.tree_apps.insert("", END, values=(name, tipo))
            if "⚠️" in tipo:
                self.tree_apps.item(item_id, tags=('warning',))

        self.tree_apps.tag_configure('warning', foreground='orange')

if __name__ == "__main__":
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        is_admin = False

    if not is_admin:
        print("Tip: Ejecutar como Administrador permite leer carpetas de sistema.")
    
    app = CleanerApp()
    app.mainloop()