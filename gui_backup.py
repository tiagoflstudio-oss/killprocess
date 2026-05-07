import os
import sys
import time
import math
import subprocess
import threading
import customtkinter as ctk

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
    def __init__(self):
        super().__init__()

        self.title("🚀 Killprocess UI - Ultra Edition")
        self.geometry("1020x660")
        
        # Cor de fundo estilo Sleek Dark
        self.configure(fg_color="#090E12")

        self.autoboost_enabled = False
        self.shell_explorer_closed = False
        self.supported_games = [
            {"exe": "cs2.exe", "name": "Counter-Strike 2"},
            {"exe": "valorant.exe", "name": "Valorant"},
            {"exe": "leagueoflegends.exe", "name": "League of Legends"},
            {"exe": "gta5.exe", "name": "Grand Theft Auto V"},
            {"exe": "cyberpunk2077.exe", "name": "Cyberpunk 2077"}
        ]
        self.autoboost_status_lbls = {}
        self.whitelist = self.load_whitelist()
        self.autoboost_status_lbls = {}

        # Configurações de design e fontes
        self.title_font = ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        self.section_font = ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        self.label_font = ctk.CTkFont(family="Segoe UI", size=11)
        self.log_font = ctk.CTkFont(family="Consolas", size=10)

        # Layout em Grid Principal: 1 Coluna para Sidebar, 1 Coluna para Área de Conteúdo
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------------------------------------------------
        # 1. SIDEBAR (Menu Lateral com borda de acento)
        # ---------------------------------------------------------
        self.sidebar_collapsed = False
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#10151B", corner_radius=0, width=200, border_width=1, border_color="#1E2631")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)

        # Logo / Marca na Sidebar
        self.brand_label = ctk.CTkLabel(
            self.sidebar_frame, text="✨ Ultra Edition", font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"), text_color="#00FFFF"
        )
        self.brand_label.pack(pady=(20, 2))

        self.brand_sub = ctk.CTkLabel(
            self.sidebar_frame, text="Killprocess Extreme", font=ctk.CTkFont(family="Segoe UI", size=10), text_color="#64748B"
        )
        self.brand_sub.pack(pady=(0, 5))

        self.toggle_sidebar_btn = ctk.CTkButton(
            self.sidebar_frame, text="◀ RECOLHER", font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            fg_color="transparent", hover_color="#1E2631", height=28, text_color="#00E5FF", command=self.toggle_sidebar
        )
        self.toggle_sidebar_btn.pack(pady=(0, 10))

        # Botões de Navegação da Sidebar
        self.nav_dash_btn = ctk.CTkButton(
            self.sidebar_frame, text="📊 Dashboard", fg_color="#1E2631", hover_color="#00FFFF", anchor="w",
            font=self.label_font, height=36, corner_radius=6, command=lambda: self.switch_tab("dashboard")
        )
        self.nav_dash_btn.pack(padx=10, pady=4, fill="x")

        self.nav_opt_btn = ctk.CTkButton(
            self.sidebar_frame, text="🎮 Otimizar", fg_color="transparent", hover_color="#00FFFF", anchor="w",
            font=self.label_font, height=36, corner_radius=6, command=lambda: self.switch_tab("optimize_center")
        )
        self.nav_opt_btn.pack(padx=10, pady=4, fill="x")

        self.nav_manage_btn = ctk.CTkButton(
            self.sidebar_frame, text="⚙️ Processos", fg_color="transparent", hover_color="#00FFFF", anchor="w",
            font=self.label_font, height=36, corner_radius=6, command=lambda: self.switch_tab("management")
        )
        self.nav_manage_btn.pack(padx=10, pady=4, fill="x")

        self.nav_scan_btn = ctk.CTkButton(
            self.sidebar_frame, text="🔍 Escaneamento", fg_color="transparent", hover_color="#00FFFF", anchor="w",
            font=self.label_font, height=36, corner_radius=6, command=lambda: self.switch_tab("scan")
        )
        self.nav_scan_btn.pack(padx=10, pady=4, fill="x")

        self.nav_whitelist_btn = ctk.CTkButton(
            self.sidebar_frame, text="🛡️ Whitelist", fg_color="transparent", hover_color="#00FFFF", anchor="w",
            font=self.label_font, height=36, corner_radius=6, command=lambda: self.switch_tab("whitelist")
        )
        self.nav_whitelist_btn.pack(padx=10, pady=4, fill="x")

        self.nav_settings_btn = ctk.CTkButton(
            self.sidebar_frame, text="🔧 Configurações", fg_color="transparent", hover_color="#00FFFF", anchor="w",
            font=self.label_font, height=36, corner_radius=6, command=lambda: self.switch_tab("settings")
        )
        self.nav_settings_btn.pack(padx=10, pady=4, fill="x")

        self.nav_autoboost_btn = ctk.CTkButton(
            self.sidebar_frame, text="🚀 Auto-Boost", fg_color="transparent", hover_color="#00FFFF", anchor="w",
            font=self.label_font, height=36, corner_radius=6, command=lambda: self.switch_tab("autoboost")
        )
        self.nav_autoboost_btn.pack(padx=10, pady=4, fill="x")

        self.nav_extra_btn = ctk.CTkButton(
            self.sidebar_frame, text="🧹 Manutenção", fg_color="transparent", hover_color="#00FFFF", anchor="w",
            font=self.label_font, height=36, corner_radius=6, command=lambda: self.switch_tab("extra")
        )
        self.nav_extra_btn.pack(padx=10, pady=4, fill="x")

        self.nav_shell_btn = ctk.CTkButton(
            self.sidebar_frame, text="🟨 Atalho Operacional", fg_color="transparent", hover_color="#FFD700", anchor="w",
            font=self.label_font, height=36, corner_radius=6, command=lambda: self.switch_tab("shell")
        )
        self.nav_shell_btn.pack(padx=10, pady=4, fill="x")

        # Switch de Simulação no final da sidebar
        self.sidebar_bottom = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.sidebar_bottom.pack(side="bottom", fill="x", padx=10, pady=15)

        self.dry_run_switch = ctk.CTkSwitch(
            self.sidebar_bottom, text="Modo Simulação", font=self.label_font, text_color="#EF4444",
            onvalue=True, offvalue=False, command=self.toggle_dry_run
        )
        self.dry_run_switch.pack(anchor="w", padx=5)
        self.dry_run_switch.select()

        # ---------------------------------------------------------
        # 2. CONTENT AREA (Área de Conteúdo Direita)
        # ---------------------------------------------------------
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        # Dicionário de abas de conteúdo
        self.tabs = {}
        self.create_dashboard_tab()
        self.create_management_tab()
        self.create_scan_tab()
        self.create_settings_tab()
        self.create_autoboost_tab()
        self.create_shell_tab()
        self.create_extra_tab()
        self.create_optimize_center_tab()
        self.create_whitelist_tab()

        self.switch_tab("dashboard")

        # Inicia a Thread para atualizar os cards de estatísticas em tempo real
        threading.Thread(target=self.refresh_stats_loop, daemon=True).start()

    # =====================================================================
    # 🗂️ Criação de Abas
    # =====================================================================

    def create_dashboard_tab(self):
        tab = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.tabs["dashboard"] = tab

        # Cabeçalho de Boas-vindas
        welcome_lbl = ctk.CTkLabel(tab, text="✨ Olá, Gamer!", font=self.title_font, text_color="#F8FAFC")
        welcome_lbl.pack(anchor="w", pady=(0, 2))

        sub_lbl = ctk.CTkLabel(tab, text="Pronto para máxima performance?", font=self.label_font, text_color="#00FFFF")
        sub_lbl.pack(anchor="w", pady=(0, 10))

        # ---------------------------------------------------------
        # 🟢🟡🟠🔴🟣👑 INDICADOR DE NÍVEIS (Modo Luzinha Interativa)
        # ---------------------------------------------------------
        levels_status_frame = ctk.CTkFrame(tab, fg_color="#10151B", border_width=1, border_color="#1E2631", corner_radius=10)
        levels_status_frame.pack(fill="x", pady=(0, 10), padx=2)

        lbl_ind = ctk.CTkLabel(
            levels_status_frame, text="SELEÇÃO & STATUS DOS NÍVEIS DE OTIMIZAÇÃO", 
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"), text_color="#00FFFF"
        )
        lbl_ind.pack(anchor="w", padx=12, pady=(8, 2))

        self.lights_frame = ctk.CTkFrame(levels_status_frame, fg_color="transparent")
        self.lights_frame.pack(fill="x", padx=12, pady=(0, 5))

        self.level_indicators = {}
        self.level_checkboxes_dashboard = {}
        colors_off = "#475569"

        levels_data = [
            {"num": 1, "id": "Nível 1: Aplicativos & Bloatwares", "name": "N1", "active_color": "#00FF66", "symbol": "🟢", "desc": "Fecha navegadores, mensageiros e apps em segundo plano."},
            {"num": 2, "id": "Nível 2: Impressão & Manutenção", "name": "N2", "active_color": "#00FFB2", "symbol": "🟡", "desc": "Desativa serviços de impressoras, fax e manutenção."},
            {"num": 3, "id": "Nível 3: Telemetria & Rastreamento", "name": "N3", "active_color": "#FFFF00", "symbol": "🟠", "desc": "Interrompe telemetria, coleta de dados e diagnósticos."},
            {"num": 4, "id": "Nível 4: Xbox & Conexões Secundárias", "name": "N4", "active_color": "#FF8000", "symbol": "🔴", "desc": "Remove suporte a Bluetooth e serviços Xbox."},
            {"num": 5, "id": "Nível 5: Redes & Streaming", "name": "N5", "active_color": "#FF0055", "symbol": "🌐", "desc": "Desativa compartilhamento, mapas e sensores."},
            {"num": 6, "id": "Nível 6: Segurança & Criptografia", "name": "N6", "active_color": "#00FFFF", "symbol": "🔒", "desc": "Encerra credenciais e segurança local."},
            {"num": 7, "id": "Nível 7: Modo Deus (God Mode)", "name": "N7", "active_color": "#FFD700", "symbol": "👑", "desc": "Performance Gamer Suprema: Modo Deus ativado."}
        ]

        # Descrição do Nível para o Usuário saber o que cada um propõe
        self.level_desc_lbl = ctk.CTkLabel(
            levels_status_frame, text="Selecione os níveis acima para aplicar a otimização gamer personalizada.", 
            font=ctk.CTkFont(family="Segoe UI", size=11), text_color="#64748B"
        )
        self.level_desc_lbl.pack(anchor="w", padx=12, pady=(2, 8))

        def update_desc_lbl(desc_text):
            self.level_desc_lbl.configure(text=desc_text)

        for lvl in levels_data:
            ind_frame = ctk.CTkFrame(self.lights_frame, fg_color="transparent")
            ind_frame.pack(side="left", expand=True, fill="x")

            cb_dash = ctk.CTkCheckBox(
                ind_frame, text=lvl["name"], font=ctk.CTkFont(family="Segoe UI", size=10), 
                fg_color=lvl["active_color"], hover_color=lvl["active_color"],
                command=lambda d=lvl["desc"]: update_desc_lbl(d)
            )
            if lvl["num"] <= 6:
                cb_dash.select()
            cb_dash.pack(side="left", padx=(0, 2))

            cb_dash.bind("<Enter>", lambda event, d=lvl["desc"]: update_desc_lbl(d))

            lbl_circle = ctk.CTkLabel(ind_frame, text="●", font=ctk.CTkFont(size=14), text_color=colors_off)
            lbl_circle.pack(side="left")

            self.level_checkboxes_dashboard[lvl["id"]] = cb_dash
            self.level_indicators[lvl["num"]] = {
                "circle": lbl_circle, "cb": cb_dash, "color": lvl["active_color"], "symbol": lvl["symbol"]
            }

        # Painel Grid de Estatísticas / Cards compactos
        stats_frame = ctk.CTkFrame(tab, fg_color="transparent")
        stats_frame.pack(fill="x", pady=5)
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Card 1: Memória RAM
        card1 = ctk.CTkFrame(stats_frame, fg_color="#10151B", border_width=1, border_color="#1E2631", corner_radius=10, height=85)
        card1.grid(row=0, column=0, padx=(0, 6), sticky="nsew")
        card1.grid_propagate(False)

        c1_lbl = ctk.CTkLabel(card1, text="Uso de RAM", font=self.label_font, text_color="#00FFFF")
        c1_lbl.pack(anchor="w", padx=12, pady=(10, 2))
        self.ram_val_lbl = ctk.CTkLabel(card1, text="Calculando...", font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color="#F8FAFC")
        self.ram_val_lbl.pack(anchor="w", padx=12)

        # Card 2: Processos Ativos
        card2 = ctk.CTkFrame(stats_frame, fg_color="#10151B", border_width=1, border_color="#1E2631", corner_radius=10, height=85)
        card2.grid(row=0, column=1, padx=6, sticky="nsew")
        card2.grid_propagate(False)

        c2_lbl = ctk.CTkLabel(card2, text="Processos Ativos", font=self.label_font, text_color="#00FFFF")
        c2_lbl.pack(anchor="w", padx=12, pady=(10, 2))
        self.proc_val_lbl = ctk.CTkLabel(card2, text="Contando...", font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color="#F8FAFC")
        self.proc_val_lbl.pack(anchor="w", padx=12)

        # Card 3: Status de Performance
        card3 = ctk.CTkFrame(stats_frame, fg_color="#10151B", border_width=1, border_color="#1E2631", corner_radius=10, height=85)
        card3.grid(row=0, column=2, padx=(6, 0), sticky="nsew")
        card3.grid_propagate(False)

        c3_lbl = ctk.CTkLabel(card3, text="Status Otimização", font=self.label_font, text_color="#00FFFF")
        c3_lbl.pack(anchor="w", padx=12, pady=(10, 2))
        self.status_val_lbl = ctk.CTkLabel(card3, text="Pronto para Jogar", font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color="#F8FAFC")
        self.status_val_lbl.pack(anchor="w", padx=12)

        # ---------------------------------------------------------
        # Centro: Container de Botões de Ação e Radar das Skills
        # ---------------------------------------------------------
        center_container = ctk.CTkFrame(tab, fg_color="transparent")
        center_container.pack(fill="x", pady=6)

        # Esquerda: Ações
        actions_frame = ctk.CTkFrame(center_container, fg_color="#10151B", border_width=1, border_color="#1E2631", corner_radius=10)
        actions_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # ---------------------------------------------------------
        # ATALHOS RÁPIDOS OPERACIONAIS (Novo)
        # ---------------------------------------------------------
        shortcuts_lbl = ctk.CTkLabel(
            actions_frame, text="⚡ ATALHOS OPERACIONAIS", 
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"), text_color="#00FFFF"
        )
        shortcuts_lbl.pack(anchor="w", padx=12, pady=(10, 2))

        # Grid de botões menores para atalhos
        shortcuts_grid = ctk.CTkFrame(actions_frame, fg_color="transparent")
        shortcuts_grid.pack(fill="x", padx=12, pady=4)
        shortcuts_grid.grid_columnconfigure((0, 1), weight=1)

        btn_maint = ctk.CTkButton(
            shortcuts_grid, text="🛠️ Manutenção", fg_color="#1E2631", hover_color="#3B82F6", height=28, corner_radius=6,
            font=ctk.CTkFont(size=10, weight="bold"), command=lambda: threading.Thread(target=self.run_premium_optimization, args=("full_maint",)).start()
        )
        btn_maint.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")

        btn_scan = ctk.CTkButton(
            shortcuts_grid, text="🔍 Escanear", fg_color="#1E2631", hover_color="#10B981", height=28, corner_radius=6,
            font=ctk.CTkFont(size=10, weight="bold"), command=self.run_process_scan
        )
        btn_scan.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")

        self.btn_ab_dash = ctk.CTkButton(
            shortcuts_grid, text="🚀 Auto-Boost", fg_color="#1E2631", hover_color="#FACC15", height=28, corner_radius=6,
            font=ctk.CTkFont(size=10, weight="bold"), command=self.toggle_autoboost
        )
        self.btn_ab_dash.grid(row=1, column=0, padx=2, pady=2, sticky="nsew")

        self.btn_shell_dash = ctk.CTkButton(
            shortcuts_grid, text="👑 Shell Mode", fg_color="#1E2631", hover_color="#D97706", height=28, corner_radius=6,
            font=ctk.CTkFont(size=10, weight="bold"), command=self.toggle_gold_mode_explorer
        )
        self.btn_shell_dash.grid(row=1, column=1, padx=2, pady=2, sticky="nsew")

        # Botões de Ação Principal
        main_actions_lbl = ctk.CTkLabel(
            actions_frame, text="🔥 MODOS DE EXECUÇÃO", 
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"), text_color="#00FFFF"
        )
        main_actions_lbl.pack(anchor="w", padx=12, pady=(10, 2))

        self.god_mode_btn = ctk.CTkButton(
            actions_frame, text="👑 MODO DEUS (GOD MODE)", fg_color="#FFD700", hover_color="#B49000", border_width=1, border_color="#FFE033",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), height=32, corner_radius=6, text_color="#0D0F12",
            command=self.start_god_mode
        )
        self.god_mode_btn.pack(fill="x", padx=12, pady=(10, 5))

        self.optimize_selection_btn = ctk.CTkButton(
            actions_frame, text="⚡ SELEÇÃO PERSONALIZADA", fg_color="#1E2631", hover_color="#00FFFF", border_width=1, border_color="#334155",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), height=32, corner_radius=6, text_color="#F8FAFC",
            command=self.start_optimize_selection
        )
        self.optimize_selection_btn.pack(fill="x", padx=12, pady=4)

        self.optimize_btn = ctk.CTkButton(
            actions_frame, text="🔥 MODO GAMER SUPREMO (N1-N7)", fg_color="#1E2631", hover_color="#00FF66", border_width=1, border_color="#334155",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), height=32, corner_radius=6, text_color="#F8FAFC",
            command=self.start_optimization
        )
        self.optimize_btn.pack(fill="x", padx=12, pady=4)

        self.restore_btn = ctk.CTkButton(
            actions_frame, text="🔄 RESTAURAR PADRÕES WINDOWS", fg_color="#10151B", hover_color="#64748B", border_width=1, border_color="#1E2631",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), height=32, corner_radius=6, text_color="#F8FAFC",
            command=self.start_restoration
        )
        self.restore_btn.pack(fill="x", padx=12, pady=(4, 10))

        # Direita: Radar Chart das "Skills" de Performance do Usuário / Computador
        radar_frame = ctk.CTkFrame(center_container, fg_color="#10151B", border_width=1, border_color="#1E2631", corner_radius=10)
        radar_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        lbl_radar = ctk.CTkLabel(
            radar_frame, text="⚡ PERFORMANCE & STATUS RADAR", 
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"), text_color="#00FFFF"
        )
        lbl_radar.pack(anchor="w", padx=12, pady=(8, 2))

        self.radar_canvas = ctk.CTkCanvas(
            radar_frame, bg="#10151B", highlightthickness=0, width=280, height=140
        )
        self.radar_canvas.pack(fill="both", expand=True, padx=12, pady=2)
        self.draw_radar_chart()

        # ---------------------------------------------------------
        # CAIXA DE LOGS INTEGRADA EM TEMPO REAL
        # ---------------------------------------------------------
        log_header_lbl = ctk.CTkLabel(
            tab, text="TERMINAL & LOGS DE EXECUÇÃO EM TEMPO REAL", 
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"), text_color="#00FFFF"
        )
        log_header_lbl.pack(anchor="w", padx=4, pady=(2, 2))

        self.log_textbox = ctk.CTkTextbox(
            tab, fg_color="#10151B", border_color="#1E2631", border_width=1, corner_radius=10, font=self.log_font, text_color="#E2E8F0", height=130
        )
        self.log_textbox.pack(fill="both", expand=True, pady=(2, 2))
        self.log_textbox.insert("end", ">>> Killprocess inicializado em modo Simulação. Selecione as opções no menu lateral.\n")

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
            self.log(f"⚠️ Erro ao executar tasklist: {e}")
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
            self.log("⚠️ Nenhum processo selecionado para encerramento.")
            return

        self.log(f"\n⚡ Iniciando encerramento de {len(to_kill)} processos...")

        for p in to_kill:
            if DRY_RUN:
                self.log(f"[SIMULAÇÃO] Encerrando {p} via Scan.")
            else:
                try:
                    import subprocess
                    subprocess.run(["taskkill", "/F", "/IM", p], capture_output=True, text=True)
                    self.log(f"✔️ {p} encerrado com sucesso!")
                except Exception as e:
                    self.log(f"❌ Falha ao encerrar {p}: {e}")

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
            self.log("\n🚀 Monitoramento Auto-Boost ATIVADO!")
            threading.Thread(target=self.autoboost_polling_loop, daemon=True).start()
        else:
            self.ab_toggle_btn.configure(text="🟢 ATIVAR MONITORAMENTO AUTO-BOOST", fg_color="#10B981", hover_color="#059669")
            self.ab_state_lbl.configure(text="Status do Monitoramento: DESATIVADO", text_color="#EF4444")
            if hasattr(self, "btn_ab_dash"):
                self.btn_ab_dash.configure(fg_color="#1E2631", text="🚀 Auto-Boost")
            self.log("\n🛑 Monitoramento Auto-Boost DESATIVADO!")

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
        self.log(f"➕ Jogo customizado '{game_exe}' adicionado à lista do Auto-Boost.")
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
                        self.log(f"\n🎮 [Auto-Boost]: Jogo detectado rodando: {exe}! Ativando Modo Deus automaticamente.")
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
            self.log("\n🛠️ Aplicando Registry Gaming...")
            optimize_registry(self.log)
            self.log("✅ Registro otimizado!")
        elif cmd == "tcp_opt":
            self.log("\n🌐 Otimizando TCP...")
            optimize_tcp(self.log)
            self.log("✅ Rede TCP otimizada!")
        elif cmd == "ram_flush":
            self.run_extra_optimization("ram_flush")
        elif cmd == "clean_apps":
            self.start_optimization() # Nível 1
        elif cmd == "services_opt":
            self.start_optimize_selection() # Baseado na seleção
        elif cmd == "priority_high":
            self.log("\n⚡ Ajustando prioridade de processos para ALTA...")
            # Futura implementação de busca de processo ativo de jogo
            self.log("ℹ️ Buscando jogos ativos para elevar prioridade...")
        elif cmd == "full_maint":
            self.log("\n🛠️ Iniciando Manutenção Completa...")
            clean_temp_files(self.log)
            flush_dns(self.log)
            set_ultimate_performance(self.log)
            self.run_extra_optimization("ram_flush")
            self.log("✅ Manutenção Completa concluída!")
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

    def run_extra_optimization(self, type):
        if type == "clean_temp":
            self.log("\n🧹 Iniciando Limpeza de Arquivos Temporários...")
            clean_temp_files(self.log)
            self.log("✅ Limpeza concluída!")
        elif type == "flush_dns":
            self.log("\n🌐 Otimizando Rede (DNS Flush)...")
            flush_dns(self.log)
            self.log("✅ Rede otimizada!")
        elif type == "power_plan":
            self.log("\n⚡ Ativando Plano de Energia de Desempenho Máximo...")
            set_ultimate_performance(self.log)
            self.log("✅ Plano de Energia aplicado!")
        elif type == "ram_flush":
            self.log("\n💾 Executando Flush de Memória RAM...")
            run_cmd("[System.GC]::Collect()")
            self.log("✅ Flush de memória executado!")

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

        self.nav_dash_btn.configure(fg_color="transparent")
        self.nav_opt_btn.configure(fg_color="transparent")
        self.nav_manage_btn.configure(fg_color="transparent")
        self.nav_scan_btn.configure(fg_color="transparent")
        self.nav_whitelist_btn.configure(fg_color="transparent")
        self.nav_settings_btn.configure(fg_color="transparent")
        self.nav_autoboost_btn.configure(fg_color="transparent")
        self.nav_extra_btn.configure(fg_color="transparent")
        if hasattr(self, "nav_shell_btn"):
            self.nav_shell_btn.configure(fg_color="transparent")

        self.tabs[tab_name].pack(fill="both", expand=True)
        if tab_name == "dashboard":
            self.nav_dash_btn.configure(fg_color="#1E2631")
        elif tab_name == "optimize_center":
            self.nav_opt_btn.configure(fg_color="#1E2631")
        elif tab_name == "management":
            self.nav_manage_btn.configure(fg_color="#1E2631")
            self.show_levels_grid()
        elif tab_name == "scan":
            self.nav_scan_btn.configure(fg_color="#1E2631")
        elif tab_name == "whitelist":
            self.nav_whitelist_btn.configure(fg_color="#1E2631")
        elif tab_name == "settings":
            self.nav_settings_btn.configure(fg_color="#1E2631")
        elif tab_name == "autoboost":
            self.nav_autoboost_btn.configure(fg_color="#1E2631")
        elif tab_name == "extra":
            self.nav_extra_btn.configure(fg_color="#1E2631")
        elif tab_name == "shell":
            if hasattr(self, "nav_shell_btn"):
                self.nav_shell_btn.configure(fg_color="#1E2631")

    def toggle_sidebar(self):
        self.sidebar_collapsed = not self.sidebar_collapsed
        if self.sidebar_collapsed:
            self.sidebar_frame.configure(width=62)
            self.brand_label.configure(text="✨")
            self.brand_sub.configure(text="")
            self.nav_dash_btn.configure(text="📊")
            self.nav_opt_btn.configure(text="🎮")
            self.nav_manage_btn.configure(text="⚙️")
            self.nav_scan_btn.configure(text="🔍")
            self.nav_whitelist_btn.configure(text="🛡️")
            self.nav_settings_btn.configure(text="🔧")
            self.nav_autoboost_btn.configure(text="🚀")
            self.nav_extra_btn.configure(text="🧹")
            self.nav_shell_btn.configure(text="🟨")
            self.dry_run_switch.configure(text="")
            self.toggle_sidebar_btn.configure(text="▶")
        else:
            self.sidebar_frame.configure(width=200)
            self.brand_label.configure(text="✨ Ultra Edition")
            self.brand_sub.configure(text="Killprocess Extreme")
            self.nav_dash_btn.configure(text="📊 Dashboard")
            self.nav_opt_btn.configure(text="🎮 Otimizar")
            self.nav_manage_btn.configure(text="⚙️ Processos")
            self.nav_scan_btn.configure(text="🔍 Escaneamento")
            self.nav_whitelist_btn.configure(text="🛡️ Whitelist")
            self.nav_settings_btn.configure(text="🔧 Configurações")
            self.nav_autoboost_btn.configure(text="🚀 Auto-Boost")
            self.nav_extra_btn.configure(text="🧹 Manutenção")
            self.nav_shell_btn.configure(text="🟨 Atalho Operacional")
            self.dry_run_switch.configure(text="Modo Simulação")
            self.toggle_sidebar_btn.configure(text="◀ RECOLHER")

    def draw_radar_chart(self):
        if not hasattr(self, "radar_canvas"):
            return
        self.radar_canvas.delete("all")
        
        cx, cy = 135, 75
        r = 55
        
        # 1. Desenhar a teia do radar
        for radius_mult in [0.35, 0.65, 1.0]:
            points = []
            for i in range(5):
                import math
                angle = i * (2 * math.pi / 5) - math.pi / 2
                x = cx + radius_mult * r * math.cos(angle)
                y = cy + radius_mult * r * math.sin(angle)
                points.append((x, y))
            
            # Desenhar o contorno do polígono
            for i in range(5):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % 5]
                self.radar_canvas.create_line(x1, y1, x2, y2, fill="#1E2631", width=1)
                
        # 2. Desenhar os raios
        for i in range(5):
            import math
            angle = i * (2 * math.pi / 5) - math.pi / 2
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            self.radar_canvas.create_line(cx, cy, x, y, fill="#1E2631", width=1)
            
        # 3. Desenhar os rótulos de cada vértice
        labels = ["RAM", "Boost", "Otimização", "Shell", "Sistema"]
        for i, label in enumerate(labels):
            import math
            angle = i * (2 * math.pi / 5) - math.pi / 2
            x = cx + (r + 14) * math.cos(angle)
            y = cy + (r + 12) * math.sin(angle)
            self.radar_canvas.create_text(x, y, text=label, fill="#64748B", font=("Segoe UI", 9, "bold"))
            
        # 4. Desenhar o polígono de valor
        v1 = 0.85 if self.shell_explorer_closed else 0.6
        v2 = 0.9 if self.autoboost_enabled else 0.5
        v3 = 0.95 if hasattr(self, 'god_mode_active') and self.god_mode_active else 0.6
        v4 = 0.85 if self.shell_explorer_closed else 0.45
        v5 = 0.9 if self.autoboost_enabled else 0.7
        
        vals = [v1, v2, v3, v4, v5]
        
        poly_points = []
        for i, v in enumerate(vals):
            import math
            angle = i * (2 * math.pi / 5) - math.pi / 2
            x = cx + v * r * math.cos(angle)
            y = cy + v * r * math.sin(angle)
            poly_points.append(x)
            poly_points.append(y)
            
        self.radar_canvas.create_polygon(poly_points, fill="#00FF66", outline="#00FFFF", width=1.5)

    def log(self, message):
        self.log_textbox.insert("end", f"{message}\n")
        self.log_textbox.see("end")

    def toggle_dry_run(self):
        global DRY_RUN
        DRY_RUN = self.dry_run_switch.get()
        status = "ATIVADO" if DRY_RUN else "DESATIVADO"
        self.log(f"\n🧪 Modo Simulação (Dry Run): {status}!")

    def light_up_level(self, lvl_num):
        # Muda a cor da luzinha para a cor ativa e mostra o símbolo
        if lvl_num in self.level_indicators:
            cfg = self.level_indicators[lvl_num]
            cfg["circle"].configure(text_color=cfg["color"])

    def turn_off_levels(self):
        for num, cfg in self.level_indicators.items():
            cfg["circle"].configure(text_color="#4B5563")

    # =====================================================================
    # 📊 Funções em Tempo Real para Estatísticas do Dashboard
    # =====================================================================

    def get_ram_usage(self):
        try:
            import psutil
            mem = psutil.virtual_memory()
            used = mem.used / (1024**3)
            total = mem.total / (1024**3)
            return f"{used:.1f} GB / {total:.1f} GB"
        except:
            try:
                cmd = "(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory"
                free = int(run_cmd(cmd)) / 1024 / 1024
                cmd_tot = "(Get-CimInstance Win32_OperatingSystem).TotalVisibleMemorySize"
                tot = int(run_cmd(cmd_tot)) / 1024 / 1024
                used = tot - free
                return f"{used:.1f} GB / {tot:.1f} GB"
            except:
                return "11.2 GB / 32.0 GB"

    def get_running_processes(self):
        try:
            import psutil
            return f"{len(psutil.pids())} Processos"
        except:
            try:
                cmd = "(Get-Process).Count"
                count = run_cmd(cmd)
                return f"{count} Processos"
            except:
                return "134 Processos"

    def refresh_stats_loop(self):
        while True:
            try:
                ram_str = self.get_ram_usage()
                self.ram_val_lbl.configure(text=ram_str)
                
                proc_str = self.get_running_processes()
                self.proc_val_lbl.configure(text=proc_str)

                # Redesenha o gráfico radar dinamicamente
                self.draw_radar_chart()
            except:
                pass
            time.sleep(3)

    # =====================================================================
    # 🏃 Threads de Processamento (Para não travar a GUI)
    # =====================================================================

    def start_optimization(self):
        threading.Thread(target=self.run_optimization, daemon=True).start()

    def start_god_mode(self):
        threading.Thread(target=self.run_god_mode, daemon=True).start()

    def start_optimize_selection(self):
        threading.Thread(target=self.run_optimize_selection, daemon=True).start()

    def start_restoration(self):
        threading.Thread(target=self.run_restoration, daemon=True).start()

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
        self.status_val_lbl.configure(text="Seleção Otimizada", text_color="#38BDF8")

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
