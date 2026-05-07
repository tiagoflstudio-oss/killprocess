import re

def fix_mojibake(text):
    # Tenta reverter o double/triple UTF-8 mangling
    for _ in range(3):
        try:
            # Pega a string corrompida, converte pra bytes usando cp1252 e volta pra utf-8
            # Mas se houver algum char q não existe, ignoramos.
            # Um regex simples para achar partes corrompidas e focar nelas:
            fixed = text.encode('cp1252').decode('utf-8')
            text = fixed
        except Exception:
            break
    return text

with open('gui.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Ao invés do script burro tentar consertar tudo (que pode falhar em caracteres de controle),
# vamos consertar com uma abordagem mais segura:
def safe_fix(match):
    s = match.group(0)
    for _ in range(3):
        try:
            s = s.encode('cp1252').decode('utf-8')
        except:
            pass
    return s

# Tenta capturar sequências de caracteres estranhos típicos de mojibake (Ã etc)
content = re.sub(r'[ÃÂ][\x80-\xff\w]+', safe_fix, content)

# Para garantir, vamos usar uma função manual para os mais comuns:
replacements = {
    "ÃƒÂ§ÃƒÂ£o": "ção",
    "ÃƒÂ§ÃƒÂµes": "ções",
    "ÃƒÂ¡": "á",
    "ÃƒÂ©": "é",
    "ÃƒÂ­": "í",
    "ÃƒÂ³": "ó",
    "ÃƒÂº": "ú",
    "ÃƒÂ£": "ã",
    "ÃƒÂµ": "õ",
    "ÃƒÂ¢": "â",
    "ÃƒÂª": "ê",
    "ÃƒÂ§": "ç",
    "Ãƒâ€¡": "Ç",
    "ÃƒÆ’": "Ã",
    "ÃƒÂ": "Í", # e outros
    "Ã¢Å“Â¨": "✨",
    "Ã¢Å¡Â¡": "⚡",
    "Ã°Å¸â€ Â¥": "🔥",
    "Ã°Å¸â€˜â€˜": "👑",
    "Ã°Å¸Å¡â‚¬": "🚀",
    "Ã°Å¸â€ºÂ Ã¯Â¸Â": "🛠️",
    "Ã°Å¸â€ Â": "🔍",
    "Ã¢â€”Â": "●",
    "Ã°Å¸Å¸Â¢": "🟢",
    "Ã°Å¸Å¸Â¡": "🟡",
    "Ã°Å¸Å¸Â": "🟠",
    "Ã°Å¸â€ Â´": "🔴",
    "Ã°Å¸Å¸Â£": "🟣",
    "Ã°Å¸Å’Â": "🌐",
    "Ã°Å¸â€ â€™": "🔒",
    "Ã°Å¸â€ â€ž": "🔄",
    "Ã°Å¸Â§Âª": "🧪",
    "Ã¢Å“â€¦": "✅",
    "Ã¢Å¡Â": "⚠️",
    "Ã°Å¸â€ºÂ¡Ã¯Â¸Â": "🛡️",
    "Ã¯Â¸Â": "️",
    "Ã¢â€": "▶",
    "Ã¢â€”â‚¬": "◀",
    "Ã°Å¸â€œÅ": "📊",
    "Ã°Å¸Â Æ": "⚙",
    "Ã°Å¸â€˜Â": "👁",
    "Ã°Å¸â€œÂ": "📁",
}

for k, v in replacements.items():
    content = content.replace(k, v)

# Tenta consertar também a versão de um único nível de mangling:
replacements_single = {
    "Ã§Ã£o": "ção",
    "Ã§Ãµes": "ções",
    "Ã¡": "á",
    "Ã©": "é",
    "Ã­": "í",
    "Ã³": "ó",
    "Ãº": "ú",
    "Ã£": "ã",
    "Ãµ": "õ",
    "Ã¢": "â",
    "Ãª": "ê",
    "Ã§": "ç",
    "Ã‡": "Ç",
    "Ãƒ": "Ã",
    "Ã": "Í",
    "âœ¨": "✨",
    "âš¡": "⚡",
    "ðŸ”¥": "🔥",
    "ðŸ‘‘": "👑",
    "ðŸš€": "🚀",
    "ðŸ› ï¸": "🛠️",
    "ðŸ”": "🔍",
    "â—": "●",
    "ðŸŸ¢": "🟢",
    "ðŸŸ¡": "🟡",
    "ðŸŸ": "🟠",
    "ðŸ”´": "🔴",
    "ðŸŸ£": "🟣",
    "ðŸŒ": "🌐",
    "ðŸ”’": "🔒",
    "ðŸ”„": "🔄",
    "ðŸ§ª": "🧪",
    "âœ…": "✅",
    "âš": "⚠️",
    "ðŸ›¡ï¸": "🛡️",
    "ï¸": "️",
    "â¶": "▶",
    "â—€": "◀",
    "ðŸ“Š": "📊",
    "ðŸ Æ": "⚙",
    "ðŸ‘": "👁",
    "ðŸ“": "📁",
}

for k, v in replacements_single.items():
    content = content.replace(k, v)

with open('gui.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Limpeza aplicada!")
