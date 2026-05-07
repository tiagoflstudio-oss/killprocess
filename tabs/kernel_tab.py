import customtkinter as ctk
import threading
from styles import C, get_fonts

class KernelTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.fonts = get_fonts()
        
        self._build_header()
        self._build_content()

    def _build_header(self):
        kernel_lbl = ctk.CTkLabel(self, text="Modificações de Kernel & Baixo Nível", font=self.fonts["title"], text_color="#F8FAFC")
        kernel_lbl.pack(anchor="w", pady=(5, 2))

        kernel_sub = ctk.CTkLabel(self, text="Avisos: Estas modificações alteram o comportamento principal do Windows para reduzir a latência de sistema.", font=self.fonts["label"], text_color="#EF4444")
        kernel_sub.pack(anchor="w", pady=(0, 20))

    def _build_content(self):
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure((0, 1), weight=1)

        tweaks = [
            ("🚀 MSI MODE (GPU)", "Força interrupções MSI para latência zero em vídeo.", "msi_mode"),
            ("🧠 CPU SCHEDULER", "Ajusta o Win32PrioritySeparation para 0x26.", "cpu_scheduler"),
            ("🌐 NETWORK THROTTLE", "Remove o limite de rede em multimídia.", "net_throttle"),
            ("📦 PROCESS GROUPING", "Agrupa serviços svchost para liberar RAM.", "svchost_grouping"),
            ("🛡️ DISABLE VBS/HVCI", "Desativa segurança por virtualização (Ganha FPS).", "vbs_disable"),
            ("🔄 RESTORE KERNEL", "Volta todas as configurações para padrão MS.", "kernel_restore")
        ]

        for i, (title, desc, cmd) in enumerate(tweaks):
            card = ctk.CTkFrame(grid, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=15)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(card, text=title, font=self.fonts["section"], text_color="#00FFFF").pack(anchor="w", padx=20, pady=(20, 5))
            ctk.CTkLabel(card, text=desc, font=self.fonts["label_small"], text_color="#94A3B8", wraplength=300).pack(anchor="w", padx=20, pady=(0, 15))
            
            ctk.CTkButton(card, text="APLICAR TWEAK", fg_color="#111827", hover_color="#00FFFF", border_width=1, border_color="#00FFFF", 
                          font=self.fonts["small_bold"], height=36, corner_radius=8, command=lambda c=cmd: self.app.run_kernel_optimization(c)).pack(fill="x", padx=20, pady=(0, 20))
