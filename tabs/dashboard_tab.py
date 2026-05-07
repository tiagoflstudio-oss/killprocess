import customtkinter as ctk
import threading
from styles import C, get_fonts
from services import SERVICES_MAP

class DashboardTab(ctk.CTkScrollableFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.app = app
        self.fonts = get_fonts()
        
        # Configuração de expansão
        self._parent_canvas.bind("<Configure>", lambda e: self._parent_canvas.itemconfig(self._parent_canvas.find_withtag("all")[0], width=e.width))
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_levels()
        self._build_metrics()
        self._build_actions_and_radar()

    def _build_header(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ctk.CTkLabel(hdr, text="CENTRO DE CONTROLE", font=self.fonts["title"],
                     text_color=C["text"]).pack(side="left")
        
        self.app.status_val_lbl = ctk.CTkLabel(
            hdr, text="● PRONTO", font=ctk.CTkFont("Segoe UI", 11, "bold"),
            text_color=C["accent"], fg_color="#051408", corner_radius=6, padx=10, pady=3)
        self.app.status_val_lbl.pack(side="right")

    def _build_levels(self):
        lvl_card = ctk.CTkFrame(self, fg_color=C["card"], border_width=1,
                                 border_color=C["border"], corner_radius=15)
        lvl_card.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(lvl_card, text="▌ NÍVEIS DE OTIMIZAÇÃO (STATUS DO KERNEL)",
                     font=self.fonts["small_bold"],
                     text_color=C["cyan"]).pack(anchor="w", padx=15, pady=(8, 4))

        self.lights_frame = ctk.CTkFrame(lvl_card, fg_color="transparent")
        self.lights_frame.pack(fill="x", expand=True, padx=15, pady=(0, 6))

        self.app.level_indicators = {}
        self.app.level_checkboxes_dashboard = {}

        self.level_desc_lbl = ctk.CTkLabel(
            lvl_card, text="Passe o mouse sobre um nível para ver detalhes da otimização.",
            font=self.fonts["label"], text_color=C["muted"])
        self.level_desc_lbl.pack(anchor="w", padx=15, pady=(0, 10))

        def update_desc(txt): self.level_desc_lbl.configure(text=txt)

        levels_data = [
            (1, "N1", "Apps", "#00FF88", "Fecha navegadores e apps em segundo plano."),
            (2, "N2", "Print", "#00FFB2", "Impressora e manutenção."),
            (3, "N3", "Telemetria", "#FFFF00", "Telemetria e diagnósticos."),
            (4, "N4", "Xbox/BT", "#FF8000", "Xbox Live e Bluetooth."),
            (5, "N5", "Net/Maps", "#FF0055", "Rede e mapas offline."),
            (6, "N6", "Crypto", "#00CCFF", "Segurança e biometria."),
            (7, "N7", "God Mode", "#FFD700", "Modo Deus: Performance Gamer."),
            (8, "N8", "Polish", "#00FF88", "Polish: Serviços fantasmas."),
            (9, "N9", "Engine", "#C084FC", "Deep Engine: Otimização de núcleo."),
            (10, "N10", "Security", "#EF4444", "⚠️ AVISO: Desativa Defender.")
        ]
        
        row_idx = 0
        col_idx = 0
        for num, lvl_id, name, color, desc in levels_data:
            f = ctk.CTkFrame(self.lights_frame, fg_color="transparent")
            f.grid(row=row_idx, column=col_idx, sticky="nsew", padx=4, pady=2)
            cb = ctk.CTkCheckBox(f, text=name, font=ctk.CTkFont("Segoe UI", 9, "bold"),
                                  fg_color=color, hover_color=color, width=16,
                                  command=lambda d=desc: update_desc(d))
            if num <= 8: cb.select()
            cb.pack(side="left", padx=(0, 2))
            cb.bind("<Enter>", lambda e, d=desc: update_desc(d))
            
            try:
                full_key = list(SERVICES_MAP.keys())[num-1]
                self.app.level_checkboxes_dashboard[full_key] = cb
            except: pass
                
            self.app.level_indicators[num] = {"circle": cb, "cb": cb, "color": color}
            col_idx += 1
            if col_idx > 4: 
                col_idx = 0
                row_idx += 1
        self.lights_frame.grid_columnconfigure((0,1,2,3,4), weight=1)

    def _build_metrics(self):
        m_frame = ctk.CTkFrame(self, fg_color="transparent")
        m_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        m_frame.grid_columnconfigure((0, 1, 2), weight=1)

        def add_m_card(title, attr, color, r, c):
            card = ctk.CTkFrame(m_frame, fg_color=C["card"], border_width=1, 
                                 border_color=C["border"], corner_radius=15)
            card.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
            ctk.CTkLabel(card, text=title, font=self.fonts["small_bold"], 
                         text_color=C["cyan"]).pack(anchor="w", padx=10, pady=(6, 0))
            lbl = ctk.CTkLabel(card, text="--", font=self.fonts["stat_val"], text_color=C["text"])
            lbl.pack(anchor="w", padx=10)
            setattr(self.app, attr, lbl)
            pb = ctk.CTkProgressBar(card, height=4, progress_color=color, fg_color="#1E2631")
            pb.pack(fill="x", padx=10, pady=(0, 6))
            pb.set(0.2)
            setattr(self.app, attr + "_pb", pb)

        add_m_card("RAM EM USO", "ram_lbl", "#10B981", 0, 0)
        add_m_card("GPU LOAD", "gpu_lbl", "#F43F5E", 0, 1)
        add_m_card("NETWORK", "net_lbl", "#C084FC", 0, 2)
        add_m_card("CPU USAGE", "cpu_lbl", C["accent"], 1, 0)
        add_m_card("DISK USAGE", "disk_lbl", "#2DD4BF", 1, 1)
        add_m_card("PROCESSOS", "proc_lbl", "#38BDF8", 1, 2)

    def _build_actions_and_radar(self):
        row3 = ctk.CTkFrame(self, fg_color="transparent")
        row3.grid(row=3, column=0, sticky="ew", pady=(0, 4))
        row3.grid_columnconfigure(0, weight=2)
        row3.grid_columnconfigure(1, weight=1)

        act = ctk.CTkFrame(row3, fg_color=C["card"], border_width=1,
                            border_color=C["border"], corner_radius=10)
        act.grid(row=0, column=0, padx=(0, 6), sticky="nsew")
        ctk.CTkLabel(act, text="▌ AÇÕES RÁPIDAS (ONE-CLICK)", font=self.fonts["small_bold"], text_color=C["cyan"]).pack(anchor="w", padx=14, pady=(10, 8))

        btn_grid = ctk.CTkFrame(act, fg_color="transparent")
        btn_grid.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        btn_grid.grid_columnconfigure((0, 1, 2), weight=1, uniform="buttons")

        self.app.full_opt_btn = ctk.CTkButton(
            btn_grid, text="🚀\nOTIMIZAR TUDO", fg_color="#0D47A1", hover_color="#1565C0",
            font=self.fonts["tab_btn"], height=100, corner_radius=10,
            command=self.app.start_full_optimization)
        self.app.full_opt_btn.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

        self.app.god_mode_btn = ctk.CTkButton(
            btn_grid, text="👑\nGOD MODE", fg_color=C["gold"], hover_color="#C8A800",
            font=self.fonts["tab_btn"], height=100, corner_radius=10, text_color="#0A0A0A",
            command=self.app.start_god_mode)
        self.app.god_mode_btn.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")

        self.app.optimize_selection_btn = ctk.CTkButton(
            btn_grid, text="⚡\nGAMER CUSTOM", fg_color="#1E2631", hover_color="#3B82F6",
            border_width=1, border_color="#3B82F6", font=self.fonts["tab_btn"], height=100, corner_radius=10,
            command=self.app.start_optimize_selection)
        self.app.optimize_selection_btn.grid(row=0, column=2, padx=8, pady=8, sticky="nsew")

        shortcuts_row = ctk.CTkFrame(act, fg_color="transparent")
        shortcuts_row.pack(fill="x", padx=10, pady=(0, 8))
        shortcuts_row.grid_columnconfigure((0, 1, 2), weight=1)

        self.app.btn_ab_dash = ctk.CTkButton(
            shortcuts_row, text="🚀 Auto Boost", fg_color="#111827", hover_color="#10B981",
            border_width=1, border_color="#10B981", font=self.fonts["card_title"], height=32, corner_radius=6,
            command=self.app.toggle_autoboost)
        self.app.btn_ab_dash.grid(row=0, column=0, padx=3, sticky="nsew")

        self.app.btn_maint_dash = ctk.CTkButton(
            shortcuts_row, text="🛠️ Executar Tudo", fg_color="#111827", hover_color="#10B981",
            border_width=1, border_color="#10B981", font=self.fonts["card_title"], height=32, corner_radius=6,
            command=lambda: threading.Thread(target=self.app.run_all_maintenance, daemon=True).start())
        self.app.btn_maint_dash.grid(row=0, column=1, padx=3, sticky="nsew")

        self.app.btn_shell_dash = ctk.CTkButton(
            shortcuts_row, text="👑 Shell Mode", fg_color="#111827", hover_color=C["gold"],
            border_width=1, border_color=C["gold"], font=self.fonts["card_title"], height=32, corner_radius=6,
            command=self.app.toggle_gold_mode_explorer)
        self.app.btn_shell_dash.grid(row=0, column=2, padx=3, sticky="nsew")

        self.restore_security_btn = ctk.CTkButton(
            act, text="🛡️  REATIVAR WINDOWS DEFENDER", fg_color="#1E1B4B", hover_color="#3730A3",
            border_width=1, border_color="#4338CA", font=self.fonts["small_bold"], height=35, corner_radius=6,
            text_color="#E2E8F0", command=self.app.start_restoration)
        self.restore_security_btn.pack(fill="x", padx=14, pady=(2, 5))

        self.app.restore_btn = ctk.CTkButton(
            act, text="🔄  RESTAURAR TODOS OS PADRÕES DO SISTEMA", fg_color="#0F172A", hover_color="#EF4444",
            border_width=1, border_color="#1E293B", font=self.fonts["small_bold"], height=35, corner_radius=6,
            text_color=C["muted"], command=self.app.start_restoration)
        self.app.restore_btn.pack(fill="x", padx=14, pady=(2, 10))

        radar_card = ctk.CTkFrame(row3, fg_color=C["card"], border_width=1, border_color=C["border"], corner_radius=10)
        radar_card.grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(radar_card, text="▌ PERFORMANCE RADAR", font=self.fonts["small_bold"], text_color=C["cyan"]).pack(anchor="w", padx=12, pady=(10, 4))
        self.app.radar_canvas = ctk.CTkCanvas(radar_card, bg=C["card"], highlightthickness=0, width=240, height=120)
        self.app.radar_canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.app.draw_radar_chart()
