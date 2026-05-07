import customtkinter as ctk

# --- PALETA DE CORES APEX HUD ---
C = {
    "bg": "#080B0F",         # Fundo principal muito escuro, quase abissal
    "panel": "#0B1015",      # Fundo de painéis/sidebar
    "card": "#10151B",       # Fundo dos cards interativos
    "card_light": "#1E293B", # Azul um pouco mais claro para destaque
    "border": "#1E2631",     # Bordas e separadores sutis
    "accent": "#00FF88",     # Verde ciberneon para ações de sucesso/status ativo
    "hover": "#162B20",      # Hover sutil esverdeado para botões
    "cyan": "#00CCFF",       # Ciano neon para informações e títulos secundários
    "text": "#E2E8F0",       # Texto principal (slate-200)
    "muted": "#64748B",      # Texto secundário (slate-500)
    "gold": "#FFD700",       # Ouro para Modo Deus e features premium
    "red": "#FF3366",        # Vermelho intenso para alertas ou modo perigoso
    "orange": "#FF8C00"      # Laranja para simulação e alertas intermediários
}

def get_fonts():
    """ Retorna um dicionário com as fontes padrão do sistema. """
    return {
        "title": ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
        "label": ctk.CTkFont(family="Segoe UI", size=12),
        "log": ctk.CTkFont(family="Consolas", size=10),
        "section": ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
        "sub": ctk.CTkFont(family="Segoe UI", size=12),
        "tab_btn": ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        "card_title": ctk.CTkFont("Segoe UI", 10, "bold"),
        "stat_val": ctk.CTkFont("Segoe UI", 14, "bold"),
        "small_bold": ctk.CTkFont("Segoe UI", 9, "bold"),
        "label_small": ctk.CTkFont("Segoe UI", 10),
        "label_italic": ctk.CTkFont("Segoe UI", 10, slant="italic")
    }
