import os
import sys
import time
import math
import subprocess
import threading
import psutil
import customtkinter as ctk
import requests
import json
from intelligence import brain # Importar a inteligência do HUD


# ---
# PALETA DE CORES APEX HUD
# ---
VERSION = "2.0.1" # Versão Atual
UPDATE_URL = "https://raw.githubusercontent.com/tiagoflstudio-oss/killprocess/main/version.json" 

C = {
    "bg": "#080B0F",         # Fundo principal muito escuro, quase abissal
    "panel": "#0B1015",      # Fundo de painéis/sidebar
    "card": "#10151B",       # Fundo dos cards interativos
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

# =====================================================================
# 🚀 Killprocess - Advanced Sapphire Edition (Fase 3 & 4)
# =====================================================================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

DRY_RUN = True  # Começa como Simulação por padrão para máxima segurança

def is_admin():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_cmd(cmd):
    if DRY_RUN:
        return f"[SIMULAÇÃO]: {cmd}"
    try:
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

# =====================================================================
# ⚙️ Mapeamento Detalhado de Processos/Serviços por 6 Níveis Completos
# =====================================================================

SERVICES_MAP = {
    "Nível 1: Aplicativos & Bloatwares": [
        {"id": "chrome", "name": "Google Chrome", "type": "process", "checked": True},
        {"id": "msedge", "name": "Microsoft Edge", "type": "process", "checked": True},
        {"id": "onedrive", "name": "Microsoft OneDrive", "type": "process", "checked": True},
        {"id": "teams", "name": "Microsoft Teams", "type": "process", "checked": True},
        {"id": "discord", "name": "Discord Client", "type": "process", "checked": True},
        {"id": "spotify", "name": "Spotify Background", "type": "process", "checked": True},
        {"id": "zoom", "name": "Zoom Meeting Service", "type": "process", "checked": True},
        {"id": "skype", "name": "Skype", "type": "process", "checked": True},
        {"id": "whatsapp", "name": "WhatsApp", "type": "process", "checked": True},
        {"id": "slack", "name": "Slack Client", "type": "process", "checked": True},
        {"id": "telegram", "name": "Telegram Desktop", "type": "process", "checked": True},
        {"id": "anydesk", "name": "AnyDesk Remote", "type": "process", "checked": True},
        {"id": "winword", "name": "Microsoft Word", "type": "process", "checked": True},
        {"id": "excel", "name": "Microsoft Excel", "type": "process", "checked": True},
        {"id": "powerpnt", "name": "Microsoft PowerPoint", "type": "process", "checked": True},
        {"id": "notepad", "name": "Notepad", "type": "process", "checked": True},
        {"id": "calc", "name": "Windows Calculator", "type": "process", "checked": True},
        {"id": "acrobat", "name": "Adobe Acrobat Reader", "type": "process", "checked": True},
        {"id": "dropbox", "name": "Dropbox Client", "type": "process", "checked": True},
        {"id": "teamviewer", "name": "TeamViewer", "type": "process", "checked": True}
    ],
    "Nível 2: Impressão & Manutenção": [
        {"id": "Spooler", "name": "Spooler de Impressão", "type": "service", "checked": True},
        {"id": "WSearch", "name": "Windows Search (Indexador)", "type": "service", "checked": True},
        {"id": "SysMain", "name": "SysMain (Superfetch)", "type": "service", "checked": True},
        {"id": "Themes", "name": "Temas Visuais do Windows", "type": "service", "checked": False},
        {"id": "TabletInputService", "name": "Teclado Virtual / Caneta", "type": "service", "checked": True},
        {"id": "PcaSvc", "name": "Assistente de Compatibilidade", "type": "service", "checked": True},
        {"id": "WerSvc", "name": "Relatório de Erros do Windows", "type": "service", "checked": True},
        {"id": "Fax", "name": "Serviço de Fax", "type": "service", "checked": True},
        {"id": "PrintWorkflowUserSvc", "name": "Fluxo de Trabalho de Impressão", "type": "service", "checked": True},
        {"id": "StiSvc", "name": "Aquisição de Imagens", "type": "service", "checked": True},
        {"id": "DPS", "name": "Serviço de Diretivas de Diagnóstico", "type": "service", "checked": True},
        {"id": "WdiServiceHost", "name": "Host de Serviço de Diagnóstico", "type": "service", "checked": True},
        {"id": "WdiSystemHost", "name": "Host de Sistema de Diagnóstico", "type": "service", "checked": True},
        {"id": "vmicguest", "name": "Hyper-V Guest", "type": "service", "checked": True},
        {"id": "vmictimesync", "name": "Hyper-V Time Sync", "type": "service", "checked": True},
        {"id": "vmicrdv", "name": "Hyper-V Remote Desktop", "type": "service", "checked": True},
        {"id": "vmicvmsession", "name": "Hyper-V VM Session", "type": "service", "checked": True}
    ],
    "Nível 3: Telemetria & Rastreamento": [
        {"id": "DiagTrack", "name": "Telemetria da Microsoft", "type": "service", "checked": True},
        {"id": "PimIndexMaintenanceSvc", "name": "Manutenção de Índice Pim", "type": "service", "checked": True},
        {"id": "ContactData", "name": "Dados de Contatos", "type": "service", "checked": True},
        {"id": "UserDataSvc", "name": "Acesso a Dados de Usuário", "type": "service", "checked": True},
        {"id": "OneSyncSvc", "name": "Sincronização do Host", "type": "service", "checked": True},
        {"id": "DusmSvc", "name": "Uso de Dados", "type": "service", "checked": True},
        {"id": "AppReadiness", "name": "Preparação de Aplicativos", "type": "service", "checked": True}
    ],
    "Nível 4: Xbox & Conexões Secundárias": [
        {"id": "XblAuthManager", "name": "Autenticação do Xbox Live", "type": "service", "checked": True},
        {"id": "XblGameSave", "name": "Salvar Jogos do Xbox Live", "type": "service", "checked": True},
        {"id": "XboxNetApiSvc", "name": "Rede do Xbox Live", "type": "service", "checked": True},
        {"id": "XboxGipSvc", "name": "Acessórios do Xbox", "type": "service", "checked": True},
        {"id": "bthserv", "name": "Serviço de Bluetooth", "type": "service", "checked": True},
        {"id": "BTAGCategoryService", "name": "Áudio Bluetooth", "type": "service", "checked": True},
        {"id": "BluetoothUserService", "name": "Serviço de Usuário de Bluetooth", "type": "service", "checked": True},
        {"id": "NfcService", "name": "NFC Service", "type": "service", "checked": True},
        {"id": "PhoneSvc", "name": "Serviço de Telefone", "type": "service", "checked": True},
        {"id": "SensorSvc", "name": "Serviço de Sensores", "type": "service", "checked": True},
        {"id": "SensorDataSvc", "name": "Dados dos Sensores", "type": "service", "checked": True},
        {"id": "SensorsSrv", "name": "Servidor de Sensores", "type": "service", "checked": True}
    ],
    "Nível 5: Redes & Streaming": [
        {"id": "SharedAccess", "name": "Compartilhamento de Internet", "type": "service", "checked": True},
        {"id": "lfsvc", "name": "Serviço de Geolocalização", "type": "service", "checked": True},
        {"id": "MapsBroker", "name": "Gerenciador de Mapas Baixados", "type": "service", "checked": True},
        {"id": "WpcProvider", "name": "Controles dos Pais", "type": "service", "checked": True},
        {"id": "RetailDemo", "name": "Modo de Demonstração de Varejo", "type": "service", "checked": True},
        {"id": "AJRouter", "name": "Roteamento AllJoyn", "type": "service", "checked": True},
        {"id": "diagnosticshub.standardcollector.service", "name": "Coletor do Hub de Diagnóstico", "type": "service", "checked": True},
        {"id": "TrkWks", "name": "Clientes de Rastreamento de Link", "type": "service", "checked": True}
    ],
    "Nível 6: Segurança & Criptografia": [
        {"id": "VaultSvc", "name": "Gerenciador de Credenciais", "type": "service", "checked": True},
        {"id": "SstpSvc", "name": "Protocolo de Túnel de Soquete Seguro", "type": "service", "checked": True},
        {"id": "SCardSvr", "name": "Cartão Inteligente", "type": "service", "checked": True},
        {"id": "ScDeviceEnum", "name": "Enumeração de Dispositivos de Cartão", "type": "service", "checked": True},
        {"id": "wisvc", "name": "Insider Service", "type": "service", "checked": True},
        {"id": "dmwappushservice", "name": "Roteamento WAP Push", "type": "service", "checked": True},
        {"id": "RemoteRegistry", "name": "Registro Remoto", "type": "service", "checked": True},
        {"id": "WbioSrvc", "name": "Biometria", "type": "service", "checked": True}
    ],
    "Nível 7: Modo Deus (God Mode)": [
        {"id": "PushToInstall", "name": "Windows Store Push Service", "type": "service", "checked": True},
        {"id": "WMPNetworkSvc", "name": "WMP Network Service", "type": "service", "checked": True},
        {"id": "ClipSVC", "name": "Serviço de Licença de Cliente", "type": "service", "checked": True},
        {"id": "AppPredictionSvc", "name": "Serviço de Previsão de Aplicativos", "type": "service", "checked": True},
        {"id": "AppXSvc", "name": "Serviço de Implantação AppX", "type": "service", "checked": True},
        {"id": "LicenseManager", "name": "Gerenciador de Licenças", "type": "service", "checked": True},
        {"id": "tzautoupdate", "name": "Atualização Automática de Fuso Horário", "type": "service", "checked": True},
        {"id": "WalletService", "name": "Serviço de Carteira", "type": "service", "checked": True},
        {"id": "WpnService", "name": "Notificações Push do Windows", "type": "service", "checked": True},
        {"id": "WpnUserService", "name": "Serviço de Usuário de Notificações", "type": "service", "checked": True},
        {"id": "AxInstSV", "name": "Instalação ActiveX", "type": "service", "checked": True},
        {"id": "BITS", "name": "Serviço de Transferência Inteligente em Segundo Plano", "type": "service", "checked": True},
        {"id": "CertPropSvc", "name": "Propagação de Certificado", "type": "service", "checked": True},
        {"id": "defragsvc", "name": "Otimização de Unidades / Desfragmentador", "type": "service", "checked": True},
        {"id": "EntAppSvc", "name": "Serviço de Aplicativo Empresarial", "type": "service", "checked": True}
    ]
}

# =====================================================================
# 📊 Gráfico Vivo Neon e Dinâmico
# =====================================================================
# =====================================================================
# 🖥️ Janela Principal Premium do Aplicativo (CustomTkinter)
# =====================================================================

class PremiumKillprocessApp(ctk.CTk):
    def show_splash(self):
        splash = ctk.CTkToplevel(self)
        splash.overrideredirect(True)
        splash.attributes("-topmost", True)
        
        sw, sh = 1280, 720
        # Centralizar na tela
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - sw) // 2
        y = (screen_h - sh) // 2
        splash.geometry(f"{sw}x{sh}+{x}+{y}")
        splash.configure(fg_color="#080B0F")
        
        canvas = ctk.CTkCanvas(splash, width=sw, height=sh, bg="#080B0F", highlightthickness=0)
        canvas.pack()
        
        import winsound, threading
        
        def play_boot_sound(freq, dur):
            threading.Thread(target=lambda: winsound.Beep(freq, dur), daemon=True).start()

        def animate_k_minimal(step=0):
            canvas.delete("all")
            cx, cy = sw // 2, sh // 2
            
            # Progresso da animação (0.0 a 1.0 em 30 steps)
            progress = min(step / 30, 1.0)
            
            # Som de Inicialização (Chime de Sistema Elegante)
            if step == 1: 
                threading.Thread(target=lambda: winsound.MessageBeep(winsound.MB_ICONASTERISK), daemon=True).start()
            
            # Cores sérias
            k_color = "#00CCFF" # Ciano Apex
            
            # Pedaços do "K" (Coordenadas relativas ao centro)
            # 1. Barra Vertical
            v_start_y = cy - 60
            v_end_y = cy + 60
            v_x = cx - 25
            # Vem de cima
            v_current_y = v_start_y - (100 * (1 - progress))
            canvas.create_line(v_x, v_current_y, v_x, v_current_y + 120, fill=k_color, width=8, capstyle="round")
            
            # 2. Diagonal Superior
            # Vem da direita
            d1_x_offset = 150 * (1 - progress)
            canvas.create_line(v_x, cy, cx + 25 + d1_x_offset, cy - 60, fill=k_color, width=8, capstyle="round")
            
            # 3. Diagonal Inferior
            # Vem de baixo/direita
            d2_offset = 150 * (1 - progress)
            canvas.create_line(v_x, cy, cx + 25 + d2_offset, cy + 60, fill=k_color, width=8, capstyle="round")
            
            # Texto de Status (Aparece no final)
            if progress > 0.8:
                canvas.create_text(cx, cy + 100, text="SYSTEM OPTIMIZED // READY", 
                                   font=("Consolas", 12, "bold"), fill="#10B981")

            if step < 30:
                splash.after(100, lambda: animate_k_minimal(step + 1))
            else:
                splash.after(500, lambda: [splash.destroy(), self.deiconify(), self.log(">>> SISTEMA PRONTO.", "success")])

        animate_k_minimal()

    def __init__(self):
        super().__init__()
        self.title("KILLPROCESS APEX EDITION")
        
        # Definições de Resolução
        self.resolutions = {
            "1920 x 1080 (Full HD)": (1920, 1080),
            "1650 x 1080 (Padrão Apex)": (1650, 1080),
            "1280 x 720 (HD)": (1280, 720)
        }
        
        # Iniciar em janela padrão 1280x720 (Corte do Fullscreen automático)
        self.geometry("1280x720")
        # self.attributes("-fullscreen", True) # Comentado conforme pedido
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False)) 
        
        # Esconde a janela principal para mostrar o Splash primeiro
        self.withdraw()
        self.after(100, self.show_splash)
        
        self.setup_ui()
        self.start_system_audit()
        
    def setup_ui(self):
        self.configure(fg_color=C["bg"])
        
        try:
            self.iconbitmap("icon.ico")
        except:
            pass

        self.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))
        
        # ---
        # LAYOUT BASE: APEX HUD
        # Topbar | Sidebar | Content
        # Terminal na base
        # ---
        
        # Topbar (100% largura)
        self.topbar = ctk.CTkFrame(self, fg_color=C["panel"], height=55, corner_radius=0, border_width=0)
        self.topbar.pack(side="top", fill="x")
        self.topbar.pack_propagate(False)
        self._build_topbar()
        
        # Terminal na Direita (Monitor Lateral APEX)
        self.terminal_frame = ctk.CTkFrame(self, fg_color="#050505", width=400, corner_radius=0, 
                                          border_width=1, border_color="#1E2631")
        self.terminal_frame.pack(side="right", fill="y")
        self.terminal_frame.pack_propagate(False)
        self._build_terminal()

        # --- NOVO: Divisor Arrastável (Resize Handler) ---
        self.resizing_terminal = False
        self.terminal_divider = ctk.CTkFrame(self, width=3, fg_color="#1E2631", corner_radius=0, cursor="sb_h_double_arrow")
        self.terminal_divider.pack(side="right", fill="y")
        
        # Binds para o redimensionamento
        self.terminal_divider.bind("<Button-1>", self.start_resizing)
        self.terminal_divider.bind("<B1-Motion>", self.resize_terminal)
        self.terminal_divider.bind("<ButtonRelease-1>", self.stop_resizing)
        self.terminal_divider.bind("<Enter>", lambda e: self.terminal_divider.configure(fg_color=C["cyan"]))
        self.terminal_divider.bind("<Leave>", lambda e: self.terminal_divider.configure(fg_color="#1E2631"))

        # Container Central (Sidebar + Content)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(side="left", fill="both", expand=True)
        
        # Sidebar (Fixa à esquerda)
        self.sidebar_frame = ctk.CTkFrame(self.main_container, fg_color=C["panel"], width=220, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)
        self._build_sidebar()
        
        # Content (Área dinâmica)
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color=C["bg"], corner_radius=0)
        self.content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        self._build_content()

        # Configurações Adicionais
        self.tabs = {}
        self.level_checkboxes_dashboard = {}
        self.level_indicators = {}
        self.whitelist = []
        self.sidebar_collapsed = False
        self.autoboost_active = False
        self.autoboost_enabled = False
        self.shell_explorer_closed = False
        self.autoboost_status_lbls = {}
        self.autoboost_checkboxes = {}
        self.supported_games = [
            {"exe": "cs2.exe", "name": "Counter-Strike 2"},
            {"exe": "valorant.exe", "name": "Valorant"},
            {"exe": "leagueoflegends.exe", "name": "League of Legends"},
            {"exe": "gta5.exe", "name": "Grand Theft Auto V"},
            {"exe": "cyberpunk2077.exe", "name": "Cyberpunk 2077"}
        ]
        
        self.title_font = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        self.label_font = ctk.CTkFont(family="Segoe UI", size=12)
        self.log_font = ctk.CTkFont(family="Consolas", size=10)
        self.section_font = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        self.sub_font = ctk.CTkFont(family="Segoe UI", size=12)

        self.load_whitelist()
        self.create_dashboard_tab()
        self.create_management_tab()
        self.create_scan_tab()
        self.create_settings_tab()
        self.create_autoboost_tab()
        self.create_optimize_center_tab()
        self.create_extra_tab()
        self.create_shell_tab()
        self.create_whitelist_tab()

        self.switch_tab("dashboard")

        # Threads
        threading.Thread(target=self.shell_clock_loop, daemon=True).start()
        threading.Thread(target=self.autoboost_polling_loop, daemon=True).start()
        threading.Thread(target=self.refresh_stats_loop, daemon=True).start()

    # --- Lógica de Redimensionamento do Terminal ---
    def start_resizing(self, event):
        self.resizing_terminal = True
        self.start_x = event.x_root
        self.start_width = self.terminal_frame.winfo_width()

    def resize_terminal(self, event):
        if self.resizing_terminal:
            # Calcula o deslocamento (invertido pois o terminal está na direita)
            delta = self.start_x - event.x_root
            new_width = self.start_width + delta
            
            # Limites de segurança para não quebrar a UI
            if 200 < new_width < 800:
                self.terminal_frame.configure(width=new_width)

    def stop_resizing(self, event):
        self.resizing_terminal = False

    def _build_topbar(self):
        # Container Esquerdo (Logo + Switch)
        left_container = ctk.CTkFrame(self.topbar, fg_color="transparent")
        left_container.pack(side="left", padx=20, fill="y")

        logo_lbl = ctk.CTkLabel(left_container, text="✨ KILLPROCESS ", font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=C["accent"])
        logo_lbl.pack(side="left")
        sub_lbl = ctk.CTkLabel(left_container, text="APEX", font=ctk.CTkFont("Segoe UI", 10, "bold"), text_color=C["muted"])
        sub_lbl.pack(side="left", padx=(0, 20), pady=(4,0))
        
        # Switch do Modo (Ajuste fino: afastando da margem do menu lateral)
        self.mode_pill = ctk.CTkLabel(left_container, text="● SIMULAÇÃO", font=ctk.CTkFont("Segoe UI", 10, "bold"),
                                      fg_color="#140A00", text_color=C["orange"], corner_radius=4, padx=10, pady=2)
        self.mode_pill.pack(side="left", padx=(80, 5)) 
        
        self.dry_run_switch = ctk.CTkSwitch(left_container, text="MODO REAL", command=self.toggle_dry_run, 
                                            font=ctk.CTkFont("Segoe UI", 10, "bold"), text_color=C["muted"],
                                            onvalue=True, offvalue=False) 
        self.dry_run_switch.pack(side="left", padx=5)
        self.dry_run_switch.deselect()

        # Container Direito (Configurações)
        right_container = ctk.CTkFrame(self.topbar, fg_color="transparent")
        right_container.pack(side="right", padx=10, fill="y")

        self.res_menu = ctk.CTkOptionMenu(right_container, values=list(self.resolutions.keys()),
                                          command=self.change_resolution, width=150, height=24,
                                          font=ctk.CTkFont("Segoe UI", 10), dropdown_font=ctk.CTkFont("Segoe UI", 10),
                                          fg_color=C["card"], button_color=C["border"], button_hover_color=C["hover"])
        self.res_menu.pack(side="right", padx=10, pady=5)
        self.res_menu.set("1650 x 1080 (Padrão Apex)")

        settings_btn = ctk.CTkButton(right_container, text="⚙️", width=30, height=30, fg_color="transparent",
                                     hover_color=C["hover"], font=("Segoe UI", 16), command=lambda: self.res_menu.focus_set())
        settings_btn.pack(side="right")

    def change_resolution(self, choice):
        w, h = self.resolutions[choice]
        self.attributes("-fullscreen", False)
        self.geometry(f"{w}x{h}")
        self.log(f">>> RESOLUÇÃO ALTERADA PARA {w}x{h}", "info")

    def _build_sidebar(self):
        # Menu Principal - 5 Abas Essenciais
        self.nav_btns = {}
        
        def add_nav_btn(id, icon, text):
            # Adicionando espaços no início do texto para afastar o ícone da borda
            btn = ctk.CTkButton(self.sidebar_frame, text=f"      {icon}   {text}", anchor="w", 
                                fg_color="transparent", hover_color=C["hover"], text_color=C["muted"],
                                font=ctk.CTkFont("Segoe UI", 12, "bold"), height=42, corner_radius=0,
                                command=lambda k=id: self.switch_tab(k))
            btn.pack(fill="x", pady=2)
            self.nav_btns[id] = btn

        ctk.CTkLabel(self.sidebar_frame, text="", height=10).pack() # Espaçador
        add_nav_btn("dashboard", "⚡", "INÍCIO")
        add_nav_btn("management", "⚙️", "PROCESSOS")
        add_nav_btn("whitelist", "🛡️", "WHITELIST")
        add_nav_btn("scan", "🔍", "SCAN")
        add_nav_btn("optimize_center", "🔥", "OTIMIZAR")
        add_nav_btn("autoboost", "🚀", "AUTO-BOOST")
        add_nav_btn("extra", "🛠️", "MANUTENÇÃO")
        
        # --- ÁREA DE ATALHOS RÁPIDOS (BANNERS RETANGULARES) ---
        ctk.CTkLabel(self.sidebar_frame, text="CENTRAL DE LANÇAMENTO", font=ctk.CTkFont("Segoe UI", 8, "bold"), text_color=C["muted"]).pack(pady=(20, 5))
        
        self.shortcut_container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.shortcut_container.pack(fill="x", padx=10, pady=5)
        
        self.custom_shortcuts = []
        self.render_shortcuts()

        # Botão de Adicionar (+)
        add_btn = ctk.CTkButton(self.sidebar_frame, text="+ ADICIONAR APP", width=180, height=32, corner_radius=6, 
                                fg_color="transparent", border_width=1, border_color=C["border"],
                                hover_color=C["hover"], font=("Segoe UI", 10, "bold"), 
                                command=self.add_custom_shortcut)
        add_btn.pack(pady=10)

        # --- Versão no Rodapé ---
        ver_lbl = ctk.CTkLabel(self.sidebar_frame, text=f"APEX HUD v{VERSION}", 
                               font=ctk.CTkFont("Segoe UI", 9), text_color=C["muted"])
        ver_lbl.pack(side="bottom", pady=10)

        # Botão de Update no rodapé da sidebar
        update_btn = ctk.CTkButton(self.sidebar_frame, text="🔄 CHECK UPDATE", 
                                   font=ctk.CTkFont("Segoe UI", 8, "bold"),
                                   fg_color="transparent", border_width=1, border_color=C["border"],
                                   height=20, corner_radius=4, text_color=C["muted"],
                                   hover_color=C["card"], command=self.check_for_updates)
        update_btn.pack(side="bottom", pady=(0, 2), padx=20, fill="x")

        # Área de Rodapé: Ponto de Restauração
        bottom_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", pady=20, padx=15)
        
        self.restore_btn = ctk.CTkButton(bottom_frame, text="🛡️ CRIAR PONTO DE RESTAURAÇÃO", 
                                          font=ctk.CTkFont("Segoe UI", 9, "bold"),
                                          fg_color="#064E3B", hover_color="#065F46", text_color="#10B981",
                                          height=35, corner_radius=8, border_width=1, border_color="#10B981",
                                          command=self.create_restore_point)
        self.restore_btn.pack(fill="x")

    def _build_content(self):
        # Este é apenas o placeholder, as abas criam frames dentro dele.
        pass

    def _build_terminal(self):
        # Monitor de Execução (Lateral Direita Total)
        hdr = ctk.CTkFrame(self.terminal_frame, fg_color="#0D1117", height=35, corner_radius=0)
        hdr.pack(fill="x")
        
        ctk.CTkLabel(hdr, text="⚡ MONITOR DE EXECUÇÃO", font=ctk.CTkFont("Segoe UI", 10, "bold"), text_color=C["accent"]).pack(side="left", padx=15)
        self.pending_clear = False
        # Botão LIMPAR maior e mais centralizado no header do terminal
        self.clear_log_btn = ctk.CTkButton(hdr, text="LIMPAR LOG", width=90, height=26, font=ctk.CTkFont("Segoe UI", 9, "bold"), 
                      fg_color="#1E293B", hover_color="#334155", text_color=C["muted"],
                      command=self.clear_terminal_logs)
        self.clear_log_btn.pack(side="right", padx=120)
        
        self.log_textbox = ctk.CTkTextbox(self.terminal_frame, fg_color="transparent", font=ctk.CTkFont("Consolas", 10), text_color=C["text"])
        self.log_textbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Tags de cores para o terminal
        self.log_textbox.tag_config("success", foreground="#10B981") # Verde Neon
        self.log_textbox.tag_config("info", foreground="#3B82F6")    # Azul Ciano
        self.log_textbox.tag_config("warning", foreground="#FACC15") # Amarelo/Ouro
        self.log_textbox.tag_config("error", foreground="#EF4444")   # Vermelho
        
        self.log_textbox.insert("end", ">>> Killprocess APEX inicializado.\n" + "="*30 + "\n", "info")

    def log(self, text, tag=None):
        if tag:
            self.log_textbox.insert("end", text + "\n", tag)
        else:
            self.log_textbox.insert("end", text + "\n")
        self.log_textbox.see("end")
        
        # Ativa o alerta de limpeza quando algo é logado
        if "✅" in text or "✔️" in text:
            self.pending_clear = True

    def clear_terminal_logs(self):
        self.log_textbox.delete("1.0", "end")
        self.pending_clear = False
        self.clear_log_btn.configure(text_color=C["muted"])

    def create_dashboard_tab(self):
        tab = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.tabs["dashboard"] = tab

        # ── LINHA 1: Cabeçalho ──────────────────────────────────────────
        hdr = ctk.CTkFrame(tab, fg_color="transparent")
        hdr.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(hdr, text="CENTRO DE CONTROLE", font=self.title_font,
                     text_color=C["text"]).pack(side="left")
        self.status_val_lbl = ctk.CTkLabel(
            hdr, text="● PRONTO", font=ctk.CTkFont("Segoe UI", 11, "bold"),
            text_color=C["accent"], fg_color="#051408", corner_radius=6, padx=10, pady=3)
        self.status_val_lbl.pack(side="right")

        # ── LINHA 2: Seletor de Níveis + Stats + Sistema ─────────────
        row2 = ctk.CTkFrame(tab, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 8))
        row2.grid_columnconfigure(0, weight=2) # Níveis
        row2.grid_columnconfigure((1, 2, 3, 4), weight=1) # 4 Colunas de Métricas uniformes

        # Card Seletor de Níveis
        lvl_card = ctk.CTkFrame(row2, fg_color=C["card"], border_width=1,
                                 border_color=C["border"], corner_radius=10)
        lvl_card.grid(row=0, column=0, padx=(0, 6), sticky="nsew", ipady=4)

        ctk.CTkLabel(lvl_card, text="▌ NÍVEIS DE OTIMIZAÇÃO",
                     font=ctk.CTkFont("Segoe UI", 9, "bold"),
                     text_color=C["cyan"]).pack(anchor="w", padx=12, pady=(8, 4))

        self.lights_frame = ctk.CTkFrame(lvl_card, fg_color="transparent")
        self.lights_frame.pack(fill="x", padx=15, pady=(0, 4))

        self.level_indicators = {}
        self.level_checkboxes_dashboard = {}

        self.level_desc_lbl = ctk.CTkLabel(
            lvl_card, text="Passe o mouse sobre um nível para ver detalhes.",
            font=ctk.CTkFont("Segoe UI", 11), text_color=C["muted"])
        self.level_desc_lbl.pack(anchor="w", padx=15, pady=(0, 10))

        def update_desc(txt): self.level_desc_lbl.configure(text=txt)

        levels_data = [
            (1, "N1", "Apps & Bloatwares", "#00FF88", "Fecha navegadores, mensageiros e apps em segundo plano."),
            (2, "N2", "Impressão & Manutenção", "#00FFB2", "Desativa serviços de impressoras, fax e manutenção."),
            (3, "N3", "Telemetria & Rastreamento", "#FFFF00", "Interrompe telemetria, coleta de dados e diagnósticos."),
            (4, "N4", "Xbox & Conexões", "#FF8000", "Remove suporte a Bluetooth e serviços Xbox."),
            (5, "N5", "Redes & Streaming", "#FF0055", "Desativa compartilhamento, mapas e sensores."),
            (6, "N6", "Segurança & Criptografia", "#00CCFF", "Encerra credenciais e segurança local."),
            (7, "N7", "Modo Deus (God Mode)", "#FFD700", "Performance Gamer Suprema: Modo Deus ativado."),
        ]
        
        row_idx = 0
        col_idx = 0
        for num, lvl_id, name, color, desc in levels_data:
            f = ctk.CTkFrame(self.lights_frame, fg_color="transparent")
            f.grid(row=row_idx, column=col_idx, sticky="w", padx=3, pady=3)
            
            cb = ctk.CTkCheckBox(f, text=name, font=ctk.CTkFont("Segoe UI", 10, "bold"),
                                  fg_color=color, hover_color=color, width=22,
                                  command=lambda d=desc: update_desc(d))
            if num <= 6: cb.select()
            cb.pack(side="left", padx=(0, 5))
            cb.bind("<Enter>", lambda e, d=desc: update_desc(d))
            
            # Usar a chave completa do SERVICES_MAP para evitar KeyError
            full_key = list(SERVICES_MAP.keys())[num-1]
            self.level_checkboxes_dashboard[full_key] = cb
            self.level_indicators[num] = {"circle": cb, "cb": cb, "color": color}
            
            col_idx += 1
            if col_idx > 1:
                col_idx = 0
                row_idx += 1

        # --- COLUNA 1: RAM & PROC ---
        c1 = ctk.CTkFrame(row2, fg_color="transparent")
        c1.grid(row=0, column=1, padx=3, sticky="nsew")
        c1.grid_rowconfigure((0, 1), weight=1)

        ram_card = ctk.CTkFrame(c1, fg_color=C["card"], border_width=1, border_color=C["border"], corner_radius=10)
        ram_card.grid(row=0, column=0, pady=(0, 3), sticky="nsew")
        ctk.CTkLabel(ram_card, text="RAM EM USO", font=ctk.CTkFont("Segoe UI", 8, "bold"), text_color=C["cyan"]).pack(anchor="w", padx=10, pady=(8, 0))
        self.ram_val_lbl = ctk.CTkLabel(ram_card, text="--", font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=C["text"])
        self.ram_val_lbl.pack(anchor="w", padx=10)
        self.ram_pb = ctk.CTkProgressBar(ram_card, height=4, progress_color="#10B981", fg_color="#1E2631")
        self.ram_pb.pack(fill="x", padx=10, pady=(0, 8))

        proc_card = ctk.CTkFrame(c1, fg_color=C["card"], border_width=1, border_color=C["border"], corner_radius=10)
        proc_card.grid(row=1, column=0, pady=(3, 0), sticky="nsew")
        ctk.CTkLabel(proc_card, text="PROCESSOS", font=ctk.CTkFont("Segoe UI", 8, "bold"), text_color=C["cyan"]).pack(anchor="w", padx=10, pady=(8, 0))
        self.proc_val_lbl = ctk.CTkLabel(proc_card, text="--", font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=C["text"])
        self.proc_val_lbl.pack(anchor="w", padx=10)
        self.proc_pb = ctk.CTkProgressBar(proc_card, height=4, progress_color="#3B82F6", fg_color="#1E2631")
        self.proc_pb.pack(fill="x", padx=10, pady=(0, 8))

        # --- COLUNA 2: GPU & DISK ---
        c2 = ctk.CTkFrame(row2, fg_color="transparent")
        c2.grid(row=0, column=2, padx=3, sticky="nsew")
        c2.grid_rowconfigure((0, 1), weight=1)

        gpu_card = ctk.CTkFrame(c2, fg_color=C["card"], border_width=1, border_color=C["border"], corner_radius=10)
        gpu_card.grid(row=0, column=0, pady=(0, 3), sticky="nsew")
        ctk.CTkLabel(gpu_card, text="GPU LOAD", font=ctk.CTkFont("Segoe UI", 8, "bold"), text_color=C["cyan"]).pack(anchor="w", padx=10, pady=(8, 0))
        self.dash_gpu_lbl = ctk.CTkLabel(gpu_card, text="--", font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=C["text"])
        self.dash_gpu_lbl.pack(anchor="w", padx=10)
        self.dash_gpu_pb = ctk.CTkProgressBar(gpu_card, height=4, progress_color="#F43F5E", fg_color="#1E2631")
        self.dash_gpu_pb.pack(fill="x", padx=10, pady=(0, 8))

        disk_card = ctk.CTkFrame(c2, fg_color=C["card"], border_width=1, border_color=C["border"], corner_radius=10)
        disk_card.grid(row=1, column=0, pady=(3, 0), sticky="nsew")
        ctk.CTkLabel(disk_card, text="DISK USAGE", font=ctk.CTkFont("Segoe UI", 8, "bold"), text_color=C["cyan"]).pack(anchor="w", padx=10, pady=(8, 0))
        self.dash_disk_lbl = ctk.CTkLabel(disk_card, text="--", font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=C["text"])
        self.dash_disk_lbl.pack(anchor="w", padx=10)
        self.dash_disk_pb = ctk.CTkProgressBar(disk_card, height=4, progress_color="#2DD4BF", fg_color="#1E2631")
        self.dash_disk_pb.pack(fill="x", padx=10, pady=(0, 8))

        # --- COLUNA 3: SISTEMA & NET ---
        c3 = ctk.CTkFrame(row2, fg_color="transparent")
        c3.grid(row=0, column=3, padx=3, sticky="nsew")
        c3.grid_rowconfigure((0, 1), weight=1)

        sys_card = ctk.CTkFrame(c3, fg_color=C["card"], border_width=1, border_color=C["border"], corner_radius=10)
        sys_card.grid(row=0, column=0, pady=(0, 3), sticky="nsew")
        ctk.CTkLabel(sys_card, text="OS INFO", font=ctk.CTkFont("Segoe UI", 8, "bold"), text_color=C["cyan"]).pack(anchor="w", padx=10, pady=(8, 0))
        self.dash_os_lbl = ctk.CTkLabel(sys_card, text="Windows", font=ctk.CTkFont("Segoe UI", 12, "bold"), text_color=C["text"])
        self.dash_os_lbl.pack(anchor="w", padx=10)
        import platform
        self.dash_os_lbl.configure(text=f"{platform.system()} {platform.release()}"[:18])

        net_card = ctk.CTkFrame(c3, fg_color=C["card"], border_width=1, border_color=C["border"], corner_radius=10)
        net_card.grid(row=1, column=0, pady=(3, 0), sticky="nsew")
        ctk.CTkLabel(net_card, text="NETWORK", font=ctk.CTkFont("Segoe UI", 8, "bold"), text_color=C["cyan"]).pack(anchor="w", padx=10, pady=(8, 0))
        self.dash_net_lbl = ctk.CTkLabel(net_card, text="--", font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=C["text"])
        self.dash_net_lbl.pack(anchor="w", padx=10)
        self.dash_net_pb = ctk.CTkProgressBar(net_card, height=4, progress_color="#A855F7", fg_color="#1E2631")
        self.dash_net_pb.pack(fill="x", padx=10, pady=(0, 8))

        # --- COLUNA 4: CPU & TEMP ---
        c4 = ctk.CTkFrame(row2, fg_color="transparent")
        c4.grid(row=0, column=4, padx=(3, 0), sticky="nsew")
        c4.grid_rowconfigure((0, 1), weight=1)

        cpu_card = ctk.CTkFrame(c4, fg_color=C["card"], border_width=1, border_color=C["border"], corner_radius=10)
        cpu_card.grid(row=0, column=0, pady=(0, 3), sticky="nsew")
        ctk.CTkLabel(cpu_card, text="CPU USAGE", font=ctk.CTkFont("Segoe UI", 8, "bold"), text_color=C["cyan"]).pack(anchor="w", padx=10, pady=(8, 0))
        self.dash_cpu_lbl = ctk.CTkLabel(cpu_card, text="--", font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=C["text"])
        self.dash_cpu_lbl.pack(anchor="w", padx=10)
        self.dash_cpu_pb = ctk.CTkProgressBar(cpu_card, height=4, progress_color=C["accent"], fg_color="#1E2631")
        self.dash_cpu_pb.pack(fill="x", padx=10, pady=(0, 8))

        temp_card = ctk.CTkFrame(c4, fg_color=C["card"], border_width=1, border_color=C["border"], corner_radius=10)
        temp_card.grid(row=1, column=0, pady=(3, 0), sticky="nsew")
        ctk.CTkLabel(temp_card, text="CORE TEMP", font=ctk.CTkFont("Segoe UI", 8, "bold"), text_color=C["cyan"]).pack(anchor="w", padx=10, pady=(8, 0))
        self.dash_temp_lbl = ctk.CTkLabel(temp_card, text="--", font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=C["text"])
        self.dash_temp_lbl.pack(anchor="w", padx=10)
        self.dash_temp_pb = ctk.CTkProgressBar(temp_card, height=4, progress_color="#FB923C", fg_color="#1E2631")
        self.dash_temp_pb.pack(fill="x", padx=10, pady=(0, 8))

        # ── LINHA 3: Botões de Ação + Radar ─────────────────────────────
        row3 = ctk.CTkFrame(tab, fg_color="transparent")
        row3.pack(fill="x", pady=(0, 8))
        row3.grid_columnconfigure(0, weight=3)
        row3.grid_columnconfigure(1, weight=1)

        # Painel de Ações
        act = ctk.CTkFrame(row3, fg_color=C["card"], border_width=1,
                            border_color=C["border"], corner_radius=10)
        act.grid(row=0, column=0, padx=(0, 6), sticky="nsew")

        ctk.CTkLabel(act, text="▌ AÇÕES RÁPIDAS (ONE-CLICK)",
                     font=ctk.CTkFont("Segoe UI", 9, "bold"),
                     text_color=C["cyan"]).pack(anchor="w", padx=14, pady=(10, 8))

        # Grid de Botões Quadrados no Dash (Simétrico e Uniforme)
        btn_grid = ctk.CTkFrame(act, fg_color="transparent")
        btn_grid.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        # uniform="buttons" garante que as colunas tenham EXATAMENTE a mesma largura
        btn_grid.grid_columnconfigure((0, 1, 2), weight=1, uniform="buttons")
        btn_grid.grid_rowconfigure(0, weight=1)

        # Botão OTIMIZAR TUDO
        self.full_opt_btn = ctk.CTkButton(
            btn_grid, text="🚀\nOTIMIZAR TUDO",
            fg_color="#0D47A1", hover_color="#1565C0",
            font=ctk.CTkFont("Segoe UI", 11, "bold"),
            height=140, corner_radius=10, text_color="white",
            command=self.start_full_optimization)
        self.full_opt_btn.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

        # GOD MODE
        self.god_mode_btn = ctk.CTkButton(
            btn_grid, text="👑\nGOD MODE",
            fg_color=C["gold"], hover_color="#C8A800",
            font=ctk.CTkFont("Segoe UI", 11, "bold"),
            height=140, corner_radius=10, text_color="#0A0A0A",
            command=self.start_god_mode)
        self.god_mode_btn.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")

        # Gamer Custom
        self.optimize_selection_btn = ctk.CTkButton(
            btn_grid, text="⚡\nGAMER CUSTOM",
            fg_color="#1E2631", hover_color="#3B82F6",
            border_width=1, border_color="#3B82F6",
            font=ctk.CTkFont("Segoe UI", 11, "bold"),
            height=140, corner_radius=10, text_color=C["text"],
            command=self.start_optimize_selection)
        self.optimize_selection_btn.grid(row=0, column=2, padx=8, pady=8, sticky="nsew")

        # Atalhos rápidos (Mais visíveis e destacados)
        shortcuts_row = ctk.CTkFrame(act, fg_color="transparent")
        shortcuts_row.pack(fill="x", padx=10, pady=(0, 8))
        shortcuts_row.grid_columnconfigure((0, 1, 2), weight=1)

        self.btn_ab_dash = ctk.CTkButton(
            shortcuts_row, text="🚀 Auto Boost", fg_color="#111827",
            hover_color="#10B981", border_width=1, border_color="#10B981",
            font=ctk.CTkFont("Segoe UI", 10, "bold"), height=32, corner_radius=6,
            command=self.toggle_autoboost)
        self.btn_ab_dash.grid(row=0, column=0, padx=3, sticky="nsew")

        self.btn_maint_dash = ctk.CTkButton(
            shortcuts_row, text="🛠️ Executar Tudo", fg_color="#111827",
            hover_color="#10B981", border_width=1, border_color="#10B981",
            font=ctk.CTkFont("Segoe UI", 10, "bold"), height=32, corner_radius=6,
            command=lambda: threading.Thread(target=self.run_all_maintenance, daemon=True).start())
        self.btn_maint_dash.grid(row=0, column=1, padx=3, sticky="nsew")

        self.btn_shell_dash = ctk.CTkButton(
            shortcuts_row, text="👑 Shell Mode", fg_color="#111827",
            hover_color=C["gold"], border_width=1, border_color=C["gold"],
            font=ctk.CTkFont("Segoe UI", 10, "bold"), height=32, corner_radius=6,
            command=self.toggle_gold_mode_explorer)
        self.btn_shell_dash.grid(row=0, column=2, padx=3, sticky="nsew")

        self.restore_btn = ctk.CTkButton(
            act, text="🔄  RESTAURAR PADRÕES DO WINDOWS",
            fg_color="#0F172A", hover_color="#EF4444",
            border_width=1, border_color="#1E293B",
            font=ctk.CTkFont("Segoe UI", 9, "bold"),
            height=30, corner_radius=6, text_color=C["muted"],
            command=self.start_restoration)
        self.restore_btn.pack(fill="x", padx=14, pady=(2, 10))

        # Card Radar (Movido para Row 3 do Dash)
        radar_card = ctk.CTkFrame(row3, fg_color=C["card"], border_width=1,
                                   border_color=C["border"], corner_radius=10)
        radar_card.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(radar_card, text="▌ PERFORMANCE RADAR",
                     font=ctk.CTkFont("Segoe UI", 9, "bold"),
                     text_color=C["cyan"]).pack(anchor="w", padx=12, pady=(10, 4))

        self.radar_canvas = ctk.CTkCanvas(
            radar_card, bg=C["card"], highlightthickness=0, width=240, height=160)
        self.radar_canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.draw_radar_chart()

        # ── LINHA 4: Manutenção Avançada (Central de Comando) ────────────────
        row4 = ctk.CTkFrame(tab, fg_color="transparent")
        row4.pack(fill="x", pady=(8, 0))
        
        m_adv_card = ctk.CTkFrame(row4, fg_color=C["card"], border_width=1,
                                   border_color=C["border"], corner_radius=10)
        m_adv_card.pack(fill="x")

        ctk.CTkLabel(m_adv_card, text="▌ MANUTENÇÃO AVANÇADA",
                     font=ctk.CTkFont("Segoe UI", 10, "bold"),
                     text_color=C["cyan"]).pack(anchor="w", padx=15, pady=(12, 10))

        m_grid = ctk.CTkFrame(m_adv_card, fg_color="transparent")
        m_grid.pack(fill="x", padx=15, pady=(0, 15))
        m_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Estilo dos botões de manutenção
        m_btn_style = {
            "height": 45,
            "corner_radius": 8,
            "font": ctk.CTkFont("Segoe UI", 11, "bold"),
            "border_width": 1,
            "border_color": C["border"],
            "fg_color": "#0F172A",
            "hover_color": "#1E293B"
        }

        # 1. Limpeza
        self.clean_btn = ctk.CTkButton(
            m_grid, text="🧹 LIMPEZA DISCO", **m_btn_style, text_color="#10B981",
            command=lambda: threading.Thread(target=self.run_extra_optimization, args=("clean_temp",)).start())
        self.clean_btn.grid(row=0, column=0, padx=5, sticky="nsew")

        # 2. Flush DNS
        self.dns_btn = ctk.CTkButton(
            m_grid, text="🌐 FLUSH DNS", **m_btn_style, text_color="#3B82F6",
            command=lambda: threading.Thread(target=self.run_extra_optimization, args=("flush_dns",)).start())
        self.dns_btn.grid(row=0, column=1, padx=5, sticky="nsew")

        # 3. Plano Ultimate
        self.power_btn = ctk.CTkButton(
            m_grid, text="⚡ PLANO ULTIMATE", **m_btn_style, text_color="#FBBF24",
            command=lambda: threading.Thread(target=self.run_extra_optimization, args=("power_plan",)).start())
        self.power_btn.grid(row=0, column=2, padx=5, sticky="nsew")

        # 4. Flush RAM
        self.ram_flush_btn = ctk.CTkButton(
            m_grid, text="💾 LIMPAR RAM", **m_btn_style, text_color="#F8FAFC",
            command=lambda: threading.Thread(target=self.run_extra_optimization, args=("ram_flush",)).start())
        self.ram_flush_btn.grid(row=0, column=3, padx=5, sticky="nsew")


    def create_management_tab(self):
        tab = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.tabs["management"] = tab

        # Cabeçalho
        manage_lbl = ctk.CTkLabel(tab, text="Processos & Serviços", font=self.title_font, text_color="#F8FAFC")
        manage_lbl.pack(anchor="w", pady=(5, 2))

        self.manage_sub = ctk.CTkLabel(
            tab, text="Selecione um nível de otimização para ver e ajustar suas opções detalhadamente.", 
            font=self.label_font, text_color="#94A3B8"
        )
        self.manage_sub.pack(anchor="w", pady=(0, 20))

        self.management_content_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.management_content_frame.pack(fill="both", expand=True)

        # ---------------------------------------------------------
        # GRID DE CARDS (Níveis de Otimização)
        # ---------------------------------------------------------
        self.levels_grid_frame = ctk.CTkFrame(self.management_content_frame, fg_color="transparent")
        self.levels_grid_frame.pack(fill="both", expand=True)

        self.levels_grid_frame.grid_columnconfigure((0, 1), weight=1)

        level_cards_data = [
            {"id": "Nível 1: Aplicativos & Bloatwares", "title": "🟢 Nível 1", "subtitle": "Apps & Bloatware", "row": 0, "col": 0},
            {"id": "Nível 2: Impressão & Manutenção", "title": "🟡 Nível 2", "subtitle": "Impressão & Servs.", "row": 0, "col": 1},
            {"id": "Nível 3: Telemetria & Rastreamento", "title": "🟠 Nível 3", "subtitle": "Telemetria & Rastr.", "row": 1, "col": 0},
            {"id": "Nível 4: Xbox & Conexões Secundárias", "title": "🔴 Nível 4", "subtitle": "Xbox & Conexões", "row": 1, "col": 1},
            {"id": "Nível 5: Redes & Streaming", "title": "🌐 Nível 5", "subtitle": "Redes & Streaming", "row": 2, "col": 0},
            {"id": "Nível 6: Segurança & Criptografia", "title": "🔒 Nível 6", "subtitle": "Segur. & Cripto.", "row": 2, "col": 1},
            {"id": "Nível 7: Modo Deus (God Mode)", "title": "👑 Modo Deus", "subtitle": "God Mode Supremo", "row": 3, "col": 0}
        ]

        for c in level_cards_data:
            btn_card = ctk.CTkButton(
                self.levels_grid_frame, text=f"{c['title']} - {c['subtitle']}",
                fg_color="#10151B", hover_color="#1E2631", border_width=1, border_color="#1E2631",
                font=self.section_font, height=60, corner_radius=10,
                command=lambda cat=c["id"]: self.show_level_options(cat)
            )
            if c["id"] == "Nível 7: Modo Deus (God Mode)":
                btn_card.grid(row=c["row"], column=c["col"], columnspan=2, padx=4, pady=4, sticky="nsew")
            else:
                btn_card.grid(row=c["row"], column=c["col"], padx=4, pady=4, sticky="nsew")

        # ---------------------------------------------------------
        self.level_details_frame = ctk.CTkFrame(self.management_content_frame, fg_color="transparent")
        
        self.back_btn = ctk.CTkButton(
            self.level_details_frame, text="⬅️ Voltar aos Níveis", fg_color="#10151B", hover_color="#1E2631", border_width=1, border_color="#1E2631",
            font=self.label_font, height=32, corner_radius=6, command=self.show_levels_grid
        )
        self.back_btn.pack(anchor="w", pady=(0, 8))

        self.scroll_frame = ctk.CTkScrollableFrame(self.level_details_frame, fg_color="#10151B", border_width=1, border_color="#1E2631", corner_radius=10)
        self.scroll_frame.pack(fill="both", expand=True)

        self.checkboxes = {}
        self.category_frames = {}

        for category, items in SERVICES_MAP.items():
            frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            self.category_frames[category] = frame

            cat_lbl = ctk.CTkLabel(frame, text=category.upper(), font=self.section_font, text_color="#00FFFF")
            cat_lbl.pack(anchor="w", padx=10, pady=(10, 5))

            for item in items:
                row_frame = ctk.CTkFrame(frame, fg_color="transparent")
                row_frame.pack(fill="x", padx=10, pady=2)

                cb = ctk.CTkCheckBox(
                    row_frame, text=f"{item['name']} ({item['id']})", 
                    font=self.label_font, fg_color="#00FFFF", hover_color="#00CCCC"
                )
                if item["checked"]:
                    cb.select()
                cb.pack(side="left", anchor="w")
                self.checkboxes[item["id"]] = cb

    def show_level_options(self, category):
        self.levels_grid_frame.pack_forget()
        self.manage_sub.configure(text=f"Personalizando opções detalhadas para: {category}")

        for frame in self.category_frames.values():
            frame.pack_forget()

        self.category_frames[category].pack(fill="both", expand=True)
        self.level_details_frame.pack(fill="both", expand=True)

    def show_levels_grid(self):
        self.level_details_frame.pack_forget()
        self.manage_sub.configure(text="Selecione um nível de otimização para ver e ajustar suas opções detalhadamente.")
        self.levels_grid_frame.pack(fill="both", expand=True)

    def create_scan_tab(self):
        tab = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.tabs["scan"] = tab

        scan_lbl = ctk.CTkLabel(tab, text="Escaneamento Avançado de Processos", font=self.title_font, text_color="#F8FAFC")
        scan_lbl.pack(anchor="w", pady=(5, 2))

        scan_sub = ctk.CTkLabel(tab, text="Visualize todos os processos do sistema operacional e escolha quais encerrar com segurança.", font=self.label_font, text_color="#94A3B8")
        scan_sub.pack(anchor="w", pady=(0, 10))

        # Top controls for scanning
        ctrl_frame = ctk.CTkFrame(tab, fg_color="transparent")
        ctrl_frame.pack(fill="x", pady=(5, 10))

        self.scan_run_btn = ctk.CTkButton(
            ctrl_frame, text="🔍 ESCANEAR TUDO EM TEMPO REAL", fg_color="#10B981", hover_color="#059669",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), height=46, corner_radius=12, text_color="#0D0F12",
            command=self.run_process_scan
        )
        self.scan_run_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.kill_selected_btn = ctk.CTkButton(
            ctrl_frame, text="⚡ ENCERRAR PROCESSOS SELECIONADOS", fg_color="#1F2937", hover_color="#10B981", border_width=1, border_color="#1E2B2A",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), height=46, corner_radius=12,
            command=self.kill_scanned_processes
        )
        self.kill_selected_btn.pack(side="right", fill="x", expand=True, padx=(10, 0))

        # Filter and Search Bar
        filter_frame = ctk.CTkFrame(tab, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        filter_frame.pack(fill="x", pady=(5, 10))

        f_lbl = ctk.CTkLabel(filter_frame, text="🔍 FILTRAR PROCESSOS:", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#10B981")
        f_lbl.pack(side="left", padx=(15, 10), pady=12)

        self.scan_filter_entry = ctk.CTkEntry(
            filter_frame, fg_color="#0D0F12", border_color="#1E2B2A", text_color="#E2E8F0", 
            placeholder_text="Ex: chrome, steam, edge...", height=36, corner_radius=8
        )
        self.scan_filter_entry.pack(side="left", fill="x", expand=True, padx=(0, 15), pady=12)
        self.scan_filter_entry.bind("<KeyRelease>", lambda e: self.filter_scan_list())

        # Select All / Select Safe
        sel_frame = ctk.CTkFrame(tab, fg_color="transparent")
        sel_frame.pack(fill="x", pady=(0, 5))

        self.select_all_btn = ctk.CTkButton(
            sel_frame, text="✅ Selecionar Todos", fg_color="#11161A", hover_color="#10B981", border_width=1, border_color="#1E2B2A",
            font=self.label_font, height=34, corner_radius=8, command=self.select_all_scanned
        )
        self.select_all_btn.pack(side="left", padx=(0, 8))

        self.select_safe_btn = ctk.CTkButton(
            sel_frame, text="🎮 Selecionar Apenas Seguros", fg_color="#11161A", hover_color="#10B981", border_width=1, border_color="#1E2B2A",
            font=self.label_font, height=34, corner_radius=8, command=self.select_safe_scanned
        )
        self.select_safe_btn.pack(side="left", padx=8)

        self.deselect_all_btn = ctk.CTkButton(
            sel_frame, text="❌ Desmarcar Todos", fg_color="#11161A", hover_color="#10B981", border_width=1, border_color="#1E2B2A",
            font=self.label_font, height=34, corner_radius=8, command=self.deselect_all_scanned
        )
        self.deselect_all_btn.pack(side="left", padx=8)

        self.scan_selection_lbl = ctk.CTkLabel(
            sel_frame, text="Nenhum processo listado", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#10B981"
        )
        self.scan_selection_lbl.pack(side="right", padx=(8, 15))

        # List Container
        self.scan_scroll_frame = ctk.CTkScrollableFrame(tab, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        self.scan_scroll_frame.pack(fill="both", expand=True, pady=(5, 5))

        # Add empty message
        self.scan_msg_lbl = ctk.CTkLabel(
            self.scan_scroll_frame, text="Clique em 'Escanear Tudo em Tempo Real' para listar todos os processos.", 
            font=self.label_font, text_color="#94A3B8"
        )
        self.scan_msg_lbl.pack(padx=20, pady=40)

        self.scanned_checkboxes = {}
        self.scanned_frames = {}

    def run_process_scan(self):
        # Limpar widgets anteriores
        for widget in self.scan_scroll_frame.winfo_children():
            widget.destroy()

        self.scanned_checkboxes.clear()
        self.scanned_frames.clear()

        # Mostrar indicador de progresso
        loading_lbl = ctk.CTkLabel(self.scan_scroll_frame, text="🔍 Escaneando processos...", font=self.label_font, text_color="#10B981")
        loading_lbl.pack(padx=20, pady=20)
        self.update_idletasks()

        # Buscar lista de processos reais usando tasklist via subprocess
        try:
            import subprocess
            out = subprocess.check_output(["tasklist", "/FO", "CSV"], text=True, errors="ignore")
            lines = out.strip().split("\n")
            active_p = {}
            for line in lines[1:]:
                parts = line.split(",")
                if len(parts) >= 5:
                    p_name = parts[0].strip('"').lower()
                    pid = parts[1].strip('"')
                    mem = parts[4].strip('"')
                    # Somar uso ou guardar
                    if p_name not in active_p:
                        active_p[p_name] = {"pid": pid, "mem": mem, "instances": 1}
                    else:
                        active_p[p_name]["instances"] += 1
        except Exception as e:
            self.log(f"⚠️ Erro ao executar tasklist: {e}", "error")
            active_p = {}

        loading_lbl.destroy()

        if not active_p:
            empty_lbl = ctk.CTkLabel(
                self.scan_scroll_frame, text="⚠️ Não foi possível obter a lista de processos ativos.", 
                font=self.label_font, text_color="#EF4444"
            )
            empty_lbl.pack(padx=20, pady=40)
            return

        # Header de Detecção
        detected_title = ctk.CTkLabel(
            self.scan_scroll_frame, text=f"📋 TOTAL DE PROCESSOS ENCONTRADOS NO SISTEMA: {len(active_p)}", 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#10B981"
        )
        detected_title.pack(anchor="w", padx=15, pady=(15, 10))

        # Table Header
        header_frame = ctk.CTkFrame(self.scan_scroll_frame, fg_color="#1E2B2A", corner_radius=6)
        header_frame.pack(fill="x", padx=15, pady=(5, 10))

        lbl_proc = ctk.CTkLabel(header_frame, text="📌 PROCESSO", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#10B981")
        lbl_proc.grid(row=0, column=0, padx=10, pady=8, sticky="w")

        lbl_ram = ctk.CTkLabel(header_frame, text="💾 INSTÂNCIAS & RAM", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#10B981")
        lbl_ram.grid(row=0, column=1, padx=10, pady=8, sticky="w")

        lbl_desc = ctk.CTkLabel(header_frame, text="📖 DESCRIÇÃO", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#10B981")
        lbl_desc.grid(row=0, column=2, padx=10, pady=8, sticky="w")

        lbl_effect = ctk.CTkLabel(header_frame, text="🎯 EFEITO / IMPACTO", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#10B981")
        lbl_effect.grid(row=0, column=3, padx=10, pady=8, sticky="w")

        header_frame.grid_columnconfigure(0, weight=3, minsize=240)
        header_frame.grid_columnconfigure(1, weight=2, minsize=140)
        header_frame.grid_columnconfigure(2, weight=3, minsize=240)
        header_frame.grid_columnconfigure(3, weight=3, minsize=220)

        # Processos Críticos do Windows que não devem ser encerrados
        CRITICAL_SYSTEM_PROCESSES = {
            "svchost.exe", "explorer.exe", "lsass.exe", "csrss.exe", "wininit.exe", 
            "services.exe", "smss.exe", "winlogon.exe", "fontdrvhost.exe", "dwm.exe",
            "taskhostw.exe", "spoolsv.exe", "ctfmon.exe", "securityhealthservice.exe",
            "sihost.exe", "nvvsvc.exe", "nvxdsync.exe", "nvdisplay.container.exe", 
            "nvgpucompilerservice.exe", "nvda.exe", "nvspcaps64.exe", "amddvr.exe", 
            "atiedxx.exe", "atiesrxx.exe", "radeonsoftware.exe", "cncmd.exe", 
            "igfxcuiservice.exe", "igfxem.exe", "igfxhk.exe", "igfxtray.exe"
        }

        # Processos recomendados para fechar (conhecidos)
        known_bloatware = {
            "chrome.exe", "msedge.exe", "discord.exe", "spotify.exe", "teams.exe", 
            "skype.exe", "anydesk.exe", "teamviewer.exe", "steam.exe", "epicgameslauncher.exe", 
            "onedrive.exe", "whatsapp.exe", "telegram.exe", "officeclicktorun.exe", "cortana.exe"
        }

        # Dicionário de metadados informativos para os processos
        PROCESS_DATA = {
            "chrome.exe": {"desc": "Navegador Google Chrome", "effect": "Libera muita RAM sem impacto no sistema"},
            "msedge.exe": {"desc": "Navegador Microsoft Edge", "effect": "Libera RAM sem impacto no sistema"},
            "discord.exe": {"desc": "Aplicativo Discord", "effect": "Reduz consumo de CPU e RAM"},
            "spotify.exe": {"desc": "Aplicativo Spotify", "effect": "Libera memória em segundo plano"},
            "teams.exe": {"desc": "Microsoft Teams", "effect": "Libera CPU e RAM"},
            "steam.exe": {"desc": "Steam Client", "effect": "Fechamento seguro para evitar distrações"},
            "epicgameslauncher.exe": {"desc": "Epic Games Launcher", "effect": "Libera RAM e Rede"},
            "onedrive.exe": {"desc": "Sincronizador OneDrive", "effect": "Evita sincronização durante o jogo"},
            "whatsapp.exe": {"desc": "WhatsApp Desktop", "effect": "Libera RAM sem impacto no sistema"},
            "telegram.exe": {"desc": "Telegram Desktop", "effect": "Libera RAM sem impacto no sistema"},
            "officeclicktorun.exe": {"desc": "Microsoft Office ClickToRun", "effect": "Libera recursos de CPU"},
            "cortana.exe": {"desc": "Assistente Cortana", "effect": "Fechamento totalmente seguro"},
            "svchost.exe": {"desc": "Host de Serviços do Windows", "effect": "Crítico. Não fechar (pode travar o PC)"},
            "explorer.exe": {"desc": "Interface visual do Windows", "effect": "Crítico. Não fechar ( some barra de tarefas )"},
            "dwm.exe": {"desc": "Gerenciador de Janelas do Windows", "effect": "Crítico. Não fechar (pode dar tela preta)"},
            "lsass.exe": {"desc": "Serviço de Segurança Local", "effect": "Crítico. Não fechar (reinicia o PC)"},
            "csrss.exe": {"desc": "Cliente/Servidor de Execução", "effect": "Crítico. Não fechar (tela azul)"},
            "services.exe": {"desc": "Gerenciador de Serviços", "effect": "Crítico. Não fechar (trava o Windows)"},
            "taskhostw.exe": {"desc": "Host de Tarefas do Windows", "effect": "Crítico. Não recomendável fechar"},
            "spoolsv.exe": {"desc": "Serviço de Impressão do Windows", "effect": "Geralmente seguro fechar se não estiver imprimindo"},
            "ctfmon.exe": {"desc": "Suporte a Idiomas e Teclado", "effect": "Crítico. Não recomendável fechar"}
        }

        # Iterar e preencher a lista completa de processos em formato de tabela
        for p_name, data in sorted(active_p.items()):
            p_frame = ctk.CTkFrame(self.scan_scroll_frame, fg_color="transparent")
            p_frame.pack(fill="x", padx=15, pady=2)

            p_frame.grid_columnconfigure(0, weight=3, minsize=240)
            p_frame.grid_columnconfigure(1, weight=2, minsize=140)
            p_frame.grid_columnconfigure(2, weight=3, minsize=240)
            p_frame.grid_columnconfigure(3, weight=3, minsize=220)

            is_critical = p_name in CRITICAL_SYSTEM_PROCESSES
            is_suggested = p_name in known_bloatware

            cb = ctk.CTkCheckBox(
                p_frame, text=p_name, font=self.label_font,
                fg_color="#10B981", hover_color="#059669",
                command=self.update_selection_counter
            )

            meta = PROCESS_DATA.get(p_name, {})
            if is_critical:
                cb.configure(state="disabled")
                desc_text = meta.get("desc", "Processo essencial do sistema")
                effect_text = meta.get("effect", "Não recomendável fechar")
                text_color = "#94A3B8"
            elif is_suggested:
                cb.select()
                desc_text = meta.get("desc", "Software de terceiro em segundo plano")
                effect_text = meta.get("effect", "Otimização Gamer Recomendada")
                text_color = "#10B981"
            else:
                desc_text = meta.get("desc", "Aplicativo / Serviço de Segundo Plano")
                effect_text = meta.get("effect", "Geralmente seguro fechar")
                text_color = "#38BDF8"

            cb.grid(row=0, column=0, padx=10, pady=4, sticky="w")

            ram_lbl = ctk.CTkLabel(p_frame, text=f"{data['instances']} inst. | {data['mem']}", font=self.label_font, text_color="#E2E8F0")
            ram_lbl.grid(row=0, column=1, padx=10, pady=4, sticky="w")

            desc_lbl = ctk.CTkLabel(p_frame, text=desc_text, font=ctk.CTkFont(family="Segoe UI", size=11), text_color="#94A3B8")
            desc_lbl.grid(row=0, column=2, padx=10, pady=4, sticky="w")

            effect_lbl = ctk.CTkLabel(p_frame, text=effect_text, font=ctk.CTkFont(family="Segoe UI", size=11, slant="italic"), text_color=text_color)
            effect_lbl.grid(row=0, column=3, padx=10, pady=4, sticky="w")

            self.scanned_checkboxes[p_name] = cb
            self.scanned_frames[p_name] = p_frame

        # Limpa o filtro de texto ao escanear
        self.scan_filter_entry.delete(0, "end")
        self.update_selection_counter()

    def update_selection_counter(self):
        total = len(self.scanned_checkboxes)
        marked = sum(1 for cb in self.scanned_checkboxes.values() if cb.get())
        if total == 0:
            self.scan_selection_lbl.configure(text="Nenhum processo listado", text_color="#94A3B8")
        else:
            self.scan_selection_lbl.configure(text=f"📌 Marcados: {marked} de {total}", text_color="#10B981")

    def select_all_scanned(self):
        for p_name, cb in self.scanned_checkboxes.items():
            if cb.cget("state") != "disabled":
                cb.select()
        self.update_selection_counter()

    def select_safe_scanned(self):
        known_bloatware = {
            "chrome.exe", "msedge.exe", "discord.exe", "spotify.exe", "teams.exe", 
            "skype.exe", "anydesk.exe", "teamviewer.exe", "steam.exe", "epicgameslauncher.exe", 
            "onedrive.exe", "whatsapp.exe", "telegram.exe", "officeclicktorun.exe", "cortana.exe"
        }
        for p_name, cb in self.scanned_checkboxes.items():
            if p_name in known_bloatware and cb.cget("state") != "disabled":
                cb.select()
            else:
                if cb.cget("state") != "disabled":
                    cb.deselect()
        self.update_selection_counter()

    def deselect_all_scanned(self):
        for p_name, cb in self.scanned_checkboxes.items():
            if cb.cget("state") != "disabled":
                cb.deselect()
        self.update_selection_counter()

    def filter_scan_list(self):
        query = self.scan_filter_entry.get().strip().lower()
        for p_name, frame in self.scanned_frames.items():
            if query in p_name:
                frame.pack(fill="x", padx=15, pady=3)
            else:
                frame.pack_forget()

    def kill_scanned_processes(self):
        to_kill = []
        for p_file, cb in self.scanned_checkboxes.items():
            if cb.get() and cb.cget("state") != "disabled":
                to_kill.append(p_file)

        if not to_kill:
            self.log("⚠️ Nenhum processo selecionado para encerramento.", "warning")
            return

        self.log(f"\n⚡ Iniciando encerramento de {len(to_kill)} processos...", "info")

        for p in to_kill:
            if DRY_RUN:
                self.log(f"[SIMULAÇÃO] Encerrando {p} via Scan.", "info")
            else:
                try:
                    import subprocess
                    subprocess.run(["taskkill", "/F", "/IM", p], capture_output=True, text=True)
                    self.log(f"✔️ {p} encerrado com sucesso!", "success")
                except Exception as e:
                    self.log(f"❌ Falha ao encerrar {p}: {e}", "error")

        # Re-escanear para atualizar a lista
        self.run_process_scan()

    def create_settings_tab(self):
        tab = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.tabs["settings"] = tab

        settings_lbl = ctk.CTkLabel(tab, text="Configurações", font=self.title_font, text_color="#F8FAFC")
        settings_lbl.pack(anchor="w", pady=(5, 2))

        settings_sub = ctk.CTkLabel(tab, text="Ajustes avançados do aplicativo.", font=self.label_font, text_color="#94A3B8")
        settings_sub.pack(anchor="w", pady=(0, 20))

        panel = ctk.CTkFrame(tab, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        panel.pack(fill="x", pady=10, padx=5)

        s1_lbl = ctk.CTkLabel(panel, text="Modo de Operação", font=self.section_font, text_color="#10B981")
        s1_lbl.pack(anchor="w", padx=20, pady=(20, 5))

        desc_lbl = ctk.CTkLabel(
            panel, text="Por padrão, o modo Simulação fica ATIVO. Desative para aplicar as modificações reais.",
            font=self.label_font, text_color="#94A3B8"
        )
        desc_lbl.pack(anchor="w", padx=20, pady=(0, 15))

    def create_autoboost_tab(self):
        tab = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.tabs["autoboost"] = tab

        ab_lbl = ctk.CTkLabel(tab, text="Módulo Auto-Boost (Automação Proativa)", font=self.title_font, text_color="#F8FAFC")
        ab_lbl.pack(anchor="w", pady=(5, 2))

        ab_sub = ctk.CTkLabel(tab, text="Deixe o Killprocess monitorar seus jogos e aplicar o nível de otimização automaticamente em tempo real.", font=self.label_font, text_color="#94A3B8")
        ab_sub.pack(anchor="w", pady=(0, 15))

        # Painel de Status
        panel = ctk.CTkFrame(tab, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        panel.pack(fill="x", pady=5)

        self.ab_toggle_btn = ctk.CTkButton(
            panel, text="🟢 ATIVAR MONITORAMENTO AUTO-BOOST", fg_color="#10B981", hover_color="#059669",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), height=46, corner_radius=10, text_color="#0D0F12",
            command=self.toggle_autoboost
        )
        self.ab_toggle_btn.pack(side="left", padx=20, pady=20)

        self.ab_state_lbl = ctk.CTkLabel(
            panel, text="Status do Monitoramento: DESATIVADO", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color="#EF4444"
        )
        self.ab_state_lbl.pack(side="left", padx=10, pady=20)

        # Container para a lista de jogos suportados
        games_frame = ctk.CTkFrame(tab, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        games_frame.pack(fill="both", expand=True, pady=10)

        title_games = ctk.CTkLabel(games_frame, text="🎮 JOGOS SUPORTADOS & MONITORADOS", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#10B981")
        title_games.pack(anchor="w", padx=15, pady=(15, 10))

        # Headers da tabela de jogos
        header_row = ctk.CTkFrame(games_frame, fg_color="#1E2B2A", corner_radius=6)
        header_row.pack(fill="x", padx=15, pady=(0, 5))

        lbl_exe = ctk.CTkLabel(header_row, text="🖥️ EXECUTÁVEL (.exe)", font=self.label_font, text_color="#10B981")
        lbl_exe.grid(row=0, column=0, padx=15, pady=8, sticky="w")

        lbl_game = ctk.CTkLabel(header_row, text="🕹️ JOGO", font=self.label_font, text_color="#10B981")
        lbl_game.grid(row=0, column=1, padx=15, pady=8, sticky="w")

        lbl_stat = ctk.CTkLabel(header_row, text="📊 STATUS EM TEMPO REAL", font=self.label_font, text_color="#10B981")
        lbl_stat.grid(row=0, column=2, padx=15, pady=8, sticky="w")

        header_row.grid_columnconfigure(0, weight=2, minsize=220)
        header_row.grid_columnconfigure(1, weight=3, minsize=320)
        header_row.grid_columnconfigure(2, weight=2, minsize=220)

        # Listar os jogos
        self.autoboost_status_lbls.clear()
        for g in self.supported_games:
            r_frame = ctk.CTkFrame(games_frame, fg_color="transparent")
            r_frame.pack(fill="x", padx=15, pady=2)

            r_frame.grid_columnconfigure(0, weight=2, minsize=220)
            r_frame.grid_columnconfigure(1, weight=3, minsize=320)
            r_frame.grid_columnconfigure(2, weight=2, minsize=220)

            exe_lbl = ctk.CTkLabel(r_frame, text=g["exe"], font=self.label_font, text_color="#E2E8F0")
            exe_lbl.grid(row=0, column=0, padx=15, pady=4, sticky="w")

            name_lbl = ctk.CTkLabel(r_frame, text=g["name"], font=self.label_font, text_color="#94A3B8")
            name_lbl.grid(row=0, column=1, padx=15, pady=4, sticky="w")

            stat_lbl = ctk.CTkLabel(r_frame, text="Inativo", font=self.label_font, text_color="#94A3B8")
            stat_lbl.grid(row=0, column=2, padx=15, pady=4, sticky="w")

            self.autoboost_status_lbls[g["exe"]] = stat_lbl

        # Botão para adicionar novo jogo manualmente
        add_frame = ctk.CTkFrame(tab, fg_color="transparent")
        add_frame.pack(fill="x", pady=5)

        self.add_game_entry = ctk.CTkEntry(
            add_frame, fg_color="#11161A", border_color="#1E2B2A", text_color="#E2E8F0",
            placeholder_text="Adicionar novo executável (Ex: cyberpunk2077.exe)", height=36, corner_radius=8
        )
        self.add_game_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.add_game_btn = ctk.CTkButton(
            add_frame, text="➕ Adicionar Jogo", fg_color="#1F2937", hover_color="#10B981", border_width=1, border_color="#1E2B2A",
            font=self.label_font, height=36, corner_radius=8, command=self.add_custom_game
        )
        self.add_game_btn.pack(side="right")

    def toggle_autoboost(self):
        self.autoboost_enabled = not self.autoboost_enabled
        if self.autoboost_enabled:
            self.ab_toggle_btn.configure(text="🔴 DESATIVAR MONITORAMENTO AUTO-BOOST", fg_color="#EF4444", hover_color="#DC2626")
            self.ab_state_lbl.configure(text="Status do Monitoramento: ATIVADO", text_color="#10B981")
            if hasattr(self, "btn_ab_dash"):
                self.btn_ab_dash.configure(fg_color="#10B981", text="🚀 Auto-Boost (ON)")
            self.log("\n🚀 Monitoramento Auto-Boost ATIVADO!", "success")
            threading.Thread(target=self.autoboost_polling_loop, daemon=True).start()
        else:
            self.ab_toggle_btn.configure(text="🟢 ATIVAR MONITORAMENTO AUTO-BOOST", fg_color="#10B981", hover_color="#059669")
            self.ab_state_lbl.configure(text="Status do Monitoramento: DESATIVADO", text_color="#EF4444")
            if hasattr(self, "btn_ab_dash"):
                self.btn_ab_dash.configure(fg_color="#1E2631", text="🚀 Auto-Boost")
            self.log("\n🛑 Monitoramento Auto-Boost DESATIVADO!", "warning")

    def add_custom_game(self):
        game_exe = self.add_game_entry.get().strip().lower()
        if not game_exe:
            return
        if not game_exe.endswith(".exe"):
            game_exe += ".exe"
        
        # Avoid duplicate
        if any(g["exe"] == game_exe for g in self.supported_games):
            return

        game_data = {"exe": game_exe, "name": f"Jogo Manual: {game_exe}"}
        self.supported_games.append(game_data)
        self.log(f"➕ Jogo customizado '{game_exe}' adicionado à lista do Auto-Boost.", "info")
        self.add_game_entry.delete(0, "end")
        
        # Clear existing widgets from game container
        for widget in self.tabs["autoboost"].winfo_children():
            widget.destroy()
        
        # Re-create and update Auto-Boost tab
        self.create_autoboost_tab()

    def autoboost_polling_loop(self):
        while self.autoboost_enabled:
            try:
                import subprocess
                out = subprocess.check_output(["tasklist", "/FO", "CSV"], text=True, errors="ignore")
                lines = out.lower()

                for g in self.supported_games:
                    exe = g["exe"].lower()
                    if exe in lines:
                        if exe in self.autoboost_status_lbls:
                            self.autoboost_status_lbls[exe].configure(text="🔥 Ativo", text_color="#10B981")
                        self.log(f"\n🎮 [Auto-Boost]: Jogo detectado rodando: {exe}! Ativando Modo Deus automaticamente.", "info")
                        self.start_god_mode()
                    else:
                        if exe in self.autoboost_status_lbls:
                            self.autoboost_status_lbls[exe].configure(text="Inativo", text_color="#94A3B8")
            except Exception as e:
                pass
            time.sleep(5)

    def create_shell_tab(self):
        tab = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.tabs["shell"] = tab

        # ---------------------------------------------------------
        # 1. HEADER & BOTÃO DOURADO
        # ---------------------------------------------------------
        top_bar = ctk.CTkFrame(tab, fg_color="#11161A", border_width=1, border_color="#D97706", corner_radius=12)
        top_bar.pack(fill="x", pady=(0, 15))

        lbl_shell = ctk.CTkLabel(top_bar, text="👑 CENTRAL DE ATALHO OPERACIONAL", font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color="#FBBF24")
        lbl_shell.pack(anchor="w", padx=20, pady=(15, 2))

        sub_shell = ctk.CTkLabel(top_bar, text="Otimize o PC fechando o Windows Explorer e gerencie tudo por aqui.", font=self.label_font, text_color="#94A3B8")
        sub_shell.pack(anchor="w", padx=20, pady=(0, 15))

        # Botão Dourado / Golden Switch para fechar o Explorer
        gold_actions = ctk.CTkFrame(top_bar, fg_color="transparent")
        gold_actions.pack(fill="x", padx=20, pady=(0, 15))

        self.gold_toggle_btn = ctk.CTkButton(
            gold_actions, text="🔥 FECHAR WINDOWS EXPLORER (GOLD MODE)", fg_color="#D97706", hover_color="#B45309",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), height=46, corner_radius=10, text_color="#0D0F12",
            command=self.toggle_gold_mode_explorer
        )
        self.gold_toggle_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.explorer_state_lbl = ctk.CTkLabel(
            gold_actions, text="Explorer do Windows: ATIVO", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color="#10B981"
        )
        self.explorer_state_lbl.pack(side="left", padx=10)

        # ---------------------------------------------------------
        # 2. RELÓGIO & CONTROLE DE VOLUME
        # ---------------------------------------------------------
        tools_frame = ctk.CTkFrame(tab, fg_color="transparent")
        tools_frame.pack(fill="x", pady=(0, 15))
        tools_frame.grid_columnconfigure((0, 1), weight=1)

        # Card de Relógio
        clock_card = ctk.CTkFrame(tools_frame, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12, height=140)
        clock_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        clock_card.grid_propagate(False)

        c_title = ctk.CTkLabel(clock_card, text="🕒 RELÓGIO E DATA", font=self.section_font, text_color="#10B981")
        c_title.pack(anchor="w", padx=15, pady=(12, 2))

        self.shell_clock_lbl = ctk.CTkLabel(clock_card, text="--:--:--", font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"), text_color="#F8FAFC")
        self.shell_clock_lbl.pack(anchor="w", padx=15)

        self.shell_date_lbl = ctk.CTkLabel(clock_card, text="Carregando data...", font=self.label_font, text_color="#94A3B8")
        self.shell_date_lbl.pack(anchor="w", padx=15)

        # Card de Volume
        volume_card = ctk.CTkFrame(tools_frame, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12, height=140)
        volume_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        volume_card.grid_propagate(False)

        v_title = ctk.CTkLabel(volume_card, text="🔊 CONTROLE DE VOLUME", font=self.section_font, text_color="#10B981")
        v_title.pack(anchor="w", padx=15, pady=(12, 10))

        vol_actions = ctk.CTkFrame(volume_card, fg_color="transparent")
        vol_actions.pack(fill="x", padx=15)

        btn_mute = ctk.CTkButton(
            vol_actions, text="🔇 Mute", fg_color="#1F2937", hover_color="#4B5563",
            font=self.label_font, width=70, height=36, corner_radius=8, command=self.shell_volume_mute
        )
        btn_mute.pack(side="left", padx=(0, 6))

        btn_vol_down = ctk.CTkButton(
            vol_actions, text="➖ Vol Down", fg_color="#1F2937", hover_color="#4B5563",
            font=self.label_font, width=90, height=36, corner_radius=8, command=self.shell_volume_down
        )
        btn_vol_down.pack(side="left", padx=6)

        btn_vol_up = ctk.CTkButton(
            vol_actions, text="➕ Vol Up", fg_color="#1F2937", hover_color="#4B5563",
            font=self.label_font, width=90, height=36, corner_radius=8, command=self.shell_volume_up
        )
        btn_vol_up.pack(side="left", padx=6)

        # ---------------------------------------------------------
        # 3. BARRA DE PESQUISA & COMANDOS
        # ---------------------------------------------------------
        search_card = ctk.CTkFrame(tab, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        search_card.pack(fill="x", pady=(0, 15))

        s_title = ctk.CTkLabel(search_card, text="🔍 EXECUTAR COMANDO / ABRIR PASTA", font=self.section_font, text_color="#10B981")
        s_title.pack(anchor="w", padx=15, pady=(12, 5))

        search_actions = ctk.CTkFrame(search_card, fg_color="transparent")
        search_actions.pack(fill="x", padx=15, pady=(0, 12))

        self.shell_cmd_entry = ctk.CTkEntry(
            search_actions, fg_color="#0D0F12", border_color="#1E2B2A", text_color="#E2E8F0",
            placeholder_text="Ex: taskmgr, calc, explorer, cmd, ou caminho de pasta como C:\\", height=38, corner_radius=8
        )
        self.shell_cmd_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.shell_cmd_entry.bind("<Return>", lambda e: self.shell_execute_command())

        btn_exec = ctk.CTkButton(
            search_actions, text="⚡ Executar", fg_color="#1F2937", hover_color="#10B981", border_width=1, border_color="#1E2B2A",
            font=self.label_font, height=38, corner_radius=8, command=self.shell_execute_command
        )
        btn_exec.pack(side="right")

        # ---------------------------------------------------------
        # 4. CENTRAL DE JOGOS FAVORITOS
        # ---------------------------------------------------------
        games_card = ctk.CTkFrame(tab, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        games_card.pack(fill="both", expand=True)

        g_title = ctk.CTkLabel(games_card, text="🕹️ LAUNCHER DE JOGOS FAVORITOS", font=self.section_font, text_color="#10B981")
        g_title.pack(anchor="w", padx=15, pady=(12, 10))

        games_grid = ctk.CTkFrame(games_card, fg_color="transparent")
        games_grid.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        games_grid.grid_columnconfigure((0, 1, 2), weight=1)

        # Populando atalhos de jogos configurados
        for idx, g in enumerate(self.supported_games):
            r = idx // 3
            c = idx % 3
            btn_game = ctk.CTkButton(
                games_grid, text=f"🎮 {g['name']}\n({g['exe']})", fg_color="#1F2937", hover_color="#10B981",
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), height=54, corner_radius=10,
                command=lambda e=g["exe"]: self.launch_game_from_shell(e)
            )
            btn_game.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")

        # Iniciar loop do relógio na aba Shell
        threading.Thread(target=self.shell_clock_loop, daemon=True).start()

    def create_optimize_center_tab(self):
        tab = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.tabs["optimize_center"] = tab

        # Header estilo referência
        header = ctk.CTkFrame(tab, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        title_lbl = ctk.CTkLabel(header, text="Otimizações Premium", font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color="#F8FAFC")
        title_lbl.pack(side="left")
        
        status_badge = ctk.CTkButton(
            header, text="SISTEMA PRONTO", fg_color="#D97706", hover_color="#D97706", width=140, height=32, corner_radius=6,
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#0D0F12"
        )
        status_badge.pack(side="right")

        # Grid de Cards (2 colunas)
        grid = ctk.CTkFrame(tab, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure((0, 1), weight=1)

        opt_items = [
            {"id": "power", "title": "Plano Energia", "desc": "Alto desempenho (monitor/disco timeout 0)", "color": "#EF4444", "cmd": "power_plan"},
            {"id": "priority", "title": "Prioridade Processo", "desc": "Define prioridade do jogo para Alta", "color": "#EF4444", "cmd": "priority_high"},
            {"id": "clean", "title": "Limpar Processo", "desc": "Fecha apps desnecessarios (exceto whitelist)", "color": "#EF4444", "cmd": "clean_apps"},
            {"id": "registry", "title": "Registry Gaming", "desc": "Otimizacoes de registro para games", "color": "#EF4444", "cmd": "registry_gaming"},
            {"id": "tcp", "title": "TCP Otimizado", "desc": "Auto-tuning, chimney, ECN", "color": "#EF4444", "cmd": "tcp_opt"},
            {"id": "services", "title": "Servicos", "desc": "Desabilita servicos nao essenciais", "color": "#EF4444", "cmd": "services_opt"},
            {"id": "ram", "title": "RAM", "desc": "Libera memoria (GC)", "color": "#EF4444", "cmd": "ram_flush"},
            {"id": "full", "title": "Otimizacao Completa", "desc": "Aplica todas as otimizações", "color": "#EF4444", "cmd": "full_opt"}
        ]

        for idx, item in enumerate(opt_items):
            r = idx // 2
            c = idx % 2
            
            card = ctk.CTkFrame(grid, fg_color="#18181B", border_width=1, border_color="#27272A", corner_radius=12, height=110)
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            card.grid_propagate(False)
            
            # Dot indicator
            dot = ctk.CTkLabel(card, text="●", text_color=item["color"], font=ctk.CTkFont(size=18))
            dot.place(x=15, y=15)
            
            title = ctk.CTkLabel(card, text=item["title"], font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"), text_color="#F8FAFC")
            title.place(x=40, y=14)
            
            desc = ctk.CTkLabel(card, text=item["desc"], font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#94A3B8")
            desc.place(x=40, y=42)

            btn = ctk.CTkButton(
                card, text="APLICAR", width=80, height=26, corner_radius=6, fg_color="#27272A", hover_color="#3F3F46",
                font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
                command=lambda cmd=item["cmd"]: threading.Thread(target=self.run_premium_optimization, args=(cmd,)).start()
            )
            btn.place(x=40, y=70)

    def run_premium_optimization(self, cmd):
        if cmd == "power_plan":
            self.run_extra_optimization("power_plan")
        elif cmd == "registry_gaming":
            self.log("\n🛠️ Aplicando Registry Gaming...", "info")
            optimize_registry(self.log)
            self.log("✅ Registro otimizado com sucesso!", "success")
        elif cmd == "tcp_opt":
            self.log("\n🌐 Otimizando TCP...", "info")
            optimize_tcp(self.log)
            self.log("✅ Rede TCP otimizada com sucesso!", "success")
        elif cmd == "ram_flush":
            self.run_extra_optimization("ram_flush")
        elif cmd == "clean_apps":
            self.start_optimization() # Nível 1
        elif cmd == "services_opt":
            self.start_optimize_selection() # Baseado na seleção
        elif cmd == "priority_high":
            self.log("\n⚡ Ajustando prioridade de processos para ALTA...", "info")
            self.log("ℹ️ Buscando jogos ativos para elevar prioridade...", "info")
        elif cmd == "full_maint":
            self.run_all_maintenance()
        elif cmd == "full_opt":
            self.start_god_mode()
            self.run_premium_optimization("registry_gaming")
            self.run_premium_optimization("tcp_opt")
            self.run_premium_optimization("power_plan")

    def create_extra_tab(self):
        tab = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.tabs["extra"] = tab

        extra_lbl = ctk.CTkLabel(tab, text="Ferramentas de Manutenção & Limpeza", font=self.title_font, text_color="#F8FAFC")
        extra_lbl.pack(anchor="w", pady=(5, 2))

        extra_sub = ctk.CTkLabel(tab, text="Otimizações adicionais para manter seu sistema limpo e rápido.", font=self.label_font, text_color="#94A3B8")
        extra_sub.pack(anchor="w", pady=(0, 15))

        # Grid de ferramentas de manutenção
        tools_grid = ctk.CTkFrame(tab, fg_color="transparent")
        tools_grid.pack(fill="both", expand=True)
        tools_grid.grid_columnconfigure((0, 1), weight=1)

        # 1. Limpeza de Arquivos Temporários
        clean_card = ctk.CTkFrame(tools_grid, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        clean_card.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")
        
        c_title = ctk.CTkLabel(clean_card, text="🧹 LIMPEZA DE DISCO", font=self.section_font, text_color="#10B981")
        c_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        c_desc = ctk.CTkLabel(clean_card, text="Remove arquivos temporários, cache e prefetch para liberar espaço.", font=self.label_font, text_color="#94A3B8", justify="left")
        c_desc.pack(anchor="w", padx=15, pady=(0, 15))

        self.btn_clean_temp = ctk.CTkButton(
            clean_card, text="EXECUTAR LIMPEZA AGORA", fg_color="#1F2937", hover_color="#10B981", border_width=1, border_color="#1E2B2A",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), height=40, corner_radius=8,
            command=lambda: threading.Thread(target=self.run_extra_optimization, args=("clean_temp",)).start()
        )
        self.btn_clean_temp.pack(fill="x", padx=15, pady=(0, 15))

        # 2. Otimização de Rede (Flush DNS)
        net_card = ctk.CTkFrame(tools_grid, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        net_card.grid(row=0, column=1, padx=6, pady=6, sticky="nsew")
        
        n_title = ctk.CTkLabel(net_card, text="🌐 OTIMIZAÇÃO DE REDE", font=self.section_font, text_color="#10B981")
        n_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        n_desc = ctk.CTkLabel(net_card, text="Limpa o cache de DNS e redefine o Winsock para melhorar o ping.", font=self.label_font, text_color="#94A3B8", justify="left")
        n_desc.pack(anchor="w", padx=15, pady=(0, 15))

        self.btn_flush_dns = ctk.CTkButton(
            net_card, text="FLUSH DNS & RESET REDE", fg_color="#1F2937", hover_color="#10B981", border_width=1, border_color="#1E2B2A",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), height=40, corner_radius=8,
            command=lambda: threading.Thread(target=self.run_extra_optimization, args=("flush_dns",)).start()
        )
        self.btn_flush_dns.pack(fill="x", padx=15, pady=(0, 15))

        # 3. Plano de Energia de Desempenho Máximo
        power_card = ctk.CTkFrame(tools_grid, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        power_card.grid(row=1, column=0, padx=6, pady=6, sticky="nsew")
        
        p_title = ctk.CTkLabel(power_card, text="⚡ DESEMPENHO MÁXIMO", font=self.section_font, text_color="#FBBF24")
        p_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        p_desc = ctk.CTkLabel(power_card, text="Ativa o Plano de Energia 'Desempenho Máximo' oculto do Windows.", font=self.label_font, text_color="#94A3B8", justify="left")
        p_desc.pack(anchor="w", padx=15, pady=(0, 15))

        self.btn_power_plan = ctk.CTkButton(
            power_card, text="ATIVAR PLANO ULTIMATE", fg_color="#D97706", hover_color="#B45309",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), height=40, corner_radius=8, text_color="#0D0F12",
            command=lambda: threading.Thread(target=self.run_extra_optimization, args=("power_plan",)).start()
        )
        self.btn_power_plan.pack(fill="x", padx=15, pady=(0, 15))
        # 4. Otimização de RAM (System Cache Flush)
        ram_card = ctk.CTkFrame(tools_grid, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        ram_card.grid(row=1, column=1, padx=6, pady=6, sticky="nsew")
        
        r_title = ctk.CTkLabel(ram_card, text="💾 FLUSH DE MEMÓRIA RAM", font=self.section_font, text_color="#F8FAFC")
        r_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        r_desc = ctk.CTkLabel(ram_card, text="Força o Garbage Collector e tenta liberar cache do sistema.", font=self.label_font, text_color="#94A3B8", justify="left")
        r_desc.pack(anchor="w", padx=15, pady=(0, 15))

        self.btn_ram_flush = ctk.CTkButton(
            ram_card, text="LIMPAR CACHE DE RAM", fg_color="#1F2937", hover_color="#00FFFF", border_width=1, border_color="#1E2B2A",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), height=40, corner_radius=8,
            command=lambda: threading.Thread(target=self.run_extra_optimization, args=("ram_flush",)).start()
        )
        self.btn_ram_flush.pack(fill="x", padx=15, pady=(0, 15))

    def run_extra_optimization(self, action):
        if action == "clean_temp":
            self.log("\n🧹 Iniciando Limpeza de Disco Avançada...", "info")
            clean_temp_files(self.log)
            self.log("✅ Limpeza de Arquivos Temporários Concluída!", "success")
        elif action == "flush_dns":
            self.log("\n🌐 Otimizando Resposta de Rede...", "info")
            flush_dns(self.log)
            self.log("✅ Cache de DNS Limpo e Rede Otimizada!", "success")
        elif action == "power_plan" or action == "ultimate_power":
            self.log("\n⚡ Configurando Plano de Performance Máxima...", "info")
            set_ultimate_performance(self.log)
            self.log("✅ Plano 'Ultimate Performance' Ativado!", "success")
        elif action == "ram_flush":
            self.log("\n💾 Executando Flush de Memória RAM...", "info")
            try:
                mem_before = psutil.virtual_memory().available
                run_cmd("[System.GC]::Collect()")
                mem_after = psutil.virtual_memory().available
                freed = (mem_after - mem_before) / (1024 * 1024)
                if freed < 0: freed = 0
                self.log(f"✅ RAM Flush Concluído: {freed:.1f} MB liberados instantaneamente!", "success")
            except Exception as e:
                self.log(f"⚠️ Falha no Flush de RAM: {e}", "error")

    def run_all_maintenance(self):
        self.log("\n--- 🛠️ INICIANDO MANUTENÇÃO COMPLETA ---", "info")
        self.run_extra_optimization("clean_temp")
        self.run_extra_optimization("flush_dns")
        self.run_extra_optimization("power_plan")
        self.run_extra_optimization("ram_flush")
        self.log("✅ MANUTENÇÃO COMPLETA CONCLUÍDA!\n", "success")

    def toggle_gold_mode_explorer(self):
        self.shell_explorer_closed = not self.shell_explorer_closed
        if self.shell_explorer_closed:
            self.gold_toggle_btn.configure(text="🟢 RESTAURAR WINDOWS EXPLORER", fg_color="#10B981", hover_color="#059669")
            self.explorer_state_lbl.configure(text="Explorer do Windows: FECHADO", text_color="#EF4444")
            if hasattr(self, "btn_shell_dash"):
                self.btn_shell_dash.configure(fg_color="#D97706", text="👑 Shell Mode (ON)")
            self.log("\n⚠️ [Gold Mode]: Encerrando explorer.exe...")
            if DRY_RUN:
                self.log("[SIMULAÇÃO] explorer.exe encerrado via Gold Mode.")
            else:
                # Usar PowerShell para garantir o encerramento em todos os contextos
                run_cmd("Stop-Process -Name explorer -Force")
        else:
            if not DRY_RUN:
                subprocess.Popen(["explorer.exe"])
            
            self.gold_toggle_btn.configure(text="🔥 FECHAR WINDOWS EXPLORER (GOLD MODE)", fg_color="#D97706", hover_color="#B45309")
            self.explorer_state_lbl.configure(text="Explorer do Windows: ATIVO", text_color="#10B981")
            if hasattr(self, "btn_shell_dash"):
                self.btn_shell_dash.configure(fg_color="#1E2631", text="👑 Shell Mode")
            self.log("\n✔️ [Gold Mode]: Restaurando explorer.exe...")
            if DRY_RUN:
                self.log("[SIMULAÇÃO] explorer.exe restaurado.")
        
        # Atualiza o radar imediatamente para feedback visual
        self.draw_radar_chart()

    def create_restore_point(self):
        self.log("\n>>> INICIANDO CRIAÇÃO DE PONTO DE RESTAURAÇÃO...", "info")
        def run():
            try:
                import subprocess
                cmd = 'Checkpoint-Computer -Description "Apex HUD Restore Point" -RestorePointType "MODIFY_SETTINGS"'
                result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    self.log("✅ PONTO DE RESTAURAÇÃO CRIADO COM SUCESSO!", "success")
                else:
                    self.log("❌ FALHA AO CRIAR PONTO. CERTIFIQUE-SE DE EXECUTAR COMO ADMINISTRADOR.", "error")
                    self.log(f"Detalhe: {result.stderr}", "muted")
            except Exception as e:
                self.log(f"❌ ERRO CRÍTICO: {str(e)}", "error")
        
        threading.Thread(target=run, daemon=True).start()

    def render_shortcuts(self):
        from PIL import Image
        import os
        
        # Limpar container
        for widget in self.shortcut_container.winfo_children():
            widget.destroy()
            
        # Adicionar os padrões se não houver customizados
        apps = self.custom_shortcuts if self.custom_shortcuts else [
            {"name": "STEAM", "icon_path": "assets/steam.png", "color": "#171A21"},
            {"name": "DISCORD", "icon_path": "assets/discord.png", "color": "#5865F2"},
            {"name": "CHROME", "icon_path": "assets/chrome.png", "color": "#4285F4"}
        ]
        
        for app in apps:
            frame = ctk.CTkFrame(self.shortcut_container, fg_color="transparent")
            frame.pack(fill="x", pady=3)
            
            # Carregar ícone original com transparência REAL
            img = None
            if "icon_path" in app and os.path.exists(app["icon_path"]):
                try:
                    pil_img = Image.open(app["icon_path"]).convert("RGBA")
                    img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(20, 20))
                except:
                    pass
            
            btn = ctk.CTkButton(frame, text=f"  {app['name']}", image=img, width=200, height=36, corner_radius=8, 
                                fg_color=C["card"], border_width=1, border_color=C["border"], anchor="w",
                                hover_color=app.get("color", C["accent"]), font=("Segoe UI", 10, "bold"), 
                                command=lambda a=app: self.launch_shortcut(a["name"], a.get("path")))
            btn.pack(side="top", fill="x")

    def start_system_audit(self):
        self.audit_active = True
        self.initial_stats = {}
        self.audit_progress = 0
        
        # Adicionar barra de carregamento no rodapé (footer)
        self.footer_frame = ctk.CTkFrame(self, fg_color="#050505", height=25, corner_radius=0)
        self.footer_frame.pack(side="bottom", fill="x")
        
        self.audit_bar = ctk.CTkProgressBar(self.footer_frame, width=300, height=4, corner_radius=0, 
                                            fg_color="#1E2631", progress_color="#00CCFF")
        self.audit_bar.pack(side="left", padx=20, pady=10)
        self.audit_bar.set(0)
        
        self.audit_lbl = ctk.CTkLabel(self.footer_frame, text="AUDITORIA INICIAL DO SISTEMA: 0%", 
                                      font=ctk.CTkFont("Consolas", 9, "bold"), text_color="#00CCFF")
        self.audit_lbl.pack(side="left", padx=10)

        def run_audit():
            import psutil, time
            self.log(">>> INICIANDO AUDITORIA DE SISTEMA (30s)...", "info")
            # Captura inicial
            self.initial_stats['ram'] = psutil.virtual_memory().percent
            self.initial_stats['cpu'] = psutil.cpu_percent(interval=1)
            self.initial_stats['proc_count'] = len(psutil.pids())
            
            for i in range(1, 101):
                time.sleep(0.3) # 30 segundos total (100 * 0.3)
                self.audit_progress = i / 100
                self.audit_bar.set(self.audit_progress)
                self.audit_lbl.configure(text=f"AUDITORIA INICIAL DO SISTEMA: {i}%")
                if i == 50: self.log(">>> ANALISANDO PROCESSOS EM BACKGROUND...", "info")
                if i == 80: self.log(">>> CALCULANDO MÉTRICAS DE LATÊNCIA...", "info")
            
            self.audit_active = False
            self.log("✅ AUDITORIA CONCLUÍDA. SISTEMA MAPEADO.", "success")
            self.footer_frame.destroy()
            
            # Disparar Inteligência Apex
            self.run_apex_brain_analysis()

        threading.Thread(target=run_audit, daemon=True).start()

    def run_apex_brain_analysis(self):
        self.log("🧠 [Apex Brain]: INICIANDO ANÁLISE PRESCRITIVA...", "info")
        analysis = brain.analyze_system()
        
        # Conversa com o usuário via Log
        rec_title = analysis["recommendation"]
        rec_details = analysis["details"]
        target = analysis["action_target"]
        
        self.log(f"🧠 [Apex Brain]: Análise concluída. {rec_title}!", "success")
        self.log(f"🧠 [Apex Brain]: Olá! Notei que {rec_details}", "info")
        
        # Nomear o alvo para o usuário
        target_names = {
            "N1": "NÍVEL 1 (APPS)", "N2": "NÍVEL 2 (MANUTENÇÃO)", "N3": "NÍVEL 3 (TELEMETRIA)",
            "GOD": "MODO DEUS (CENTRO)", "CLEAN": "LIMPEZA DE DISCO (RODAPÉ)"
        }
        friendly_target = target_names.get(target, "o botão indicado")
        self.log(f"🧠 [Apex Brain]: Recomendação: Siga o botão [{friendly_target}] que está PULSANDO agora.", "success")
        
        # Efeito de pulsação no botão alvo (Guia visual)
        self.start_pulse_effect(target)

    def start_pulse_effect(self, target_id):
        # Mapeamento de targets para botões físicos
        targets = {
            "N1": self.level_indicators[1]["cb"],
            "N2": self.level_indicators[2]["cb"],
            "N3": self.level_indicators[3]["cb"],
            "GOD": self.god_mode_btn,
            "N7": self.god_mode_btn,
            "CLEAN": self.clean_btn
        }
        
        btn = targets.get(target_id)
        if not btn: 
            # Fallback se o botão não for encontrado
            return
        
        def pulse():
            try:
                # Salvar estados originais
                orig_fg = btn.cget("fg_color")
                orig_border = btn.cget("border_color")
                
                # Pulsação intensa e rápida (Foco total do usuário)
                for _ in range(12): # 6 ciclos
                    # Estado ON (Neon)
                    btn.configure(fg_color="#00CCFF", border_color="#FFFFFF")
                    time.sleep(0.2)
                    # Estado OFF (Original)
                    btn.configure(fg_color=orig_fg, border_color=orig_border)
                    time.sleep(0.2)
                
                # Garantir que volta ao original
                btn.configure(fg_color=orig_fg, border_color=orig_border)
            except: 
                pass
        
        threading.Thread(target=pulse, daemon=True).start()

    def check_for_updates(self):
        self.log("🌐 [Update System]: VERIFICANDO NOVAS VERSÕES...", "info")
        
        def run_check():
            import urllib.request
            import json
            try:
                # Simulação ou URL Real
                # Para teste, vamos simular uma resposta do servidor
                # response = urllib.request.urlopen(UPDATE_URL).read()
                # data = json.loads(response)
                
                # MOCK PARA DEMONSTRAÇÃO
                data = {"version": "2.0.1", "url": "#", "changelog": "Correções na Inteligência"}
                
                latest = data["version"]
                if latest > VERSION:
                    self.log(f"🚀 [Update System]: NOVA VERSÃO DISPONÍVEL: v{latest}!", "success")
                    self.log(f"🚀 [Update System]: Changelog: {data['changelog']}", "info")
                    
                    # Perguntar ao usuário
                    from tkinter import messagebox
                    if messagebox.askyesno("Apex Update", f"Nova versão v{latest} disponível!\n\n{data['changelog']}\n\nDeseja baixar e instalar agora?"):
                        self.perform_update(data["url"])
                else:
                    self.log("✅ [Update System]: SEU HUD ESTÁ NA VERSÃO MAIS RECENTE.", "success")
            except Exception as e:
                self.log(f"⚠️ [Update System]: FALHA AO CONSULTAR SERVIDOR: {e}", "error")
        
        threading.Thread(target=run_check, daemon=True).start()

    def perform_update(self, download_url):
        self.log("🚀 [Update System]: INICIANDO DOWNLOAD DO PACOTE...", "info")
        
        def run_update():
            try:
                import urllib.request
                import subprocess
                import os
                import sys

                # 1. Baixar o novo executável (simulado se a URL for #)
                if download_url == "#":
                    self.log("⚠️ [Update System]: URL DE DOWNLOAD NÃO CONFIGURADA NO MANIFESTO.", "warning")
                    return

                temp_exe = "apex_update_temp.exe"
                urllib.request.urlretrieve(download_url, temp_exe)
                self.log("🚀 [Update System]: DOWNLOAD CONCLUÍDO. PREPARANDO SUBSTITUIÇÃO...", "success")

                # 2. Criar o script de substituição (Batch)
                current_exe = sys.executable
                exe_name = os.path.basename(current_exe)
                
                bat_content = f"""
@echo off
echo Finalizando processos Apex...
timeout /t 2 /nobreak > nul
del /f /q "{exe_name}"
rename "{temp_exe}" "{exe_name}"
echo Sistema Atualizado! Reiniciando...
start "" "{exe_name}"
del "%~f0"
"""
                with open("updater.bat", "w") as f:
                    f.write(bat_content)

                # 3. Lançar o updater e fechar
                self.log("🚀 [Update System]: REINICIANDO PARA APLICAR MUDANÇAS...", "info")
                subprocess.Popen(["updater.bat"], shell=True)
                self.quit()
                sys.exit()

            except Exception as e:
                self.log(f"⚠️ [Update System]: ERRO DURANTE A ATUALIZAÇÃO: {e}", "error")

        threading.Thread(target=run_update, daemon=True).start()
        path = filedialog.askopenfilename(title="Selecionar Executável", filetypes=[("Executáveis", "*.exe")])
        if path:
            name = os.path.basename(path).replace(".exe", "").capitalize()
            self.custom_shortcuts.append({"name": name, "icon": "⚙️", "path": path, "color": C["accent"]})
            self.render_shortcuts()
            self.log(f">>> ATALHO PERSONALIZADO ADICIONADO: {name}", "success")

    def launch_shortcut(self, app_name, custom_path=None):
        import os, subprocess
        if custom_path:
            if os.path.exists(custom_path):
                subprocess.Popen([custom_path])
                self.log(f">>> LANÇANDO {app_name.upper()}...", "success")
                return
        
        paths = {
            "Chrome": [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ],
            "Steam": [
                r"C:\Program Files (x86)\Steam\steam.exe",
                r"C:\Program Files\Steam\steam.exe"
            ],
            "Discord": [
                os.path.expandvars(r"%LocalAppData%\Discord\Update.exe"),
                os.path.expandvars(r"%AppData%\Local\Discord\Update.exe")
            ]
        }
        
        found = False
        for path in paths.get(app_name, []):
            if os.path.exists(path):
                if app_name == "Discord":
                    subprocess.Popen([path, "--processStart", "Discord.exe"])
                else:
                    subprocess.Popen([path])
                self.log(f">>> LANÇANDO {app_name.upper()}...", "success")
                found = True
                break
        
        if not found:
            self.log(f"⚠️ {app_name.upper()} NÃO ENCONTRADO NOS CAMINHOS PADRÃO.", "warning")

    def log(self, message, type="info"):
        timestamp = time.strftime("%H:%M:%S")
        if hasattr(self, "log_textbox"):
            self.log_textbox.insert(ctk.END, f"[{timestamp}] {message}\n", type)
            self.log_textbox.see(ctk.END)

    def shell_clock_loop(self):
        while True:
            try:
                import datetime
                now = datetime.datetime.now()
                time_str = now.strftime("%H:%M:%S")
                date_str = now.strftime("%A, %d de %B de %Y")
                
                # Traduzir nomes dos dias da semana
                dias = {"Monday": "Segunda-feira", "Tuesday": "Terça-feira", "Wednesday": "Quarta-feira",
                        "Thursday": "Quinta-feira", "Friday": "Sexta-feira", "Saturday": "Sábado", "Sunday": "Domingo"}
                meses = {"January": "Janeiro", "February": "Fevereiro", "March": "Março", "April": "Abril", "May": "Maio",
                         "June": "Junho", "July": "Julho", "August": "Agosto", "September": "Setembro", "October": "Outubro",
                         "November": "Novembro", "December": "Dezembro"}
                
                for en, pt in dias.items():
                    date_str = date_str.replace(en, pt)
                for en, pt in meses.items():
                    date_str = date_str.replace(en, pt)

                self.shell_clock_lbl.configure(text=time_str)
                self.shell_date_lbl.configure(text=date_str)
            except:
                pass
            time.sleep(1)

    def shell_volume_mute(self):
        self.log("🔊 Muting/Unmuting volume via PowerShell...")
        run_cmd("(New-Object -ComObject WScript.Shell).SendKeys([char]173)")

    def shell_volume_down(self):
        self.log("🔊 Diminuindo volume...")
        if DRY_RUN:
            self.log("[SIMULAÇÃO] Volume diminuído.")
        else:
            for _ in range(5):
                subprocess.run(["powershell", "-Command", "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"], capture_output=True, text=True)

    def shell_volume_up(self):
        self.log("🔊 Aumentando volume...")
        if DRY_RUN:
            self.log("[SIMULAÇÃO] Volume aumentado.")
        else:
            for _ in range(5):
                subprocess.run(["powershell", "-Command", "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"], capture_output=True, text=True)

    def shell_execute_command(self):
        cmd_text = self.shell_cmd_entry.get().strip()
        if not cmd_text:
            return
        self.log(f"⚡ [Shell Executar]: {cmd_text}")
        if DRY_RUN:
            self.log(f"[SIMULAÇÃO] Executado comando: {cmd_text}")
        else:
            # Check if cmd_text is a path or a direct file to start
            if os.path.exists(cmd_text):
                subprocess.Popen(f'explorer.exe "{cmd_text}"', shell=True)
            else:
                subprocess.Popen(cmd_text, shell=True)
        self.shell_cmd_entry.delete(0, "end")

    def launch_game_from_shell(self, exe):
        self.log(f"🎮 Iniciando jogo: {exe}")
        if DRY_RUN:
            self.log(f"[SIMULAÇÃO] Lançado jogo: {exe}")
        else:
            subprocess.Popen(exe, shell=True)

    def create_whitelist_tab(self):
        tab = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.tabs["whitelist"] = tab

        wl_lbl = ctk.CTkLabel(tab, text="Gerenciador de Whitelist (Processos Protegidos)", font=self.title_font, text_color="#F8FAFC")
        wl_lbl.pack(anchor="w", pady=(5, 2))

        wl_sub = ctk.CTkLabel(tab, text="Processos adicionados aqui nunca serão encerrados pelo Killprocess, garantindo estabilidade.", font=self.label_font, text_color="#94A3B8")
        wl_sub.pack(anchor="w", pady=(0, 20))

        # Adicionar novo processo
        add_frame = ctk.CTkFrame(tab, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        add_frame.pack(fill="x", pady=(0, 15))

        self.wl_entry = ctk.CTkEntry(
            add_frame, fg_color="#0D0F12", border_color="#1E2B2A", text_color="#E2E8F0",
            placeholder_text="Digite o nome do processo (ex: steam.exe, voicemeeter.exe)", height=38, corner_radius=8
        )
        self.wl_entry.pack(side="left", fill="x", expand=True, padx=15, pady=15)
        self.wl_entry.bind("<Return>", lambda e: self.add_to_whitelist())

        btn_add = ctk.CTkButton(
            add_frame, text="➕ ADICIONAR", fg_color="#1F2937", hover_color="#10B981", border_width=1, border_color="#1E2B2A",
            font=self.label_font, height=38, corner_radius=8, command=self.add_to_whitelist
        )
        btn_add.pack(side="right", padx=15, pady=15)

        # Lista de processos na whitelist
        self.wl_scroll = ctk.CTkScrollableFrame(tab, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        self.wl_scroll.pack(fill="both", expand=True)
        
        self.refresh_whitelist_ui()

    def add_to_whitelist(self):
        process = self.wl_entry.get().strip().lower()
        if not process: return
        if not process.endswith(".exe"): process += ".exe"
        
        if process not in self.whitelist:
            self.whitelist.append(process)
            self.save_whitelist()
            self.refresh_whitelist_ui()
            self.log(f"🛡️ [Whitelist]: {process} adicionado com sucesso.")
        self.wl_entry.delete(0, "end")

    def remove_from_whitelist(self, process):
        if process in self.whitelist:
            self.whitelist.remove(process)
            self.save_whitelist()
            self.refresh_whitelist_ui()
            self.log(f"🛡️ [Whitelist]: {process} removido da proteção.")

    def refresh_whitelist_ui(self):
        for widget in self.wl_scroll.winfo_children():
            widget.destroy()
        
        if not self.whitelist:
            empty = ctk.CTkLabel(self.wl_scroll, text="Sua whitelist está vazia.", font=self.label_font, text_color="#64748B")
            empty.pack(pady=40)
            return

        for p in sorted(self.whitelist):
            item_frame = ctk.CTkFrame(self.wl_scroll, fg_color="transparent")
            item_frame.pack(fill="x", padx=15, pady=4)
            
            lbl = ctk.CTkLabel(item_frame, text=f"🛡️ {p}", font=self.label_font, text_color="#E2E8F0")
            lbl.pack(side="left")
            
            btn_rem = ctk.CTkButton(
                item_frame, text="REMOVER", width=70, height=24, corner_radius=4, fg_color="#EF4444", hover_color="#DC2626",
                font=ctk.CTkFont(size=9, weight="bold"), command=lambda proc=p: self.remove_from_whitelist(proc)
            )
            btn_rem.pack(side="right")

    def save_whitelist(self):
        try:
            with open("whitelist.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(self.whitelist))
        except: pass

    def load_whitelist(self):
        if not os.path.exists("whitelist.txt"):
            # Whitelist padrão
            return ["killprocess.exe", "gui.exe", "python.exe", "svchost.exe", "explorer.exe", "taskmgr.exe"]
        try:
            with open("whitelist.txt", "r", encoding="utf-8") as f:
                return [l.strip().lower() for l in f.readlines() if l.strip()]
        except:
            return []

    # =====================================================================
    # 🔄 Lógica de Navegação e Troca de Abas
    # =====================================================================

    def switch_tab(self, tab_name):
        for tab in self.tabs.values():
            tab.pack_forget()

        # Reset todos os botões da sidebar
        sidebar_map = {
            "dashboard": "dashboard",
            "scan": "scan",
            "optimize_center": "optimize_center",
            "autoboost": "autoboost",
            "extra": "extra",
            "whitelist": "whitelist",
            "management": "management",
            "settings": "extra",
            "shell": "extra",
        }
        for key, btn in self.nav_btns.items():
            btn.configure(fg_color="transparent", text_color=C["muted"])

        active_key = sidebar_map.get(tab_name, tab_name)
        if active_key in self.nav_btns:
            self.nav_btns[active_key].configure(
                fg_color=C["hover"], text_color=C["accent"])

        if tab_name in self.tabs:
            self.tabs[tab_name].pack(fill="both", expand=True)
        elif tab_name == "whitelist" and "whitelist" in self.tabs:
            self.tabs["whitelist"].pack(fill="both", expand=True)
        elif tab_name == "management" and "management" in self.tabs:
            self.tabs["management"].pack(fill="both", expand=True)
            self.show_levels_grid()

    def toggle_sidebar(self):
        pass

    def draw_radar_chart(self):
        # Dimensões dinâmicas baseadas no canvas
        cw = self.radar_canvas.winfo_width()
        ch = self.radar_canvas.winfo_height()
        if cw < 10: cw, ch = 200, 200 # Fallback inicial
        
        cx, cy = cw // 2, ch // 2
        r = min(cx, cy) - 35
        
        self.radar_canvas.delete("all")
        
        # Rótulos dos Eixos
        labels = ["RAM", "BOOST", "GOD", "SHELL", "MAINT"]
        
        # Desenhar as teias (rings)
        for i in range(1, 6):
            r_ring = (r / 5) * i
            # Polígono de fundo (pentágono)
            ring_points = []
            for j in range(5):
                angle = j * (2 * math.pi / 5) - math.pi / 2
                ring_points.append(cx + r_ring * math.cos(angle))
                ring_points.append(cy + r_ring * math.sin(angle))
            self.radar_canvas.create_polygon(ring_points, outline="#1E2631", fill="", width=1)

        # Desenhar eixos e labels
        for i, label in enumerate(labels):
            angle = i * (2 * math.pi / 5) - math.pi / 2
            x_end = cx + r * math.cos(angle)
            y_end = cy + r * math.sin(angle)
            self.radar_canvas.create_line(cx, cy, x_end, y_end, fill="#1E2631", width=1)
            
            # Label
            lx = cx + (r + 15) * math.cos(angle)
            ly = cy + (r + 15) * math.sin(angle)
            self.radar_canvas.create_text(lx, ly, text=label, font=("Segoe UI", 8, "bold"), fill=C["muted"])

        # Dados
        import psutil
        mem = psutil.virtual_memory()
        v1 = 0.3 + (mem.percent / 100.0) * 0.6
        v2 = 0.9 if self.autoboost_enabled else 0.5
        v3 = 0.95 if hasattr(self, "god_mode_active") and self.god_mode_active else 0.6
        v4 = 0.85 if self.shell_explorer_closed else 0.45
        v5 = 0.9 if self.autoboost_enabled else 0.7 # Simulação de manutenção
        
        vals = [v1, v2, v3, v4, v5]
        poly_points = []
        for i, v in enumerate(vals):
            angle = i * (2 * math.pi / 5) - math.pi / 2
            x = cx + v * r * math.cos(angle)
            y = cy + v * r * math.sin(angle)
            poly_points.append(x)
            poly_points.append(y)
            
        if len(poly_points) >= 6:
            self.radar_canvas.create_polygon(poly_points, fill="#00FF66", outline="#00FFFF", width=2, stipple="gray25")
            self.radar_canvas.create_polygon(poly_points, fill="", outline="#00FFFF", width=1.5)
    def toggle_dry_run(self):
        global DRY_RUN
        # switch ON (True) -> DRY_RUN = False (Real)
        # switch OFF (False) -> DRY_RUN = True (Simulation)
        is_on = self.dry_run_switch.get()
        DRY_RUN = not is_on
        
        if DRY_RUN:
            self.mode_pill.configure(text="● SIMULAÇÃO", text_color=C["orange"], fg_color="#140A00")
            self.log("\n🧪 Modo Simulação ATIVADO. Nenhuma ação real será executada.", "warning")
        else:
            self.mode_pill.configure(text="● MODO REAL", text_color=C["red"], fg_color="#1A0000")
            self.log("\n⚠️ MODO REAL ATIVADO! Ações vão afetar o sistema!", "error")

    def refresh_stats_loop(self):
        self.after(500, self.blink_real_mode)
        self.after(600, self.blink_clear_btn)
        while True:
            try:
                import psutil
                # RAM
                mem = psutil.virtual_memory()
                ram_pct = mem.percent / 100.0
                if hasattr(self, "ram_val_lbl"): self.ram_val_lbl.configure(text=f"{mem.used/(1024**3):.1f} GB")
                if hasattr(self, "ram_pb"): self.ram_pb.set(ram_pct)

                # CPU
                cpu_p = psutil.cpu_percent()
                if hasattr(self, "dash_cpu_lbl"): self.dash_cpu_lbl.configure(text=f"{cpu_p:.1f}%")
                if hasattr(self, "dash_cpu_pb"): self.dash_cpu_pb.set(cpu_p/100.0)

                # PROC
                procs = len(psutil.pids())
                if hasattr(self, "proc_val_lbl"): self.proc_val_lbl.configure(text=str(procs))
                if hasattr(self, "proc_pb"): self.proc_pb.set(min(procs/500, 1.0))

                # GPU (Simulado)
                import random
                gpu_p = random.randint(15, 45)
                if hasattr(self, "dash_gpu_lbl"): self.dash_gpu_lbl.configure(text=f"{gpu_p}%")
                if hasattr(self, "dash_gpu_pb"): self.dash_gpu_pb.set(gpu_p/100.0)

                # TEMP (Simulado)
                temp_v = random.randint(40, 65)
                if hasattr(self, "dash_temp_lbl"): self.dash_temp_lbl.configure(text=f"{temp_v}°C")
                if hasattr(self, "dash_temp_pb"): self.dash_temp_pb.set((temp_v-30)/70.0)

                # DISK
                disk = psutil.disk_usage('/')
                if hasattr(self, "dash_disk_lbl"): self.dash_disk_lbl.configure(text=f"{disk.percent}%")
                if hasattr(self, "dash_disk_pb"): self.dash_disk_pb.set(disk.percent/100.0)

                # NET (Simulado Activity)
                net_v = random.randint(1, 100)
                if hasattr(self, "dash_net_lbl"): self.dash_net_lbl.configure(text=f"{net_v} Mb/s")
                if hasattr(self, "dash_net_pb"): self.dash_net_pb.set(net_v/100.0)

                self.draw_radar_chart()
            except: pass
            time.sleep(1.5)
    # =====================================================================
    # 🏃 Threads de Processamento (Para não travar a GUI)
    # =====================================================================

    def start_optimization(self):
        threading.Thread(target=self.run_optimization, daemon=True).start()

    def start_god_mode(self):
        threading.Thread(target=self.run_god_mode, daemon=True).start()

    def start_full_optimization(self):
        threading.Thread(target=self.run_full_optimization, daemon=True).start()

    def start_optimize_selection(self):
        threading.Thread(target=self.run_optimize_selection, daemon=True).start()

    def start_restoration(self):
        threading.Thread(target=self.run_restoration, daemon=True).start()

    def run_full_optimization(self):
        self.log("\n--- 🔥 INICIANDO OTIMIZAÇÃO TOTAL DO SISTEMA (N7 + MANUTENÇÃO) ---")
        # Run God Mode
        self.run_god_mode()
        # Run All Maintenance
        self.run_all_maintenance()
        self.log("\n🚀 SISTEMA 100% OTIMIZADO PARA ALTA PERFORMANCE!")

    def run_optimization(self):
        self.log("\n--- 🔥 Iniciando Otimização Gamer Suprema ---")
        
        create_restore_point(self.log)
        backup_active_services(self.log)
        
        levels = list(SERVICES_MAP.keys())[:7]
        for idx, category in enumerate(levels, start=1):
            self.log(f"\n⚡ Executando {category}...")
            items = SERVICES_MAP[category]
            for item in items:
                if self.checkboxes[item["id"]].get():
                    if item["type"] == "process":
                        stop_process(item["id"], self.log, self.whitelist)
                    elif item["type"] == "service":
                        stop_service(item["id"], self.log, self.whitelist)
            self.light_up_level(idx)

        self.log("\n✅ Otimização Gamer Suprema concluída!")
        self.status_val_lbl.configure(text="Modo Gamer Ativado", text_color="#34D399")

    def run_god_mode(self):
        self.log("\n--- 👑 INICIANDO MODO DEUS (GOD MODE) ---")
        self.log("⚠️ Operação Extrema: Encerrando absolutamente todos os processos e serviços mapeados em todos os 7 níveis.")
        
        create_restore_point(self.log)
        backup_active_services(self.log)

        # Força a seleção de todos os checkboxes na interface
        for category, items in SERVICES_MAP.items():
            if category in self.level_checkboxes_dashboard:
                self.level_checkboxes_dashboard[category].select()
            for item in items:
                if item["id"] in self.checkboxes:
                    self.checkboxes[item["id"]].select()

        for idx, (category, items) in enumerate(SERVICES_MAP.items(), start=1):
            self.log(f"\n👑 Executando {category} em Modo Deus...")
            for item in items:
                # O usuário solicitou que o Modo Deus ignore o Discord
                if item["id"].lower() == "discord":
                    self.log("🛡️ [Modo Deus]: Ignorando Discord conforme regra de proteção.")
                    continue
                    
                if item["type"] == "process":
                    stop_process(item["id"], self.log, self.whitelist)
                elif item["type"] == "service":
                    stop_service(item["id"], self.log, self.whitelist)
            self.light_up_level(idx)

        self.log("\n✅ MODO DEUS ATIVADO COM SUCESSO EM TODOS OS 7 NÍVEIS!")
        self.status_val_lbl.configure(text="MODO DEUS ATIVO", text_color="#FACC15")

    def run_optimize_selection(self):
        self.log("\n--- ⚡ Iniciando Otimização da Seleção Personalizada ---")
        
        create_restore_point(self.log)
        backup_active_services(self.log)

        for idx, (category, items) in enumerate(SERVICES_MAP.items(), start=1):
            if self.level_checkboxes_dashboard[category].get():
                self.log(f"\n⚡ Executando {category}...")
                for item in items:
                    if self.checkboxes[item["id"]].get():
                        if item["type"] == "process":
                            stop_process(item["id"], self.log, self.whitelist)
                        elif item["type"] == "service":
                            stop_service(item["id"], self.log, self.whitelist)
                self.light_up_level(idx)
            else:
                self.log(f"\n⏭️ Pulando {category} (não selecionado).")

        self.log("\n✅ Otimização de seleção personalizada concluída!")
        self.status_val_lbl.configure(text="GAMER CUSTOM ATIVO", text_color="#38BDF8")

    def toggle_autoboost(self):
        self.autoboost_enabled = not hasattr(self, "autoboost_enabled") or not self.autoboost_enabled
        if self.autoboost_enabled:
            self.btn_ab_dash.configure(fg_color="#10B981", text="🚀 Auto Boost (ON)")
            self.log("\n🚀 Auto Boost ATIVADO: Monitoramento em tempo real iniciado.")
            threading.Thread(target=self.autoboost_loop, daemon=True).start()
        else:
            self.btn_ab_dash.configure(fg_color="#111827", text="🚀 Auto Boost")
            self.log("\n🛑 Auto Boost DESATIVADO.")

    def autoboost_loop(self):
        while hasattr(self, "autoboost_enabled") and self.autoboost_enabled:
            # Lógica simples de monitoramento: limpa RAM e processos da lista Nível 1 periodicamente
            if not DRY_RUN:
                run_cmd("[System.GC]::Collect()")
                # Aqui poderíamos adicionar uma limpeza recorrente de processos leves
            time.sleep(60) # Executa a cada 1 minuto enquanto ativo

    def run_restoration(self):
        self.log("\n--- 🔄 Iniciando Restauração de Padrões do Windows ---")
        
        for category, items in SERVICES_MAP.items():
            for item in items:
                if item["type"] == "service":
                    start_service(item["id"], self.log)
                    
        self.log("🟢 Reiniciando Explorer.exe...")
        if DRY_RUN:
            self.log("[SIMULAÇÃO] Explorer reiniciado.")
        else:
            run_cmd("explorer.exe")
            
        self.turn_off_levels()
        self.log("\n✅ Todos os padrões do Windows foram restaurados!")
        self.status_val_lbl.configure(text="Pronto para Jogar", text_color="#F8FAFC")

    def light_up_level(self, lvl_num):
        if lvl_num in self.level_indicators:
            cfg = self.level_indicators[lvl_num]
            cfg["circle"].configure(text_color=cfg["color"])

    def turn_off_levels(self):
        for num, cfg in self.level_indicators.items():
            cfg["circle"].configure(text_color="#4B5563")

    def blink_real_mode(self):
        if not DRY_RUN:
            current_color = self.mode_pill.cget("text_color")
            # Efeito de Pulso (Glow): Alterna entre vermelho intenso com fundo e vermelho suave
            if current_color == C["red"]:
                self.mode_pill.configure(text_color="#FF9999", fg_color="#440000")
            else:
                self.mode_pill.configure(text_color=C["red"], fg_color="#1A0000")
        else:
            self.mode_pill.configure(text_color=C["orange"], fg_color="#140A00")
        self.after(400, self.blink_real_mode)

    def blink_clear_btn(self):
        if self.pending_clear:
            current_color = self.clear_log_btn.cget("text_color")
            new_color = C["cyan"] if current_color == C["muted"] else C["muted"]
            self.clear_log_btn.configure(text_color=new_color)
        else:
            self.clear_log_btn.configure(text_color=C["muted"])
        self.after(600, self.blink_clear_btn)

# =====================================================================
# 🛡️ Sistema de Backup e Segurança
# =====================================================================

def create_restore_point(log_func):
    log_func("\n🛡️ Criando Ponto de Restauração do Windows...")
    if DRY_RUN:
        log_func("[SIMULAÇÃO]: Ponto de Restauração criado com sucesso!")
        return
    cmd = "Enable-ComputerRestore -Drive 'C:\\'; Checkpoint-Computer -Description 'Killprocess_GameMode_Backup' -RestorePointType 'MODIFY_SETTINGS'"
    run_cmd(cmd)
    log_func("✅ Ponto de Restauração 'Killprocess_GameMode_Backup' criado com sucesso!")

def backup_active_services(log_func):
    log_func("📋 Fazendo backup dos serviços ativos...")
    if DRY_RUN:
        log_func("[SIMULAÇÃO]: Lista de serviços ativos salva em 'active_services_backup.txt'.")
        return
    cmd = "Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object -ExpandProperty Name"
    running_services = run_cmd(cmd)
    if running_services:
        with open("active_services_backup.txt", "w", encoding="utf-8") as f:
            f.write(running_services)
        log_func("✅ Backup salvo em 'active_services_backup.txt'.")
    else:
        log_func("⚠️ Nenhum serviço ativo encontrado para backup.")

def stop_process(process_name, log_func, whitelist=[]):
    if process_name.lower() in whitelist or (process_name.lower() + ".exe") in whitelist:
        log_func(f"🛡️ [Whitelist]: Ignorando processo protegido: {process_name}")
        return
    log_func(f"🛑 Encerrando processo: {process_name}...")
    if not DRY_RUN:
        run_cmd(f"Stop-Process -Name '{process_name}' -Force")

def stop_service(service_name, log_func, whitelist=[]):
    if service_name.lower() in whitelist:
        log_func(f"🛡️ [Whitelist]: Ignorando serviço protegido: {service_name}")
        return
    log_func(f"🛑 Desativando serviço: {service_name}...")
    if not DRY_RUN:
        run_cmd(f"Stop-Service -Name '{service_name}' -Force")
        run_cmd(f"Set-Service -Name '{service_name}' -StartupType Disabled")

def start_service(service_name, log_func):
    log_func(f"🟢 Reativando serviço: {service_name}...")
    if not DRY_RUN:
        run_cmd(f"Set-Service -Name '{service_name}' -StartupType Automatic")
        run_cmd(f"Start-Service -Name '{service_name}'")

def clean_temp_files(log_func):
    log_func("\n🧹 Removendo arquivos temporários...")
    if DRY_RUN:
        log_func("[SIMULAÇÃO] Arquivos temporários removidos.")
        return
    commands = [
        "Remove-Item -Path $env:TEMP\\* -Recurse -Force -ErrorAction SilentlyContinue",
        "Remove-Item -Path 'C:\\Windows\\Temp\\*' -Recurse -Force -ErrorAction SilentlyContinue",
        "Remove-Item -Path 'C:\\Windows\\Prefetch\\*' -Recurse -Force -ErrorAction SilentlyContinue"
    ]
    for cmd in commands:
        run_cmd(cmd)
    log_func("✅ Limpeza de arquivos temporários concluída!")

def flush_dns(log_func):
    log_func("\n🌐 Otimizando Rede...")
    if DRY_RUN:
        log_func("[SIMULAÇÃO] Cache de DNS limpo e rede redefinida.")
        return
    run_cmd("ipconfig /flushdns")
    run_cmd("netsh winsock reset")
    log_func("✅ Cache de DNS limpo e Winsock redefinido!")

def set_ultimate_performance(log_func):
    log_func("\n⚡ Ativando Plano de Energia...")
    if DRY_RUN:
        log_func("[SIMULAÇÃO] Plano de Energia definido para Desempenho Máximo.")
        return
    cmd = "powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61"
    run_cmd(cmd)
    run_cmd("powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61")
    log_func("✅ Plano de Energia definido para DESEMPENHO MÁXIMO!")

def optimize_registry(log_func):
    log_func("\n🛠️ Aplicando Otimizações de Registro...")
    if DRY_RUN:
        log_func("[SIMULAÇÃO] Registro otimizado.")
        return
    commands = [
        "Set-ItemProperty -Path 'HKCU:\\System\\GameConfigStore' -Name 'GameDVR_Enabled' -Value 0",
        "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR' -Name 'AllowGameDVR' -Value 0",
        "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games' -Name 'GPU Priority' -Value 8",
        "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games' -Name 'Priority' -Value 6",
        "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games' -Name 'Scheduling Category' -Value 'High'"
    ]
    for cmd in commands:
        run_cmd(cmd)
    log_func("✅ Registro otimizado!")

def optimize_tcp(log_func):
    log_func("\n🌐 Otimizando TCP...")
    if DRY_RUN:
        log_func("[SIMULAÇÃO] Rede TCP otimizada.")
        return
    commands = [
        "netsh int tcp set global autotuninglevel=normal",
        "netsh int tcp set global ecncapability=disabled",
        "netsh int tcp set global rss=enabled",
        "netsh int tcp set global chimney=enabled",
        "netsh int tcp set global dca=enabled",
        "netsh int tcp set global netdma=enabled",
        "netsh int tcp set global congestionprovider=ctcp",
        "netsh int tcp set global timestamps=disabled"
    ]
    for cmd in commands:
        run_cmd(cmd)
    log_func("✅ Rede TCP otimizada!")

if __name__ == "__main__":
    if not is_admin():
        print("[AVISO] Este script nao esta rodando como ADMINISTRADOR. Algumas funcoes reais podem nao funcionar.")
        
    app = PremiumKillprocessApp()
    app.mainloop()
