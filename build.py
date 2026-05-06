import subprocess
import os
import sys
import shutil

def build():
    print("="*60)
    print(" KILLPROCESS - BUILD SYSTEM (PyInstaller)")
    print("="*60)
    
    # Nome do arquivo principal e do executável
    main_script = "gui.py"
    exe_name = "Killprocess_Sapphire"
    
    # Verificar se o PyInstaller está instalado
    try:
        import PyInstaller
    except ImportError:
        print(" PyInstaller nao encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    # Limpar builds anteriores
    print(" Limpando pastas de build anteriores...")
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    if os.path.exists(f"{exe_name}.spec"):
        os.remove(f"{exe_name}.spec")

    # Caminho dos assets
    assets_path = "assets"
    if not os.path.exists(assets_path):
        os.makedirs(assets_path)

    # Gerar .ico a partir do .png se necessário

    icon_png = os.path.join(assets_path, "icon.png")
    icon_ico = os.path.join(assets_path, "icon.ico")
    if os.path.exists(icon_png):
        print(" Convertendo icon.png para icon.ico...")
        try:
            from PIL import Image
            img = Image.open(icon_png)
            # Salva como ICO com múltiplos tamanhos para compatibilidade Windows
            img.save(icon_ico, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
        except Exception as e:
            print(f" ⚠️ Erro ao converter ícone: {e}")

    # Comando de Build
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        f"--name={exe_name}",
        f"--icon={icon_ico}" if os.path.exists(icon_ico) else "",
        f"--add-data={assets_path};assets",
        f"--add-data=version.json;.",
        "--uac-admin",
        "--clean",
        main_script
    ]
    # Filtrar argumentos vazios (caso o ícone não exista)
    cmd = [arg for arg in cmd if arg]

    
    print(f"\n Iniciando compilacao de '{exe_name}'...")
    print(f" Comando: {' '.join(cmd)}\n")
    
    try:
        subprocess.run(cmd, check=True)
        print("\n" + "="*60)
        print(f" SUCESSO! O executavel foi gerado com exito.")
        print(f" Local: {os.path.join(os.getcwd(), 'dist', exe_name + '.exe')}")
        print("="*60)
    except subprocess.CalledProcessError as e:
        print(f"\n ERRO durante o processo de build: {e}")
    except Exception as e:
        print(f"\n ERRO inesperado: {e}")

if __name__ == "__main__":
    build()
