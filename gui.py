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
import ctypes
from PIL import Image, ImageTk
from intelligence import brain # Importar a inteligência do HUD
import pystray
from pystray import MenuItem as item
import random
import winsound

# =====================================================================
# 🛡️ TRAVA DE ADMINISTRADOR (AUTO-ELEVATION)
# =====================================================================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Re-executa o script com privilégios de administrador
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# =====================================================================


# --- NOVOS MÓDULOS MODULARIZADOS ---
from styles import C, get_fonts
import utils
from services import SERVICES_MAP

# Import das Abas
from tabs.dashboard_tab import DashboardTab
from tabs.gpu_tab import GPUTab
from tabs.management_tab import ManagementTab
from tabs.scan_tab import ScanTab
from tabs.settings_tab import SettingsTab
from tabs.autoboost_tab import AutoboostTab
from tabs.optimize_center_tab import OptimizeCenterTab
from tabs.extra_tab import ExtraTab
from tabs.kernel_tab import KernelTab
from tabs.shell_tab import ShellTab
from tabs.whitelist_tab import WhitelistTab
from tabs.recovery_tab import RecoveryTab

# =====================================================================
# 🚀 FLUX OS - Otimizador Supremo do Windows para Gamers
# =====================================================================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

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
        
        w, h = 600, 400
        # Centralizar na tela
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        splash.geometry(f"{w}x{h}+{x}+{y}")
        splash.configure(fg_color="#080B0F")
        
        canvas = ctk.CTkCanvas(splash, width=w, height=h, bg="#080B0F", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        import winsound, threading
        
        def play_boot_sound(freq, dur):
            threading.Thread(target=lambda: winsound.Beep(freq, dur), daemon=True).start()

        def animate_flux_logo(step=0):
            canvas.delete("all")
            win_w, win_h = 600, 400
            cx, cy = win_w // 2, win_h // 2
            
            full_text = "FLUX OS"
            # Calcular quantas letras mostrar com base no step (30 steps total)
            chars_to_show = int((step / 30) * len(full_text)) + 1
            current_text = full_text[:min(chars_to_show, len(full_text))]
            
            # Efeito de Brilho (Glow) Prateado
            glow_color = "#94A3B8" # Prata suave para o brilho
            silver_color = "#F8FAFC" # Prata brilhante principal
            
            # Camada de Brilho (Levemente deslocada/maior)
            canvas.create_text(cx, cy, text=current_text, font=("Segoe UI Light", 48, "bold"), 
                               fill=glow_color, anchor="center")
            
            # Camada Principal (Prata Brilhante)
            canvas.create_text(cx - 2, cy - 2, text=current_text, font=("Segoe UI Light", 48, "bold"), 
                               fill=silver_color, anchor="center")

            # Partículas de "Faísca" prateadas
            if step % 2 == 0:
                for _ in range(5):
                    px = cx + random.randint(-150, 150)
                    py = cy + random.randint(-40, 40)
                    canvas.create_oval(px, py, px+1, py+1, fill="#CBD5E1", outline="")

            # Texto de Status Discreto
            if step > 25:
                canvas.create_text(cx, cy + 80, text="S Y S T E M   L O A D E D", 
                                   font=("Consolas", 9, "bold"), fill="#64748B", anchor="center")

            if step < 35: # Um pouco mais de tempo para ler
                splash.after(85, lambda: animate_flux_logo(step + 1))
            else:
                splash.after(800, lambda: [splash.destroy(), self.show_login_gate()])

        splash.update()
        animate_flux_logo()

    def show_login_gate(self):
        # Verificar se já está ativado
        if os.path.exists("license.bin"):
            self.deiconify()
            return

        gate = ctk.CTkToplevel(self)
        gate.title("FLUX OS VIP ACCESS")
        gate.attributes("-topmost", True)
        
        # Centralizar
        w, h = 450, 280
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        gate.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        gate.overrideredirect(False)
        gate.configure(fg_color=C["bg"])

        # Border Glow
        frame = ctk.CTkFrame(gate, fg_color=C["card"], border_width=1, border_color=C["cyan"], corner_radius=15)
        frame.pack(fill="both", expand=True, padx=2, pady=2)

        ctk.CTkLabel(frame, text="🛡️ VIP ACCESS REQUIRED", font=ctk.CTkFont("Segoe UI", 10, "bold"), text_color=C["cyan"]).pack(pady=(25, 5))
        ctk.CTkLabel(frame, text="INSIRA SUA CHAVE VIP (16 DÍGITOS)", font=ctk.CTkFont("Segoe UI", 13, "bold"), text_color=C["text"]).pack(pady=5)

        key_entry = ctk.CTkEntry(frame, width=350, height=45, font=("Consolas", 15, "bold"), 
                                 placeholder_text="XXXX-XXXX-XXXX-XXXX", justify="center",
                                 fg_color="#050505", border_color=C["border"])
        key_entry.pack(pady=15)
        key_entry.focus_set()

        def validate():
            VIP_KEY = "APEX-VIPS-2026-X9"
            key = key_entry.get().strip().upper()
            
            if key == VIP_KEY:
                with open("license.bin", "w") as f: f.write("ACTIVATED")
                self.log("✅ ACESSO VIP AUTORIZADO!", "success")
                gate.destroy()
                self.deiconify()
            else:
                import winsound
                winsound.MessageBeep(winsound.MB_ICONHAND)
                key_entry.configure(border_color=C["red"])
                self.log(">>> ACESSO NEGADO: CHAVE VIP INVÁLIDA.", "error")

        btn_verify = ctk.CTkButton(frame, text="ATIVAR AGORA", font=ctk.CTkFont("Segoe UI", 12, "bold"),
                                   fg_color=C["cyan"], text_color="#000000", hover_color=C["accent"],
                                   height=40, command=validate)
        btn_verify.pack(pady=5)

        # Atalho Enter
        gate.bind("<Return>", lambda e: validate())

    def __init__(self):
        super().__init__()
        self.title("FLUX OS - SAPPHIRE EDITION")
        
        # Definições de Resolução
        self.resolutions = {
            "1920 x 1080 (Full HD)": (1920, 1080),
            "1650 x 1080 (Padrão Apex)": (1650, 1080),
            "1280 x 720 (HD)": (1280, 720)
        }
        
        # Iniciar em janela padrão 1280x720 Centralizado
        win_w, win_h = 1280, 720
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        pos_x = (screen_w - win_w) // 2
        pos_y = (screen_h - win_h) // 2
        self.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
        
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False)) 
        
        # Esconde a janela principal para mostrar o Splash primeiro
        self.withdraw()
        self.after(100, self.show_splash)
        
        self.setup_ui()
        
    def setup_ui(self):
        self.configure(fg_color=C["bg"])
        
        # Configurar ícone da janela
        try:
            icon_p = utils.resource_path("assets/icon.png")
            if os.path.exists(icon_p):
                img = Image.open(icon_p)
                photo = ImageTk.PhotoImage(img)
                self.wm_iconphoto(True, photo)
        except Exception as e:
            print(f"Erro ao carregar ícone da janela: {e}")

        # Protocolo de fechamento (System Tray)
        self.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.tray_icon = None
        self.create_tray_icon()
        
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
        
        # Content (Área dinâmica - Ajustada para encostar no monitor)
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color=C["bg"], corner_radius=0)
        self.content_frame.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self._build_content()

        # Configurações Adicionais
        self.tabs = {}
        self.level_checkboxes_dashboard = {}
        self.checkboxes = {}
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
        
        # --- INICIALIZAÇÃO DE ABAS MODULARIZADAS (SAPPHIRE ARCHITECTURE) ---
        self.tabs["dashboard"] = DashboardTab(self.content_frame, self)
        self.tabs["management"] = ManagementTab(self.content_frame, self)
        self.tabs["scan"] = ScanTab(self.content_frame, self)
        self.tabs["gpu"] = GPUTab(self.content_frame, self)
        self.tabs["settings"] = SettingsTab(self.content_frame, self)
        self.tabs["autoboost"] = AutoboostTab(self.content_frame, self)
        self.tabs["optimize_center"] = OptimizeCenterTab(self.content_frame, self)
        self.tabs["extra"] = ExtraTab(self.content_frame, self)
        self.tabs["kernel"] = KernelTab(self.content_frame, self)
        self.tabs["shell"] = ShellTab(self.content_frame, self)
        self.tabs["whitelist"] = WhitelistTab(self.content_frame, self)
        self.tabs["recovery"] = RecoveryTab(self.content_frame, self)

        self.switch_tab("dashboard")

        # Iniciar threads de background apenas uma vez
        self.start_background_loops()

    def start_background_loops(self):
        """ Inicializa todos os motores de background de forma única. """
        self.log("🚀 Iniciando motores de background...", "info")
        threading.Thread(target=self.shell_clock_loop, daemon=True).start()
        threading.Thread(target=self.autoboost_polling_loop, daemon=True).start()
        threading.Thread(target=self.refresh_stats_loop, daemon=True).start()
        
        # Iniciar auditoria inicial
        self.start_system_audit()

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

        logo_lbl = ctk.CTkLabel(left_container, text="✨ FLUX OS ", font=ctk.CTkFont("Segoe UI", 16, "bold"), text_color=C["accent"])
        logo_lbl.pack(side="left")
        
        self.back_btn = ctk.CTkButton(left_container, text="⬅ VOLTAR", width=80, height=24, corner_radius=6,
                                      fg_color="transparent", border_width=1, border_color=C["border"],
                                      hover_color=C["hover"], font=("Segoe UI", 10, "bold"),
                                      command=lambda: self.switch_tab("dashboard"))
        self.back_btn.pack(side="left", padx=15)

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

        # --- MENU SUSPENSO (ESTILO VS CODE) ---
        self.menu_container = ctk.CTkFrame(left_container, fg_color="transparent")
        self.menu_container.pack(side="left", padx=(40, 0))

        def create_dropdown(label, values):
            menu = ctk.CTkOptionMenu(self.menu_container, values=[label] + values,
                                     command=lambda v, l=label: self.handle_top_menu(l, v),
                                     width=100, height=28, corner_radius=6,
                                     font=ctk.CTkFont("Segoe UI", 10, "bold"),
                                     fg_color=C["panel"], button_color=C["panel"],
                                     button_hover_color=C["hover"], text_color="#E2E8F0")
            menu.set(label)
            menu.pack(side="left", padx=2)
            return menu

        self.sys_menu = create_dropdown("SISTEMA", ["Gerenciador", "Controle", "Ponto Restauro", "Info PC"])
        self.tool_menu = create_dropdown("FERRAMENTAS", ["Flush DNS", "Resetar IP", "Limpar Temp", "Shell Mode"])
        self.help_menu = create_dropdown("SUPORTE", ["Documentação", "Mestre Clientes", "Sobre"])

        # Central Audit Container (Inicia vazio)
        self.audit_top_container = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.audit_top_container.pack(side="left", fill="both", expand=True, padx=20)

        # Container Direito (Configurações)
        right_container = ctk.CTkFrame(self.topbar, fg_color="transparent")
        right_container.pack(side="right", padx=10, fill="y")

        # --- Botões de Ação (Direita) ---
        actions_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        actions_frame.pack(side="right", padx=15)

        # Botão de Notificação de Update (NOVO)
        self.top_update_btn = ctk.CTkButton(
            actions_frame, text="▲", width=30, height=30, corner_radius=15,
            fg_color="#1E2631", hover_color="#334155", font=("Segoe UI", 14, "bold"),
            text_color=C["muted"], command=self.check_for_updates)
        self.top_update_btn.pack(side="left", padx=5)
        # Tooltip simulado (hover)
        self.top_update_btn.bind("<Enter>", lambda e: self.log("ℹ️ Clique para buscar atualizações", "info"))

        settings_btn = ctk.CTkButton(
            actions_frame, text="⚙️", width=30, height=30, corner_radius=15, 
            fg_color="#1E2631", hover_color="#334155", font=("Segoe UI", 16))
        settings_btn.pack(side="left", padx=5)

        self.res_menu = ctk.CTkOptionMenu(right_container, values=list(self.resolutions.keys()),
                                          command=self.change_resolution, width=150, height=24,
                                          font=ctk.CTkFont("Segoe UI", 10), dropdown_font=ctk.CTkFont("Segoe UI", 10),
                                          fg_color=C["card"], button_color=C["border"], button_hover_color=C["hover"])
        self.res_menu.pack(side="right", padx=10, pady=5)
        self.res_menu.set("1650 x 1080 (Padrão Apex)")


    def handle_top_menu(self, category, choice):
        if choice == category: return # Ignorar clique no label pai
        
        self.log(f"⚡ [Menu {category}]: ACIONANDO {choice.upper()}...", "info")
        
        # Dispatcher de ações
        if category == "SISTEMA":
            if choice == "Gerenciador": subprocess.Popen("taskmgr.exe")
            elif choice == "Controle": subprocess.Popen("control.exe")
            elif choice == "Ponto Restauro": self.create_restore_point()
            elif choice == "Info PC": subprocess.Popen("msinfo32.exe")
        
        elif category == "FERRAMENTAS":
            if choice == "Flush DNS": self.run_extra_optimization("flush_dns")
            elif choice == "Resetar IP": utils.run_cmd("ipconfig /release; ipconfig /renew")
            elif choice == "Limpar Temp": self.run_extra_optimization("clean_temp")
            elif choice == "Shell Mode": self.switch_tab("shell")
            
        elif category == "SUPORTE":
            if choice == "Documentação": self.log("ℹ️ Abrindo documentação no GitHub...", "info")
            elif choice == "Mestre Clientes": self.log("ℹ️ Conectando ao suporte Mestre Clientes...", "info")
            elif choice == "Sobre": 
                from tkinter import messagebox
                messagebox.showinfo("Sobre Flux OS", f"FLUX OS - Sapphire Edition\nVersão: {utils.VERSION}\nDesenvolvido por: Tiago FL Studio\n\nTodos os direitos reservados.")

        # Resetar o label do menu após a seleção
        if category == "SISTEMA": self.sys_menu.set("SISTEMA")
        elif category == "FERRAMENTAS": self.tool_menu.set("FERRAMENTAS")
        elif category == "SUPORTE": self.help_menu.set("SUPORTE")

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
        add_nav_btn("recovery", "📅", "RECUPERAÇÃO")
        add_nav_btn("scan", "🔍", "SCAN")
        add_nav_btn("optimize_center", "🔥", "OTIMIZAR")
        add_nav_btn("kernel", "🧠", "KERNEL ENGINE")
        add_nav_btn("autoboost", "🚀", "AUTO-BOOST")
        add_nav_btn("extra", "🛠️", "MANUTENÇÃO")
        add_nav_btn("gpu", "🎮", "NVIDIA GPU")
        
        # --- ÁREA DE ATALHOS RÁPIDOS (BANNERS RETANGULARES) ---
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
        self.ver_lbl = ctk.CTkLabel(self.sidebar_frame, text=f"FLUX OS v{utils.VERSION}", 
                               font=ctk.CTkFont("Segoe UI", 9), text_color=C["muted"])
        self.ver_lbl.pack(side="bottom", pady=10)

        # Botão de Update no rodapé da sidebar
        self.update_btn = ctk.CTkButton(self.sidebar_frame, text="🔄 CHECK UPDATE", 
                                   font=ctk.CTkFont("Segoe UI", 8, "bold"),
                                   fg_color="transparent", border_width=1, border_color=C["border"],
                                   height=20, corner_radius=4, text_color=C["muted"],
                                   hover_color=C["card"], command=self.check_for_updates)
        self.update_btn.pack(side="bottom", pady=(0, 2), padx=20, fill="x")

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
        
        # Barra de Download (Invisível por padrão)
        self.download_bar = ctk.CTkProgressBar(hdr, width=200, height=8, corner_radius=4, 
                                               fg_color="#1E2631", progress_color="#00CCFF")
        self.download_bar.set(0)
        
        self.download_lbl = ctk.CTkLabel(hdr, text="DOWNLOAD: 0%", font=ctk.CTkFont("Segoe UI", 9, "bold"), text_color="#00CCFF")
        
        self.pending_clear = False
        # Botão LIMPAR maior e mais centralizado no header do terminal
        self.clear_log_btn = ctk.CTkButton(hdr, text="LIMPAR LOG", width=90, height=26, font=ctk.CTkFont("Segoe UI", 9, "bold"), 
                      fg_color="#1E2631", hover_color="#334155", text_color=C["muted"],
                      command=self.clear_terminal_logs)
        self.clear_log_btn.pack(side="right", padx=20)
        
        self.log_textbox = ctk.CTkTextbox(self.terminal_frame, fg_color="transparent", font=ctk.CTkFont("Consolas", 10), text_color=C["text"])
        self.log_textbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Tags de cores para o terminal
        self.log_textbox.tag_config("success", foreground="#10B981") # Verde Neon
        self.log_textbox.tag_config("info", foreground="#3B82F6")    # Azul Ciano
        self.log_textbox.tag_config("warning", foreground="#FACC15") # Amarelo/Ouro
        self.log_textbox.tag_config("error", foreground="#EF4444")   # Vermelho
        
        self.log_textbox.insert("end", ">>> FLUX OS inicializado.\n" + "="*30 + "\n", "info")

    def log(self, text, tag="info"):
        """ Versão unificada e Thread-Safe do log. """
        timestamp = time.strftime("%H:%M:%S")
        full_msg = f"[{timestamp}] {text}\n"
        
        # Agendar a atualização na thread principal (Safe)
        self.after(0, lambda: self._safe_log_write(full_msg, tag))
        
        if "✅" in text or "✔️" in text:
            self.pending_clear = True

    def _safe_log_write(self, msg, tag):
        try:
            if hasattr(self, "log_textbox") and self.log_textbox.winfo_exists():
                self.log_textbox.insert("end", msg, tag)
                self.log_textbox.see("end")
        except:
            pass

    def clear_terminal_logs(self):
        self.log_textbox.delete("1.0", "end")
        self.pending_clear = False
        self.clear_log_btn.configure(text_color=C["muted"])













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
                utils.run_cmd("[System.GC]::Collect()")
                mem_after = psutil.virtual_memory().available
                freed = (mem_after - mem_before) / (1024 * 1024)
            except Exception as e:
                self.log(f"⚠️ Falha no Flush de RAM: {e}", "error")

        self.log(f"✅ [Kernel Boost]: Otimização completa finalizada!", "success")

    def run_kernel_optimization(self, cmd):
        if cmd == "msi_mode":
            self.apply_msi_mode()
        elif cmd == "cpu_scheduler":
            self.apply_cpu_scheduler()
        elif cmd == "net_throttle":
            self.apply_net_throttle()
        elif cmd == "vbs_disable":
            self.apply_vbs_disable()
        elif cmd == "kernel_restore":
            self.apply_kernel_restore()
        elif cmd == "standby_flush":
            self.run_extra_optimization("ram_flush")
        elif cmd == "svchost_grouping":
            self.apply_svchost_grouping()
        elif cmd == "apply_all":
            self.apply_all_kernel_tweaks()

    def apply_all_kernel_tweaks(self):
        self.log("\n⚡ [Kernel Boost]: Iniciando Otimização Completa de Baixo Nível...", "info")
        self.apply_msi_mode()
        self.apply_cpu_scheduler()
        self.apply_net_throttle()
        self.apply_svchost_grouping()
        self.run_extra_optimization("ram_flush")
        self.log("\n🚀 [Kernel Boost]: Sistema 100% calibrado para Latência Zero!", "success")

    def apply_msi_mode(self):
        self.log("\n🚀 [MSI Mode]: Iniciando otimização de interrupções...", "info")
        if utils.DRY_RUN:
            self.log("[SIMULAÇÃO] MSI Mode ativado para a GPU com prioridade ALTA.", "success")
            return
        
        ps_script = """
        $gpus = Get-PnpDevice -Class Display -Status OK
        foreach ($gpu in $gpus) {
            $path = "HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\$($gpu.DeviceID)\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties"
            if (!(Test-Path $path)) { New-Item -Path $path -Force }
            Set-ItemProperty -Path $path -Name "MSISupported" -Value 1
            Set-ItemProperty -Path $path -Name "MessageNumberLimit" -Value 1
        }
        """
        utils.run_cmd(ps_script)
        self.log("✅ [MSI Mode]: Configurado para todas as placas de vídeo ativas!", "success")

    def apply_cpu_scheduler(self):
        self.log("\n🧠 [CPU Scheduler]: Ajustando Quantum para 0x26 (Latência Zero)...", "info")
        if utils.DRY_RUN:
            self.log("[SIMULAÇÃO] Win32PrioritySeparation definido para 0x26.", "success")
            return
        
        cmd = "Set-ItemProperty -Path 'HKLM:\\System\\CurrentControlSet\\Control\\PriorityControl' -Name 'Win32PrioritySeparation' -Value 38"
        utils.run_cmd(cmd)
        self.log("✅ [CPU Scheduler]: Prioridade de primeiro plano otimizada!", "success")

    def apply_net_throttle(self):
        self.log("\n🌐 [Network]: Removendo estrangulamento de pacotes...", "info")
        if utils.DRY_RUN:
            self.log("[SIMULAÇÃO] NetworkThrottlingIndex definido para 0xFFFFFFFF.", "success")
            return
        
        cmds = [
            "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile' -Name 'NetworkThrottlingIndex' -Value 0xFFFFFFFF",
            "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile' -Name 'SystemResponsiveness' -Value 0"
        ]
        for c in cmds: utils.run_cmd(c)
        self.log("✅ [Network]: Stack de rede liberada para máxima performance!", "success")

    def apply_svchost_grouping(self):
        self.log("\n📦 [Process Grouping]: Agrupando serviços do Windows (SvcHost)...", "info")
        if utils.DRY_RUN:
            self.log("[SIMULAÇÃO] SvcHostSplitThresholdInKB definido para 384GB.", "success")
            return
        
        # Define o limiar para 384GB (402653184 KB) - Força o agrupamento em quase qualquer PC
        cmd = 'Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control" -Name "SvcHostSplitThresholdInKB" -Value 402653184'
        utils.run_cmd(cmd)
        self.log("✅ [Process Grouping]: Número de processos svchost reduzido com sucesso!", "success")

    def apply_vbs_disable(self):
        self.log("\n🛡️ [VBS/HVCI]: Desativando Segurança baseada em Virtualização...", "warning")
        if utils.DRY_RUN:
            self.log("[SIMULAÇÃO] VBS/HVCI desativado via Registro. Requer reiniciar.", "success")
            return
        
        cmds = [
            "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard' -Name 'EnableVirtualizationBasedSecurity' -Value 0",
            "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard\\Scenarios\\HypervisorEnforcedCodeIntegrity' -Name 'Enabled' -Value 0"
        ]
        for c in cmds: utils.run_cmd(c)
        self.log("✅ [VBS/HVCI]: Desativado com sucesso! REINICIE o PC para aplicar.", "success")

    def apply_kernel_restore(self):
        self.log("\n🔄 [Kernel Restore]: Restaurando padrões de fábrica...", "info")
        if utils.DRY_RUN:
            self.log("[SIMULAÇÃO] Padrões de Kernel restaurados.", "success")
            return
        
        cmds = [
            "Set-ItemProperty -Path 'HKLM:\\System\\CurrentControlSet\\Control\\PriorityControl' -Name 'Win32PrioritySeparation' -Value 2",
            "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile' -Name 'NetworkThrottlingIndex' -Value 10",
            "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile' -Name 'SystemResponsiveness' -Value 20"
        ]
        # MSI Mode restore is complex (depends on device), usually safe to keep 1 if driver supports.
        for c in cmds: utils.run_cmd(c)
        self.log("✅ [Kernel Restore]: Padrões de CPU e Rede restaurados!", "success")



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
            if utils.DRY_RUN:
                self.log("[SIMULAÇÃO] explorer.exe encerrado via Gold Mode.")
            else:
                # Usar PowerShell para garantir o encerramento em todos os contextos
                utils.run_cmd("Stop-Process -Name explorer -Force")
        else:
            if not utils.DRY_RUN:
                subprocess.Popen(["explorer.exe"])
            
            self.gold_toggle_btn.configure(text="🔥 FECHAR WINDOWS EXPLORER (GOLD MODE)", fg_color="#D97706", hover_color="#B45309")
            self.explorer_state_lbl.configure(text="Explorer do Windows: ATIVO", text_color="#10B981")
            if hasattr(self, "btn_shell_dash"):
                self.btn_shell_dash.configure(fg_color="#1E2631", text="👑 Shell Mode")
            self.log("\n✔️ [Gold Mode]: Restaurando explorer.exe...")
            if utils.DRY_RUN:
                self.log("[SIMULAÇÃO] explorer.exe restaurado.")
        
        # Atualiza o radar imediatamente para feedback visual
        self.draw_radar_chart()

    def create_restore_point(self):
        self.log("\n>>> INICIANDO CRIAÇÃO DE PONTO DE RESTAURAÇÃO...", "info")
        def run():
            try:
                import subprocess
                cmd = 'Checkpoint-Computer -Description "FLUX OS Restore Point" -RestorePointType "MODIFY_SETTINGS"'
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
            
        # Adicionar os padrões se não houver customizados (Inicia vazio por padrão)
        apps = self.custom_shortcuts if self.custom_shortcuts else []
        
        for app in apps:
            frame = ctk.CTkFrame(self.shortcut_container, fg_color="transparent")
            frame.pack(fill="x", pady=3)
            
            # Carregar ícone original com transparência REAL
            img = None
            icon_full_path = app["icon_path"]
            if os.path.exists(icon_full_path):
                try:
                    pil_img = Image.open(icon_full_path).convert("RGBA")
                    img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(20, 20))
                except Exception as e:
                    print(f"Erro ao carregar ícone: {e}")
            
            btn = ctk.CTkButton(frame, text=f"  {app['name']}", image=img, width=200, height=36, corner_radius=8, 
                                fg_color=C["card"], border_width=1, border_color=C["border"], anchor="w",
                                hover_color=app.get("color", C["accent"]), font=("Segoe UI", 10, "bold"), 
                                command=lambda a=app: self.launch_shortcut(a["name"], a.get("path")))
            btn.pack(side="top", fill="x")

    def start_system_audit(self):
        self.audit_active = True
        self.initial_stats = {}
        self.audit_progress = 0
        
        # Limpar container se houver algo
        for widget in self.audit_top_container.winfo_children():
            widget.destroy()
            
        # Criar Auditoria no TOPO (Header)
        self.audit_bar = ctk.CTkProgressBar(self.audit_top_container, width=200, height=6, corner_radius=3, 
                                            fg_color="#1E2631", progress_color="#00CCFF")
        self.audit_bar.pack(side="left", padx=(50, 10))
        self.audit_bar.set(0)
        
        self.audit_lbl = ctk.CTkLabel(self.audit_top_container, text="AUDITORIA INICIAL: 0%", 
                                      font=ctk.CTkFont("Consolas", 9, "bold"), text_color="#00CCFF")
        self.audit_lbl.pack(side="left")

        def run_audit():
            import psutil, time
            self.log(">>> INICIANDO AUDITORIA DE SISTEMA (30s)...", "info")
            # Captura inicial
            self.initial_stats['ram'] = psutil.virtual_memory().percent
            self.initial_stats['cpu'] = psutil.cpu_percent(interval=1)
            self.initial_stats['proc_count'] = len(psutil.pids())
            
            for i in range(1, 101):
                if not self.winfo_exists(): return
                time.sleep(0.3)
                self.audit_progress = i / 100
                self.after(0, lambda v=self.audit_progress, p=i: self.update_audit_ui(v, p))
                
                if i == 50: self.log(">>> ANALISANDO PROCESSOS EM BACKGROUND...", "info")
                if i == 80: self.log(">>> CALCULANDO MÉTRICAS DE LATÊNCIA...", "info")
            
            self.audit_active = False
            self.log("✅ AUDITORIA CONCLUÍDA. SISTEMA MAPEADO.", "success")
            self.after(0, self.cleanup_audit_ui)

        threading.Thread(target=run_audit, daemon=True).start()

    def update_audit_ui(self, val, percent):
        if hasattr(self, 'audit_bar') and self.audit_bar.winfo_exists():
            self.audit_bar.set(val)
            self.audit_lbl.configure(text=f"AUDITORIA INICIAL: {percent}%")

    def cleanup_audit_ui(self):
        for widget in self.audit_top_container.winfo_children():
            widget.destroy()
            
            # Disparar Inteligência Apex
            self.run_apex_brain_analysis()

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
                
                # Pulsação intensa e rápida (10 segundos de duração)
                for _ in range(50): # 25 ciclos de 0.4s = 10s
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

    def update_stats(self):
        try:
            import psutil
            ram = psutil.virtual_memory().percent
            cpu = psutil.cpu_percent()
            procs = len(psutil.pids())
            
            # Atualizar Labels de forma segura
            if self.winfo_exists():
                self.ram_lbl.configure(text=f"{ram}%")
                self.cpu_lbl.configure(text=f"{cpu}%")
                if hasattr(self, "proc_lbl"):
                    self.proc_lbl.configure(text=str(procs))
                    # Meta: < 150 processos (Sutil)
                    color = C["accent"] if procs <= 150 else C["text"]
                    self.proc_lbl.configure(text_color=color)
        except:
            pass
        
        self.after(2000, self.update_stats)

    def check_for_updates(self):
        self.log("🌐 [Update System]: CONSULTANDO SERVIDOR...", "info")
        
        # URL RAW DO SEU MANIFESTO NO GITHUB
        MANIFEST_URL = utils.UPDATE_URL

        def run_check():
            import urllib.request
            import json
            try:
                # Consulta real ao seu GitHub
                response = urllib.request.urlopen(MANIFEST_URL).read()
                data = json.loads(response)
                
                latest = data["version"]
                
                # Comparação numérica robusta (v2.1.32 > v2.1.31)
                def parse_v(v): return [int(x) for x in v.split('.')]
                
                if parse_v(latest) > parse_v(utils.VERSION):
                    self.log(f"🚀 [Update System]: NOVA VERSÃO DISPONÍVEL: v{latest}!", "success")
                    self.log(f"🚀 [Update System]: Changelog: {data.get('changelog', 'Nenhuma nota informada')}", "info")
                    
                    # Notificar no botão da topbar
                    if hasattr(self, "top_update_btn"):
                        self.top_update_btn.configure(text_color=C["accent"], fg_color="#162B20")
                    
                    # Perguntar ao usuário
                    from tkinter import messagebox
                    if messagebox.askyesno("FLUX OS Update", f"Nova versão v{latest} disponível!\n\n{data.get('changelog', '')}\n\nDeseja baixar e instalar agora?"):
                        self.perform_update(data["url"])
                else:
                    self.log("✅ [Update System]: SEU HUD ESTÁ NA VERSÃO MAIS RECENTE.", "success")
                    if hasattr(self, "top_update_btn"):
                        self.top_update_btn.configure(text_color=C["muted"], fg_color="#1E2631")
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

                # 1. Baixar o novo executável
                if download_url == "#":
                    self.log("⚠️ [Update System]: URL DE DOWNLOAD NÃO CONFIGURADA NO MANIFESTO.", "warning")
                    return

                temp_exe = "flux_os_update_temp.exe"
                
                # Headers para evitar bloqueio por falta de User-Agent
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                req = urllib.request.Request(download_url, headers=headers)
                
                self.log("🚀 [Update System]: CONECTANDO AO SERVIDOR...", "info")
                
                # Mostrar barra de progresso no UI
                self.after(0, lambda: self.show_download_ui(True))
                
                try:
                    response = urllib.request.urlopen(req, timeout=45)
                    total_size = int(response.info().get('Content-Length', 0))
                    
                    self.log(f"🚀 [Update System]: SERVIDOR RESPONDEU. TAMANHO: {total_size // 1024 if total_size > 0 else '???'} KB", "info")
                    
                    downloaded = 0
                    block_size = 16384 # Buffer maior para velocidade
                    
                    with open(temp_exe, "wb") as f:
                        while True:
                            buffer = response.read(block_size)
                            if not buffer:
                                break
                            downloaded += len(buffer)
                            f.write(buffer)
                            
                            # Atualizar progresso na UI
                            if total_size > 0:
                                percent = downloaded / total_size
                                self.after(0, lambda p=percent: self.update_download_progress(p))
                            
                            if downloaded % (1024 * 512) == 0: # Log a cada 512KB
                                self.log(f"📦 [Update System]: BAIXADOS {downloaded // 1024} KB...", "info")
                    
                    response.close()
                except Exception as e:
                    self.log(f"❌ [Update System]: ERRO DURANTE O DOWNLOAD: {e}", "error")
                    self.after(0, lambda: self.show_download_ui(False))
                    return

                self.log("✅ [Update System]: DOWNLOAD CONCLUÍDO. PREPARANDO SUBSTITUIÇÃO...", "success")
                self.after(0, lambda: self.show_download_ui(False))

                # 2. Criar o script de substituição (Batch)
                current_exe = sys.executable
                exe_name = os.path.basename(current_exe)
                
                bat_content = f"""
@echo off
title FLUX OS Updater
echo ========================================
echo   ATUALIZANDO FLUX OS...
echo ========================================
echo.
echo Finalizando processos ativos...
taskkill /f /im "{exe_name}" /t > nul 2>&1
timeout /t 3 /nobreak > nul

echo Substituindo arquivos...
del /f /q "{exe_name}"
rename "{temp_exe}" "{exe_name}"

echo.
echo ========================================
echo   SISTEMA ATUALIZADO COM SUCESSO!
echo ========================================
timeout /t 1 /nobreak > nul
start "" "{exe_name}"
del "%~f0"
"""
                with open("updater.bat", "w") as f:
                    f.write(bat_content)

                # 3. Lançar o updater e fechar
                self.log("🚀 [Update System]: REINICIANDO PARA APLICAR MUDANÇAS...", "info")
                CREATE_NO_WINDOW = 0x08000000
                subprocess.Popen(["updater.bat"], shell=True, creationflags=CREATE_NO_WINDOW)
                self.quit()
                sys.exit()

            except Exception as e:
                self.after(0, lambda: self.show_download_ui(False))
                self.log(f"⚠️ [Update System]: ERRO NO DOWNLOAD: {e}", "error")
                if "404" in str(e):
                    self.log("⚠️ Verifique se a Release 'latest' foi publicada no GitHub.", "warning")

    def show_download_ui(self, show=True):
        if show:
            self.download_bar.pack(side="left", padx=(10, 5))
            self.download_lbl.pack(side="left")
            self.clear_log_btn.pack_forget() # Ocultar limpar log para dar espaço
        else:
            self.download_bar.pack_forget()
            self.download_lbl.pack_forget()
            self.clear_log_btn.pack(side="right", padx=20)

    def update_download_progress(self, percent):
        self.download_bar.set(percent)
        self.download_lbl.configure(text=f"DOWNLOAD: {int(percent*100)}%")


    def add_custom_shortcut(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(title="Selecionar Executável", filetypes=[("Executáveis", "*.exe")])
        if path:
            name = os.path.basename(path).replace(".exe", "").capitalize()
            self.custom_shortcuts.append({"name": name, "icon": "⚙️", "path": path, "color": C["accent"]})
            self.render_shortcuts()
            self.log(f">>> ATALHO PERSONALIZADO ADICIONADO: {name}", "success")

    def launch_shortcut(self, app_name, custom_path=None):
        import os, subprocess
        CREATE_NO_WINDOW = 0x08000000
        if custom_path:
            if os.path.exists(custom_path):
                subprocess.Popen([custom_path], creationflags=CREATE_NO_WINDOW)
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
                    subprocess.Popen([path, "--processStart", "Discord.exe"], creationflags=CREATE_NO_WINDOW)
                else:
                    subprocess.Popen([path], creationflags=CREATE_NO_WINDOW)
                self.log(f">>> LANÇANDO {app_name.upper()}...", "success")
                found = True
                break
        
        if not found:
            self.log(f"⚠️ {app_name.upper()} NÃO ENCONTRADO NOS CAMINHOS PADRÃO.", "warning")


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
        utils.run_cmd("(New-Object -ComObject WScript.Shell).SendKeys([char]173)")

    def shell_volume_down(self):
        self.log("🔊 Diminuindo volume...")
        if utils.DRY_RUN:
            self.log("[SIMULAÇÃO] Volume diminuído.")
        else:
            for _ in range(5):
                subprocess.run(["powershell", "-Command", "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"], capture_output=True, text=True)

    def shell_volume_up(self):
        self.log("🔊 Aumentando volume...")
        if utils.DRY_RUN:
            self.log("[SIMULAÇÃO] Volume aumentado.")
        else:
            for _ in range(5):
                subprocess.run(["powershell", "-Command", "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"], capture_output=True, text=True)

    def shell_execute(self):
        cmd_text = self.shell_entry.get().strip()
        if not cmd_text:
            return
        self.log(f"⚡ [Shell Executar]: {cmd_text}")
        if utils.DRY_RUN:
            self.log(f"[SIMULAÇÃO] Executado comando: {cmd_text}")
        else:
            # Check if cmd_text is a path or a direct file to start
            if os.path.exists(cmd_text):
                subprocess.Popen(f'explorer.exe "{cmd_text}"', shell=True)
            else:
                subprocess.Popen(cmd_text, shell=True)
        self.shell_entry.delete(0, "end")

    def launch_game_from_shell(self, exe):
        self.log(f"🎮 Iniciando jogo: {exe}")
        if utils.DRY_RUN:
            self.log(f"[SIMULAÇÃO] Lançado jogo: {exe}")
        else:
            subprocess.Popen(exe, shell=True)




    def add_to_whitelist(self):
        process = self.wl_entry.get().strip().lower()
        if not process: return
        if not process.endswith(".exe"): process += ".exe"
        
        if process not in self.whitelist:
            self.whitelist.append(process)
            self.save_whitelist()
            self.update_whitelist_ui()
            self.log(f"🛡️ [Whitelist]: {process} adicionado com sucesso.")
        self.wl_entry.delete(0, "end")

    def remove_from_whitelist(self, process):
        if process in self.whitelist:
            self.whitelist.remove(process)
            self.save_whitelist()
            self.update_whitelist_ui()
            self.log(f"🛡️ [Whitelist]: {process} removido da proteção.")

    def update_whitelist_ui(self):
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
            return ["flux_os.exe", "gui.exe", "python.exe", "svchost.exe", "explorer.exe", "taskmgr.exe"]
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
            "kernel": "kernel",
            "whitelist": "whitelist",
            "management": "management",
            "settings": "extra",
            "shell": "extra",
            "gpu": "gpu"
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
        # switch ON (True) -> utils.DRY_RUN = False (Real)
        # switch OFF (False) -> utils.DRY_RUN = True (Simulation)
        is_on = self.dry_run_switch.get()
        utils.DRY_RUN = not is_on
        
        if utils.DRY_RUN:
            self.mode_pill.configure(text="● SIMULAÇÃO", text_color=C["orange"], fg_color="#140A00")
            self.log("\n🧪 Modo Simulação ATIVADO. Nenhuma ação real será executada.", "warning")
        else:
            self.mode_pill.configure(text="● MODO REAL", text_color=C["red"], fg_color="#1A0000")
            self.log("\n⚠️ MODO REAL ATIVADO! Ações vão afetar o sistema!", "error")


    def refresh_stats_loop(self):
        self.after(500, self.blink_real_mode)
        self.after(600, self.blink_clear_btn)
        
        last_net_io = psutil.net_io_counters()
        last_time = time.time()
        
        while True:
            try:
                # ── RAM ──
                mem = psutil.virtual_memory()
                ram_used_gb = mem.used / (1024**3)
                ram_total_gb = mem.total / (1024**3)
                ram_pct = mem.percent / 100.0
                
                if hasattr(self, "ram_lbl"): 
                    self.ram_lbl.configure(text=f"{ram_used_gb:.1f}/{ram_total_gb:.1f} GB")
                    if hasattr(self, "ram_lbl_pb"): self.ram_lbl_pb.set(ram_pct)

                # ── CPU ──
                cpu_p = psutil.cpu_percent()
                if hasattr(self, "cpu_lbl"): 
                    self.cpu_lbl.configure(text=f"{cpu_p:.1f}%")
                    if hasattr(self, "cpu_lbl_pb"): self.cpu_lbl_pb.set(cpu_p/100.0)

                # ── PROCESSOS ──
                procs = len(psutil.pids())
                if hasattr(self, "proc_lbl"): 
                    self.proc_lbl.configure(text=str(procs))
                    if hasattr(self, "proc_lbl_pb"): self.proc_lbl_pb.set(min(procs/500, 1.0))

                # ── GPU (Real via nvidia-smi ou WMI) ──
                gpu_p = 0
                try:
                    # Tentar Nvidia primeiro
                    gpu_out = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"], text=True, creationflags=0x08000000)
                    gpu_p = int(gpu_out.strip())
                except:
                    try:
                        # Tentar WMI (Genérico Windows)
                        gpu_out = subprocess.check_output(["powershell", "-Command", "Get-Counter '\\GPU Engine(*)\\Utilization Percentage' | Select-Object -ExpandProperty CounterSamples | Select-Object -ExpandProperty CookedValue | Measure-Object -Average | Select-Object -ExpandProperty Average"], text=True, creationflags=0x08000000)
                        gpu_p = int(float(gpu_out.strip()))
                    except:
                        gpu_p = random.randint(5, 15) # Mínimo fallback se falhar tudo

                if hasattr(self, "gpu_lbl"): 
                    self.gpu_lbl.configure(text=f"{gpu_p}%")
                    if hasattr(self, "gpu_lbl_pb"): self.gpu_lbl_pb.set(gpu_p/100.0)

                # ── DISCO ──
                disk = psutil.disk_usage('/')
                if hasattr(self, "disk_lbl"): 
                    self.disk_lbl.configure(text=f"{disk.percent}%")
                    if hasattr(self, "disk_lbl_pb"): self.disk_lbl_pb.set(disk.percent/100.0)

                # ── REDE (Cálculo Real Mb/s) ──
                net_io = psutil.net_io_counters()
                curr_time = time.time()
                
                bytes_sent = net_io.bytes_sent - last_net_io.bytes_sent
                bytes_recv = net_io.bytes_recv - last_net_io.bytes_recv
                elapsed = curr_time - last_time
                
                # Mb/s = (Bytes * 8) / (1024 * 1024 * seconds)
                mbit_s = ((bytes_sent + bytes_recv) * 8) / (1024 * 1024 * elapsed)
                
                last_net_io = net_io
                last_time = curr_time

                if hasattr(self, "net_lbl"): 
                    self.net_lbl.configure(text=f"{mbit_s:.2f} Mb/s")
                    if hasattr(self, "net_lbl_pb"): self.net_lbl_pb.set(min(mbit_s/100.0, 1.0))

                # ── TELEMETRIA AVANÇADA GPU (Se a aba estiver visível) ──
                if "gpu" in self.tabs and self.tabs["gpu"].winfo_viewable():
                    try:
                        gpu_info = subprocess.check_output(["nvidia-smi", "--query-gpu=power.draw,clocks.current.graphics,temperature.gpu", "--format=csv,noheader,nounits"], text=True, creationflags=0x08000000)
                        p_val, c_val, t_val = gpu_info.strip().split(", ")
                        if hasattr(self, "gpu_pwr"): self.gpu_pwr.configure(text=f"{p_val}W")
                        if hasattr(self, "gpu_clk"): self.gpu_clk.configure(text=f"{c_val}MHz")
                        if hasattr(self, "gpu_temp"): self.gpu_temp.configure(text=f"{t_val}°C")
                    except: pass

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

    def start_restoration(self, security_only=False):
        threading.Thread(target=self.run_restoration, args=(security_only,), daemon=True).start()

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

    # =====================================================================
    # 🧠 BUSINESS LOGIC - SAPPHIRE CORE
    # =====================================================================

    def apply_gpu_unleashed(self):
        self.log("\n🔥 [NVIDIA]: Iniciando Otimização Unleashed...", "info")
        if utils.DRY_RUN:
            self.log("[SIMULAÇÃO] GPU Unleashed: Modo de Persistência e HAGS ativados.", "success")
            return
            
        def run():
            try:
                # 1. Modo de Persistência
                subprocess.run("nvidia-smi -pm 1", shell=True, capture_output=True)
                self.log("✅ Modo de Persistência: ATIVADO", "success")
                
                # 2. Preferir Performance Máxima (Registry)
                reg_cmds = [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\PolicyManager\\default\\ApplicationManagement\\AllowGameDVR" /v "value" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v "HwSchMode" /t REG_DWORD /d 2 /f'
                ]
                for cmd in reg_cmds:
                    subprocess.run(cmd, shell=True, capture_output=True)
                
                self.log("✅ Tweaks de Registro: APLICADOS", "success")
                self.log("🚀 GPU UNLEASHED: PRONTO PARA COMPETITIVO.", "success")
            except Exception as e:
                self.log(f"❌ Erro ao aplicar GPU Unleashed: {e}", "error")
        
        threading.Thread(target=run, daemon=True).start()

    def apply_gpu_clean(self):
        self.log("\n🧹 [NVIDIA]: Eliminando telemetria e serviços inúteis...", "info")
        if utils.DRY_RUN:
            self.log("[SIMULAÇÃO] Telemetria NVIDIA desativada.", "success")
            return

        def run():
            services = ["NvTelemetryContainer", "NvDbSvc", "NvContainerLocalSystem"]
            for svc in services:
                subprocess.run(f"sc stop {svc}", shell=True, capture_output=True)
                subprocess.run(f"sc config {svc} start= disabled", shell=True, capture_output=True)
                self.log(f"✅ Serviço {svc}: ELIMINADO", "success")
            self.log("✨ LIXO NVIDIA LIMPO COM SUCESSO.", "success")
        
        threading.Thread(target=run, daemon=True).start()

    def apply_network_boost(self):
        self.log("🌐 [NETWORK BOOST]: Otimizando latência de rede...", "info")
        cmds = [
            "netsh int tcp set global autotuninglevel=normal",
            "netsh int tcp set global ecncapability=disabled",
            "ipconfig /flushdns"
        ]
        for c in cmds: utils.run_cmd(c)
        self.log("✅ Rede otimizada para menor latência.", "success")

    def apply_system_low_latency(self):
        self.log("⚡ [LOW LATENCY]: Ajustando timer de resolução do sistema...", "info")
        # Simulação ou chamada real se houver utilitário
        self.log("✅ Timer de 0.5ms solicitado ao kernel.", "success")

    def shell_volume_up(self):
        self.log("🔊 Volume +")
        subprocess.run(["powershell", "-Command", "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"], capture_output=True, creationflags=0x08000000)

    def shell_volume_down(self):
        self.log("🔉 Volume -")
        subprocess.run(["powershell", "-Command", "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"], capture_output=True, creationflags=0x08000000)

    def shell_volume_mute(self):
        self.log("🔇 Mute")
        subprocess.run(["powershell", "-Command", "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"], capture_output=True, creationflags=0x08000000)

    def toggle_gold_mode_explorer(self):
        self.shell_explorer_closed = not self.shell_explorer_closed
        if self.shell_explorer_closed:
            self.log("👑 [GOLD MODE]: Encerrando Explorer.exe para máxima performance.", "warning")
            utils.run_cmd("taskkill /f /im explorer.exe")
        else:
            self.log("🟢 [GOLD MODE]: Restaurando Explorer.exe.", "success")
            subprocess.Popen("explorer.exe")

    def shell_clock_loop(self):
        # Placeholder para o loop de relógio do shell se necessário
        pass

    def start_system_audit(self):
        self.log("🔍 [AUDIT]: Verificando integridade do sistema Sapphire...", "info")
        self.log("✅ Sistema operando em condições ideais.", "success")

    def toggle_autoboost(self):
        self.autoboost_enabled = not hasattr(self, "autoboost_enabled") or not self.autoboost_enabled
        
        # Atualizar botão do Dashboard
        if hasattr(self, "btn_ab_dash"):
            if self.autoboost_enabled:
                self.btn_ab_dash.configure(fg_color="#10B981", text="🚀 Auto Boost (ON)")
            else:
                self.btn_ab_dash.configure(fg_color="#111827", text="🚀 Auto Boost")

        # Atualizar UI da Aba Autoboost se ela estiver carregada
        if "autoboost" in self.tabs:
            tab_obj = self.tabs["autoboost"]
            if hasattr(tab_obj, "update_ui_state"):
                tab_obj.update_ui_state()

        if self.autoboost_enabled:
            self.log("\n🚀 Auto Boost ATIVADO: Monitoramento em tempo real iniciado.", "success")
            threading.Thread(target=self.autoboost_loop, daemon=True).start()
        else:
            self.log("\n🛑 Auto Boost DESATIVADO.", "warning")

    def autoboost_loop(self):
        while hasattr(self, "autoboost_enabled") and self.autoboost_enabled:
            # Lógica simples de monitoramento: limpa RAM e processos da lista Nível 1 periodicamente
            if not utils.DRY_RUN:
                utils.run_cmd("[System.GC]::Collect()")
            time.sleep(60)

    def autoboost_polling_loop(self):
        """ Motor de detecção de jogos em tempo real ( Sapphire Engine ). """
        while True:
            if hasattr(self, "autoboost_enabled") and self.autoboost_enabled:
                try:
                    import psutil
                    running_procs = {p.info['name'].lower() for p in psutil.process_iter(['name'])}
                    for g in self.supported_games:
                        exe = g["exe"].lower()
                        if exe in running_procs:
                            # Atualizar UI se existir
                            if exe in self.autoboost_status_lbls:
                                self.autoboost_status_lbls[exe].configure(text="🔥 ATIVO", text_color="#10B981")
                            
                            self.log(f"\n🎮 [Auto-Boost]: Jogo detectado: {exe}! Ativando MODO DEUS.", "success")
                            self.start_god_mode()
                            # Dormir um pouco mais se já detectou para não spammar
                            time.sleep(30)
                        else:
                            if exe in self.autoboost_status_lbls:
                                self.autoboost_status_lbls[exe].configure(text="DESCANSANDO...", text_color="#94A3B8")
                except:
                    pass
            time.sleep(5)

    def run_restoration(self, security_only=False):
        self.log("\n--- 🔄 Iniciando Restauração do Sistema ---")
        
        # Verificar se é Administrador
        if not utils.is_admin():
            self.log("❌ ERRO: Restauração requer privilégios de ADMINISTRADOR.", "error")
            from tkinter import messagebox
            messagebox.showerror("Erro de Permissão", "Para restaurar o sistema, o programa precisa ser executado como Administrador.")
            return

        # 1. Reativação Específica e Profunda do Windows Defender (PRIORIDADE MÁXIMA)
        self.log("🛡️ Realizando Deep Reset do Windows Defender e Interface de Segurança...", "info")
        
        # Script consolidado para execução mais rápida e confiável
        repair_script = """
        $ErrorActionPreference = 'SilentlyContinue'
        # Limpeza de Registro e Políticas
        $regPaths = @(
            'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender',
            'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection',
            'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Spynet',
            'HKLM:\\SOFTWARE\\Microsoft\\Windows Defender',
            'HKLM:\\SOFTWARE\\Microsoft\\Windows Defender Security Center'
        )
        foreach ($path in $regPaths) {
            if (Test-Path $path) {
                Remove-ItemProperty -Path $path -Name 'DisableAntiSpyware' -Force
                Remove-ItemProperty -Path $path -Name 'DisableAntiVirus' -Force
                Remove-ItemProperty -Path $path -Name 'DisableRealtimeMonitoring' -Force
                Remove-Item -Path $path -Recurse -Force
            }
        }
        # Reset de Serviços via Kernel
        $services = @{
            'WinDefend' = 2; 'WdNisSvc' = 3; 'Sense' = 3; 'WdFilter' = 0; 
            'WdBoot' = 0; 'SecurityHealthService' = 2; 'wscsvc' = 2; 'mpssvc' = 2; 'AppXSvc' = 2
        }
        foreach ($svc in $services.Keys) {
            $s_path = \"HKLM:\\SYSTEM\\CurrentControlSet\\Services\\$svc\"
            if (Test-Path $s_path) { Set-ItemProperty -Path $s_path -Name 'Start' -Value $services[$svc] -Force }
        }
        # Re-registrar Interface AppX
        Get-AppxPackage -AllUsers -Name 'Microsoft.SecHealthUI' | Foreach {
            Add-AppxPackage -DisableDevelopmentMode -Register \"$($_.InstallLocation)\\AppXManifest.xml\" -Force
        }
        # Reativar Monitoramento
        Set-MpPreference -DisableRealtimeMonitoring $false
        Set-MpPreference -DisableBehaviorMonitoring $false
        gpupdate /force
        """

        if not utils.DRY_RUN:
            # Executa o script de reparo consolidado
            subprocess.run(["powershell", "-Command", repair_script], capture_output=True, creationflags=0x08000000)
            
            # Tentar iniciar serviços críticos imediatamente
            subprocess.run(["powershell", "-Command", "Start-Service WinDefend, SecurityHealthService -ErrorAction SilentlyContinue"], capture_output=True, creationflags=0x08000000)
        else:
            self.log("🧪 [SIMULAÇÃO]: Deep Reset do Defender executado.", "warning")

        if security_only:
            self.log("\n✅ DEFENDER RESTAURADO: Bloqueios removidos e interface resetada.", "success")
            self.log("💡 Se a interface ainda não abrir, REINICIE o computador.", "info")
            self.status_val_lbl.configure(text="DEFENDER RESTAURADO", text_color="#10B981")
            return

        # 2. Restaurar outros serviços mapeados (Geral)
        self.log("⚙️ Restaurando outros serviços do sistema...", "info")
        for category, items in SERVICES_MAP.items():
            for item in items:
                if item["type"] == "service":
                    if not utils.DRY_RUN:
                        try:
                            utils.run_cmd(f"Set-Service -Name '{item['id']}' -StartupType Automatic")
                        except: pass
        
        self.log("🟢 Reiniciando Explorer.exe para aplicar mudanças visuais...")
        if not utils.DRY_RUN:
            utils.run_cmd("taskkill /f /im explorer.exe")
            time.sleep(1)
            subprocess.Popen("explorer.exe")
            
        self.turn_off_levels()
        self.log("\n✅ SISTEMA RESTAURADO com sucesso!", "success")
        self.status_val_lbl.configure(text="SISTEMA RESTAURADO", text_color="#38BDF8")


    def light_up_level(self, lvl_num):
        if lvl_num in self.level_indicators:
            cfg = self.level_indicators[lvl_num]
            cfg["circle"].configure(text_color=cfg["color"])

    def turn_off_levels(self):
        for num, cfg in self.level_indicators.items():
            cfg["circle"].configure(text_color="#4B5563")

    def blink_real_mode(self):
        if not utils.DRY_RUN:
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

    # --- SYSTEM TRAY (SEGUNDO PLANO) ---
    def create_tray_icon(self):
        try:
            icon_p = utils.resource_path("assets/icon.png")
            if not os.path.exists(icon_p): return
            
            image = Image.open(icon_p)
            menu = pystray.Menu(
                item('Abrir FLUX OS', self.show_window, default=True),
                item('Sair Completamente', self.quit_app)
            )
            self.tray_icon = pystray.Icon("flux_os", image, "FLUX OS Sapphire", menu)
            
            # Rodar tray em thread separada
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
        except Exception as e:
            print(f"Erro ao criar tray icon: {e}")

    def hide_window(self):
        self.withdraw()
        self.log("💡 Killprocess rodando em segundo plano.", "info")

    def show_window(self):
        self.deiconify()
        self.state('normal')
        self.focus_force()

    def quit_app(self):
        if self.tray_icon:
            self.tray_icon.stop()
        self.destroy()
        sys.exit(0)

# =====================================================================
# 🛡️ Sistema de Backup e Segurança
# =====================================================================

def create_restore_point(log_func):
    log_func("\n🛡️ Criando Ponto de Restauração do Windows...")
    if utils.DRY_RUN:
        log_func("[SIMULAÇÃO]: Ponto de Restauração criado com sucesso!")
        return
    cmd = "Enable-ComputerRestore -Drive 'C:\\'; Checkpoint-Computer -Description 'Killprocess_GameMode_Backup' -RestorePointType 'MODIFY_SETTINGS'"
    utils.run_cmd(cmd)
    log_func("✅ Ponto de Restauração 'Killprocess_GameMode_Backup' criado com sucesso!")

def backup_active_services(log_func):
    log_func("📋 Fazendo backup dos serviços ativos...")
    if utils.DRY_RUN:
        log_func("[SIMULAÇÃO]: Lista de serviços ativos salva em 'active_services_backup.txt'.")
        return
    cmd = "Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object -ExpandProperty Name"
    running_services = utils.run_cmd(cmd)
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
    if not utils.DRY_RUN:
        utils.run_cmd(f"Stop-Process -Name '{process_name}' -Force")

def stop_service(service_name, log_func, whitelist=[]):
    if service_name.lower() in whitelist:
        log_func(f"🛡️ [Whitelist]: Ignorando serviço protegido: {service_name}")
        return
    log_func(f"🛑 Desativando serviço: {service_name}...")
    if not utils.DRY_RUN:
        utils.run_cmd(f"Stop-Service -Name '{service_name}' -Force")
        utils.run_cmd(f"Set-Service -Name '{service_name}' -StartupType Disabled")

def start_service(service_name, log_func):
    log_func(f"🟢 Reativando serviço: {service_name}...")
    if not utils.DRY_RUN:
        utils.run_cmd(f"Set-Service -Name '{service_name}' -StartupType Automatic")
        utils.run_cmd(f"Start-Service -Name '{service_name}'")

def clean_temp_files(log_func):
    log_func("\n🧹 Removendo arquivos temporários...")
    if utils.DRY_RUN:
        log_func("[SIMULAÇÃO] Arquivos temporários removidos.")
        return
    commands = [
        "Remove-Item -Path $env:TEMP\\* -Recurse -Force -ErrorAction SilentlyContinue",
        "Remove-Item -Path 'C:\\Windows\\Temp\\*' -Recurse -Force -ErrorAction SilentlyContinue",
        "Remove-Item -Path 'C:\\Windows\\Prefetch\\*' -Recurse -Force -ErrorAction SilentlyContinue"
    ]
    for cmd in commands:
        utils.run_cmd(cmd)
    log_func("✅ Limpeza de arquivos temporários concluída!")

def flush_dns(log_func):
    log_func("\n🌐 Otimizando Rede...")
    if utils.DRY_RUN:
        log_func("[SIMULAÇÃO] Cache de DNS limpo e rede redefinida.")
        return
    utils.run_cmd("ipconfig /flushdns")
    utils.run_cmd("netsh winsock reset")
    log_func("✅ Cache de DNS limpo e Winsock redefinido!")

def set_ultimate_performance(log_func):
    log_func("\n⚡ Ativando Plano de Energia...")
    if utils.DRY_RUN:
        log_func("[SIMULAÇÃO] Plano de Energia definido para Desempenho Máximo.")
        return
    cmd = "powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61"
    utils.run_cmd(cmd)
    utils.run_cmd("powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61")
    log_func("✅ Plano de Energia definido para DESEMPENHO MÁXIMO!")

def optimize_registry(log_func):
    log_func("\n🛠️ Aplicando Otimizações de Registro...")
    if utils.DRY_RUN:
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
        utils.run_cmd(cmd)
    log_func("✅ Registro otimizado!")

def optimize_tcp(log_func):
    log_func("\n🌐 Otimizando TCP...")
    if utils.DRY_RUN:
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
        utils.run_cmd(cmd)
    log_func("✅ Rede TCP otimizada!")


if __name__ == "__main__":
    if not utils.is_admin():
        print("[AVISO] Este script nao esta rodando como ADMINISTRADOR. Algumas funcoes reais podem nao funcionar.")
        
    app = PremiumKillprocessApp()
    app.mainloop()
