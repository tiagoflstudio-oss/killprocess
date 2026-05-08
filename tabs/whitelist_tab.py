import customtkinter as ctk
from styles import C, get_fonts

class WhitelistTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.fonts = get_fonts()
        
        self._build_header()
        self._build_content()

    def _build_header(self):
        wl_lbl = ctk.CTkLabel(self, text="Gerenciar Whitelist (Lista Segura)", font=self.fonts["title"], text_color="#F8FAFC")
        wl_lbl.pack(anchor="w", pady=(5, 2))

        wl_sub = ctk.CTkLabel(self, text="Adicione processos ou serviços que o FLUX OS nunca deve encerrar.", font=self.fonts["label"], text_color="#94A3B8")
        wl_sub.pack(anchor="w", pady=(0, 20))

    def _build_content(self):
        panel = ctk.CTkFrame(self, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        panel.pack(fill="both", expand=True)

        input_f = ctk.CTkFrame(panel, fg_color="transparent")
        input_f.pack(fill="x", padx=20, pady=20)

        self.app.wl_entry = ctk.CTkEntry(input_f, placeholder_text="Ex: special_service.exe, MyApp...", height=40, corner_radius=8)
        self.app.wl_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(input_f, text="ADICIONAR", fg_color="#1E2631", hover_color=C["hover"], font=self.fonts["small_bold"], height=40, corner_radius=8, command=self.app.add_to_whitelist).pack(side="left", padx=5)
        
        ctk.CTkButton(input_f, text="🔍 AUTO-DETECT", fg_color="#10B981", hover_color="#059669", 
                      text_color="#051408", font=self.fonts["small_bold"], height=40, corner_radius=8, 
                      command=self.app.auto_detect_whitelist).pack(side="left", padx=5)

        self.app.wl_scroll = ctk.CTkScrollableFrame(panel, fg_color="#0D0F12", border_width=1, border_color="#1E2B2A", height=300)
        self.app.wl_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Initial render
        self.app.update_whitelist_ui()
