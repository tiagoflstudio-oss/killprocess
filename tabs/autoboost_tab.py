import customtkinter as ctk
import threading
from styles import C, get_fonts

class AutoboostTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.fonts = get_fonts()
        
        self._build_header()
        self._build_status_panel()
        self._build_games_list()

    def _build_header(self):
        ab_lbl = ctk.CTkLabel(self, text="Módulo Auto-Boost (Automação Proativa)", font=self.fonts["title"], text_color="#F8FAFC")
        ab_lbl.pack(anchor="w", pady=(5, 2))

        ab_sub = ctk.CTkLabel(self, text="Deixe o FLUX OS monitorar seus jogos e aplicar o nível de otimização automaticamente em tempo real.", font=self.fonts["label"], text_color="#94A3B8")
        ab_sub.pack(anchor="w", pady=(0, 15))

    def _build_status_panel(self):
        panel = ctk.CTkFrame(self, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        panel.pack(fill="x", pady=5)

        self.ab_toggle_btn = ctk.CTkButton(
            panel, text="🟢 ATIVAR MONITORAMENTO AUTO-BOOST", fg_color="#10B981", hover_color="#059669",
            font=self.fonts["tab_btn"], height=46, corner_radius=10, text_color="#0D0F12",
            command=self.app.toggle_autoboost
        )
        self.ab_toggle_btn.pack(side="left", padx=20, pady=20)

        self.ab_state_lbl = ctk.CTkLabel(
            panel, text="Status do Monitoramento: DESATIVADO", font=self.fonts["section"], text_color="#EF4444"
        )
        self.ab_state_lbl.pack(side="left", padx=10, pady=20)

    def update_ui_state(self):
        if self.app.autoboost_enabled:
            self.ab_toggle_btn.configure(text="🔴 DESATIVAR MONITORAMENTO AUTO-BOOST", fg_color="#EF4444", hover_color="#DC2626")
            self.ab_state_lbl.configure(text="Status do Monitoramento: ATIVADO", text_color="#10B981")
        else:
            self.ab_toggle_btn.configure(text="🟢 ATIVAR MONITORAMENTO AUTO-BOOST", fg_color="#10B981", hover_color="#059669")
            self.ab_state_lbl.configure(text="Status do Monitoramento: DESATIVADO", text_color="#EF4444")

    def _build_games_list(self):
        games_frame = ctk.CTkFrame(self, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        games_frame.pack(fill="both", expand=True, pady=10)

        title_games = ctk.CTkLabel(games_frame, text="🎮 JOGOS SUPORTADOS & MONITORADOS", font=self.fonts["small_bold"], text_color="#10B981")
        title_games.pack(anchor="w", padx=15, pady=(15, 10))

        # Headers
        header_row = ctk.CTkFrame(games_frame, fg_color="#1E2B2A", corner_radius=6)
        header_row.pack(fill="x", padx=15, pady=(0, 5))

        headers = [("🖥️ EXECUTÁVEL (.exe)", 220), ("🕹️ JOGO", 320), ("📊 STATUS EM TEMPO REAL", 220)]
        for i, (text, width) in enumerate(headers):
            lbl = ctk.CTkLabel(header_row, text=text, font=self.fonts["label"], text_color="#10B981")
            lbl.grid(row=0, column=i, padx=15, pady=8, sticky="w")
            header_row.grid_columnconfigure(i, weight=1, minsize=width)

        self.app.autoboost_status_lbls = {}
        self.app.autoboost_checkboxes = {}

        for game in self.app.supported_games:
            row = ctk.CTkFrame(games_frame, fg_color="transparent")
            row.pack(fill="x", padx=15)
            
            cb = ctk.CTkCheckBox(row, text=game["exe"], font=self.fonts["label"], fg_color="#10B981")
            cb.select()
            cb.grid(row=0, column=0, padx=15, pady=6, sticky="w")
            
            ctk.CTkLabel(row, text=game["name"], font=self.fonts["label"], text_color="#E2E8F0").grid(row=0, column=1, padx=15, pady=6, sticky="w")
            
            status = ctk.CTkLabel(row, text="DESCANSANDO...", font=self.fonts["label_italic"], text_color="#94A3B8")
            status.grid(row=0, column=2, padx=15, pady=6, sticky="w")
            
            self.app.autoboost_status_lbls[game["exe"]] = status
            self.app.autoboost_checkboxes[game["exe"]] = cb
            
            row.grid_columnconfigure(0, weight=2, minsize=220)
            row.grid_columnconfigure(1, weight=3, minsize=320)
            row.grid_columnconfigure(2, weight=2, minsize=220)
