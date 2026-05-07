import json
import re
import os

def sync():
    print("Sincronizando versões...")
    
    # 1. Ler versão do utils.py
    version = "0.0.0"
    if os.path.exists("utils.py"):
        with open("utils.py", "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'VERSION = "([\d\.]+)"', content)
            if match:
                version = match.group(1)
    
    # 2. Ler/Atualizar version.json
    data = {}
    if os.path.exists("version.json"):
        with open("version.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    
    # Atualizar campos
    data["version"] = version
    if "changelog" not in data:
        data["changelog"] = "Melhorias gerais e correções de estabilidade."
    
    # URL da release (Padronizada para o GitHub)
    # Nota: Vamos configurar o workflow para criar uma release com o nome 'latest' ou tag da versão
    data["url"] = f"https://github.com/tiagoflstudio-oss/Flux_OS/releases/latest/download/Flux_OS_Sapphire.exe"
    
    with open("version.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"OK: version.json atualizado para v{version}")
    print(f"URL de Download: {data['url']}")

if __name__ == "__main__":
    sync()
