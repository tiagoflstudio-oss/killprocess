import customtkinter as ctk
import threading
from styles import C, get_fonts

class OptimizeCenterTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.fonts = get_fonts()
        
        self._build_header()
        self._build_grid()

    def _build_header(self):
        opt_lbl = ctk.CTkLabel(self, text="NVIDIA & Gaming Optimize Center", font=self.fonts["title"], text_color="#F8FAFC")
        opt_lbl.pack(anchor="w", pady=(5, 2))

        opt_sub = ctk.CTkLabel(self, text="Central de otimizações de um clique para hardware específico e drivers.", font=self.fonts["label"], text_color="#94A3B8")
        opt_sub.pack(anchor="w", pady=(0, 20))

    def _build_grid(self):
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure((0, 1), weight=1)

        options = [
            ("🔥 NVIDIA UNLEASHED", "Aplica o Modo de Persistência e remove Power Limit via SMI.", "#059669", self.app.apply_gpu_unleashed),
            ("🧹 TELEMETRY KILLER", "Desativa serviços de espionagem da NVIDIA e ShadowPlay.", "#EF4444", self.app.apply_gpu_clean),
            ("⚡ LATENCY REDUCER", "Otimiza o timer de sistema (HPET) e BCDedit.", "#3B82F6", lambda: self.app.run_kernel_optimization("msi_mode")),
            ("💾 RAM PURGE (FLUSH)", "Limpa cache de standby e força Garbage Collection.", "#8B5CF6", lambda: self.app.run_extra_optimization("ram_flush"))
        ]

        for i, (title, desc, color, cmd) in enumerate(options):
            card = ctk.CTkFrame(grid, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=15)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(card, text=title, font=self.fonts["section"], text_color=color).pack(anchor="w", padx=20, pady=(20, 5))
            ctk.CTkLabel(card, text=desc, font=self.fonts["label_small"], text_color="#94A3B8", wraplength=300).pack(anchor="w", padx=20, pady=(0, 15))
            
            ctk.CTkButton(card, text="EXECUTAR AGORA", fg_color=color, hover_color=color, font=self.fonts["small_bold"], 
                          height=36, corner_radius=8, text_color="#0D0F12", command=cmd).pack(fill="x", padx=20, pady=(0, 20))
