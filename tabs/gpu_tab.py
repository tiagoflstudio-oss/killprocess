import customtkinter as ctk
import threading
import subprocess
from styles import C, get_fonts

class GPUTab(ctk.CTkScrollableFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.app = app
        self.fonts = get_fonts()
        
        # Configuração de expansão
        self._parent_canvas.bind("<Configure>", lambda e: self._parent_canvas.itemconfig(self._parent_canvas.find_withtag("all")[0], width=e.width))
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_telemetry()
        self._build_actions()

    def _build_header(self):
        ctk.CTkLabel(self, text="NVIDIA GPU ELITE OPTIMIZER", font=self.fonts["title"], text_color=C["accent"]).pack(anchor="w", pady=(10, 5))
        ctk.CTkLabel(self, text="Otimizações profundas para placas NVIDIA. Melhore a latência e libere o Power Limit.", 
                     font=self.fonts["label"], text_color=C["muted"]).pack(anchor="w", pady=(0, 20))

    def _build_telemetry(self):
        diag_frame = ctk.CTkFrame(self, fg_color=C["card"], border_width=1, border_color=C["border"], corner_radius=15)
        diag_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(diag_frame, text="▌ TELEMETRIA NVIDIA (LIVE)", font=self.fonts["small_bold"], text_color=C["cyan"]).pack(anchor="w", padx=15, pady=(10, 5))
        
        stats_grid = ctk.CTkFrame(diag_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=15, pady=(0, 15))
        stats_grid.grid_columnconfigure((0, 1, 2), weight=1)

        def add_gpu_stat(title, attr, icon, col):
            f = ctk.CTkFrame(stats_grid, fg_color="#0F172A", corner_radius=10, height=70)
            f.grid(row=0, column=col, padx=5, sticky="nsew")
            f.grid_propagate(False)
            ctk.CTkLabel(f, text=f"{icon} {title}", font=self.fonts["small_bold"], text_color=C["muted"]).pack(pady=(8, 0))
            lbl = ctk.CTkLabel(f, text="--", font=self.fonts["stat_val"], text_color=C["text"])
            lbl.pack()
            setattr(self.app, "gpu_" + attr, lbl)

        add_gpu_stat("POWER LIMIT", "pwr", "⚡", 0)
        add_gpu_stat("CORE CLOCK", "clk", "🔥", 1)
        add_gpu_stat("TEMP", "temp", "🌡️", 2)

    def _build_actions(self):
        actions_grid = ctk.CTkFrame(self, fg_color="transparent")
        actions_grid.pack(fill="x", pady=(0, 15))
        actions_grid.grid_columnconfigure((0, 1), weight=1)

        # Card 1: Power & Latency
        pwr_card = ctk.CTkFrame(actions_grid, fg_color=C["card"], border_width=1, border_color=C["border"], corner_radius=15)
        pwr_card.grid(row=0, column=0, padx=(0, 5), sticky="nsew")
        
        ctk.CTkLabel(pwr_card, text="▌ POWER & LATENCY", font=self.fonts["small_bold"], text_color=C["cyan"]).pack(anchor="w", padx=15, pady=(10, 10))
        
        self.gpu_boost_btn = ctk.CTkButton(pwr_card, text="🚀 ATIVAR NVIDIA UNLEASHED", 
                                           fg_color="#059669", hover_color="#10B981", font=self.fonts["tab_btn"],
                                           height=40, command=self.app.apply_gpu_unleashed)
        self.gpu_boost_btn.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkLabel(pwr_card, text="Aplica Modo de Persistência e remove limites de energia via SMI.", 
                     font=ctk.CTkFont("Segoe UI", 9), text_color=C["muted"], wraplength=300).pack(padx=15, pady=(0, 15))

        # Card 2: Clean & Telemetry
        clean_card = ctk.CTkFrame(actions_grid, fg_color=C["card"], border_width=1, border_color=C["border"], corner_radius=15)
        clean_card.grid(row=0, column=1, padx=(5, 0), sticky="nsew")
        
        ctk.CTkLabel(clean_card, text="▌ TELEMETRY KILLER", font=self.fonts["small_bold"], text_color=C["cyan"]).pack(anchor="w", padx=15, pady=(10, 10))
        
        self.gpu_clean_btn = ctk.CTkButton(clean_card, text="🧹 LIMPAR LIXO NVIDIA", 
                                           fg_color="#EF4444", hover_color="#F43F5E", font=self.fonts["tab_btn"],
                                           height=40, command=self.app.apply_gpu_clean)
        self.gpu_clean_btn.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkLabel(clean_card, text="Desativa NvTelemetry, ShadowPlay e serviços de espionagem de dados.", 
                     font=ctk.CTkFont("Segoe UI", 9), text_color=C["muted"], wraplength=300).pack(padx=15, pady=(0, 15))


