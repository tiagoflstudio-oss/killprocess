import ctypes
import sys
import os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_admin_elevation():
    """ Garante que o programa rode como administrador. """
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def hide_console():
    """ Esconde a janela do terminal de forma segura. """
    try:
        hWnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hWnd:
            ctypes.windll.user32.ShowWindow(hWnd, 0) # 0 = SW_HIDE
    except:
        pass

def show_console():
    """ Mostra a janela do terminal (útil para debug). """
    try:
        hWnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hWnd:
            ctypes.windll.user32.ShowWindow(hWnd, 5) # 5 = SW_SHOW
    except:
        pass
