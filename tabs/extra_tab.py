import customtkinter as ctk
import threading
from styles import C, get_fonts

class ExtraTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.fonts = get_fonts()
        
        self._build_header()
        self._build_content()

    def _build_header(self):
        extra_lbl = ctk.CTkLabel(self, text="Recursos Extras & Manutenção", font=self.fonts["title"], text_color="#F8FAFC")
        extra_lbl.pack(anchor="w", pady=(5, 2))

        extra_sub = ctk.CTkLabel(self, text="Ferramentas adicionais para manter seu Windows limpo e rápido.", font=self.fonts["label"], text_color="#94A3B8")
        extra_sub.pack(anchor="w", pady=(0, 20))

    def _build_content(self):
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure((0, 1), weight=1)

        extras = [
            ("🧹 LIMPEZA DE ARQUIVOS TEMP", "Remove cache do Windows, Temp, Prefetch e Logs inúteis.", "#10B981", "clean_temp"),
            ("🌐 FLUSH DNS & WINSOCK", "Redefine a stack de rede e limpa o cache de resolução DNS.", "#3B82F6", "flush_dns"),
            ("⚡ ULTIMATE PERFORMANCE", "Ativa o plano de energia oculto 'Desempenho Máximo'.", "#F59E0B", "power_plan"),
            ("🛠️ REGISTRY OPTIMIZER", "Aplica tweaks de registro para prioridade de Games e I/O.", "#EC4899", "registry_opt"),
            ("📉 TCP OPTIMIZATION", "Reduz o overhead do protocolo TCP para menor Ping.", "#06B6D4", "tcp_opt")
        ]

        for i, (title, desc, color, cmd) in enumerate(extras):
            card = ctk.CTkFrame(grid, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=15)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(card, text=title, font=self.fonts["section"], text_color=color).pack(anchor="w", padx=20, pady=(20, 5))
            ctk.CTkLabel(card, text=desc, font=self.fonts["label_small"], text_color="#94A3B8", wraplength=300).pack(anchor="w", padx=20, pady=(0, 15))
            
            ctk.CTkButton(card, text="EXECUTAR", fg_color="#1F2937", hover_color=color, font=self.fonts["small_bold"], 
                          height=36, corner_radius=8, command=lambda c=cmd: self.app.run_extra_optimization(c)).pack(fill="x", padx=20, pady=(0, 20))
