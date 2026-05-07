import customtkinter as ctk
import utils
from styles import C, get_fonts

class SettingsTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.fonts = get_fonts()
        
        self._build_header()
        self._build_operation_mode()
        self._build_appearance()
        self._build_about()

    def _build_header(self):
        settings_lbl = ctk.CTkLabel(self, text="Configurações", font=self.fonts["title"], text_color="#F8FAFC")
        settings_lbl.pack(anchor="w", pady=(5, 2))

        settings_sub = ctk.CTkLabel(self, text="Ajustes avançados do aplicativo e comportamento do sistema.", font=self.fonts["label"], text_color="#94A3B8")
        settings_sub.pack(anchor="w", pady=(0, 20))

    def _build_operation_mode(self):
        panel = ctk.CTkFrame(self, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        panel.pack(fill="x", pady=10)

        ctk.CTkLabel(panel, text="Modo de Operação", font=self.fonts["section"], text_color="#10B981").pack(anchor="w", padx=20, pady=(20, 5))
        
        ctk.CTkLabel(
            panel, text="Por padrão, o modo Simulação fica ATIVO. Desative para aplicar as modificações reais.",
            font=self.fonts["label"], text_color="#94A3B8"
        ).pack(anchor="w", padx=20, pady=(0, 15))

        self.dry_run_switch = ctk.CTkSwitch(
            panel, text="ATIVAR MODO REAL (CUIDADO)", font=self.fonts["label"], 
            fg_color="#1F2937", progress_color="#10B981", command=self.toggle_dry_run
        )
        self.dry_run_switch.pack(anchor="w", padx=20, pady=(0, 20))
        
        if not utils.DRY_RUN:
            self.dry_run_switch.select()

    def _build_appearance(self):
        panel = ctk.CTkFrame(self, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        panel.pack(fill="x", pady=10)

        ctk.CTkLabel(panel, text="Aparência & UI", font=self.fonts["section"], text_color="#00FFFF").pack(anchor="w", padx=20, pady=(20, 5))
        
        ctk.CTkCheckBox(panel, text="Efeitos de Transparência (Glassmorphism)", font=self.fonts["label"]).pack(anchor="w", padx=20, pady=5)
        ctk.CTkCheckBox(panel, text="Animações de Transição Suaves", font=self.fonts["label"]).pack(anchor="w", padx=20, pady=(5, 20))

    def _build_about(self):
        panel = ctk.CTkFrame(self, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        panel.pack(fill="x", pady=10)
        
        ctk.CTkLabel(panel, text="Sobre o FLUX OS", font=self.fonts["section"], text_color=C["accent"]).pack(anchor="w", padx=20, pady=(20, 5))
        ctk.CTkLabel(panel, text=f"Versão: {utils.VERSION} (Sapphire Architecture)", font=self.fonts["label"], text_color="#E2E8F0").pack(anchor="w", padx=20, pady=2)
        ctk.CTkLabel(panel, text="Desenvolvido para Performance Extrema em Gaming.", font=self.fonts["label_small"], text_color="#94A3B8").pack(anchor="w", padx=20, pady=(0, 20))

    def toggle_dry_run(self):
        is_on = self.dry_run_switch.get()
        utils.DRY_RUN = not is_on
        
        if utils.DRY_RUN:
            self.app.mode_pill.configure(text="● SIMULAÇÃO", text_color=C["orange"], fg_color="#140A00")
            self.app.log("\n🧪 Modo Simulação ATIVADO. Nenhuma ação real será executada.", "warning")
        else:
            self.app.mode_pill.configure(text="● MODO REAL", text_color="#00FF88", fg_color="#001408")
            self.app.log("\n⚠️ MODO REAL ATIVADO! As alterações afetarão o sistema.", "warning")
