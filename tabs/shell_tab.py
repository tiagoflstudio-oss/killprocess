import customtkinter as ctk
from styles import C, get_fonts

class ShellTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.fonts = get_fonts()
        
        self._build_header()
        self._build_controls()
        self._build_launcher()

    def _build_header(self):
        sh_lbl = ctk.CTkLabel(self, text="Console Shell & Game Launcher", font=self.fonts["title"], text_color="#F8FAFC")
        sh_lbl.pack(anchor="w", pady=(5, 2))

        sh_sub = ctk.CTkLabel(self, text="Controle total do sistema via atalhos e execução direta.", font=self.fonts["label"], text_color="#94A3B8")
        sh_sub.pack(anchor="w", pady=(0, 20))

    def _build_controls(self):
        panel = ctk.CTkFrame(self, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        panel.pack(fill="x", pady=10)

        ctk.CTkLabel(panel, text="🎛️ CONTROLES RÁPIDOS", font=self.fonts["section"], text_color="#F59E0B").pack(anchor="w", padx=20, pady=(15, 10))
        
        btn_f = ctk.CTkFrame(panel, fg_color="transparent")
        btn_f.pack(fill="x", padx=20, pady=(0, 20))

        btns = [
            ("🔇 MUTE", self.app.shell_volume_mute),
            ("🔉 VOL -", self.app.shell_volume_down),
            ("🔊 VOL +", self.app.shell_volume_up),
            ("👑 GOLD MODE", self.app.toggle_gold_mode_explorer)
        ]

        for i, (txt, cmd) in enumerate(btns):
            b = ctk.CTkButton(btn_f, text=txt, fg_color="#1F2937", hover_color="#F59E0B", font=self.fonts["small_bold"], height=36, corner_radius=8, command=cmd)
            b.pack(side="left", padx=5, fill="x", expand=True)

    def _build_launcher(self):
        panel = ctk.CTkFrame(self, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        panel.pack(fill="both", expand=True, pady=10)

        ctk.CTkLabel(panel, text="🚀 EXECUTAR COMANDO OU JOGO", font=self.fonts["section"], text_color="#3B82F6").pack(anchor="w", padx=20, pady=(15, 5))
        
        self.app.shell_entry = ctk.CTkEntry(panel, placeholder_text="Digite o comando ou caminho do .exe...", height=42, corner_radius=8)
        self.app.shell_entry.pack(fill="x", padx=20, pady=10)
        
        self.app.shell_entry.bind("<Return>", lambda e: self.app.shell_execute())

        ctk.CTkButton(panel, text="EXECUTAR", fg_color="#3B82F6", hover_color="#2563EB", font=self.fonts["tab_btn"], height=42, corner_radius=8, command=self.app.shell_execute).pack(fill="x", padx=20, pady=(0, 20))
