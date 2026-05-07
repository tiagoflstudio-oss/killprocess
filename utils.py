import os
import sys
import subprocess

VERSION = "2.1.31" # Versão Atual (Sapphire Edition)
DRY_RUN = True  # Modo Simulação por padrão
UPDATE_URL = "https://raw.githubusercontent.com/tiagoflstudio-oss/killprocess/main/version.json"

def resource_path(relative_path):
    """ Retorna o caminho absoluto para recursos, funcionando em Dev e no PyInstaller exe. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def is_admin():
    """ Verifica se o programa está rodando com privilégios de administrador. """
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_cmd(cmd, dry_run=True):
    """ Executa um comando via PowerShell com suporte a modo de simulação. """
    if dry_run:
        return f"[SIMULAÇÃO]: {cmd}"
    try:
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)
