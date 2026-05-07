import customtkinter as ctk
import threading
import webbrowser
from styles import C, get_fonts
import utils

class RecoveryTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.fonts = get_fonts()
        
        self._build_header()
        self._build_content()

    def _build_header(self):
        manage_lbl = ctk.CTkLabel(self, text="Recuperação do Sistema", font=self.fonts["title"], text_color="#F8FAFC")
        manage_lbl.pack(anchor="w", pady=(5, 2))

        self.manage_sub = ctk.CTkLabel(
            self, text="Gerencie pontos de restauração e reverta alterações indesejadas do Windows.", 
            font=self.fonts["label"], text_color="#94A3B8"
        )
        self.manage_sub.pack(anchor="w", pady=(0, 20))

    def _build_content(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # Ações Rápidas
        actions_frame = ctk.CTkFrame(self.container, fg_color=C["card"], border_width=1, border_color=C["border"], corner_radius=10)
        actions_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(actions_frame, text="🛡️ AÇÕES DE SEGURANÇA", font=self.fonts["small_bold"], text_color=C["cyan"]).pack(anchor="w", padx=15, pady=(10, 5))
        
        btns_f = ctk.CTkFrame(actions_frame, fg_color="transparent")
        btns_f.pack(fill="x", padx=10, pady=(0, 10))

        self.create_rp_btn = ctk.CTkButton(
            btns_f, text="➕ Criar Novo Ponto", fg_color="#10B981", hover_color="#059669",
            font=self.fonts["tab_btn"], height=35, command=self.create_rp
        )
        self.create_rp_btn.pack(side="left", padx=5, expand=True, fill="x")

        self.refresh_btn = ctk.CTkButton(
            btns_f, text="🔄 Atualizar Lista", fg_color="#1E2631", hover_color="#334155",
            font=self.fonts["tab_btn"], height=35, command=self.load_points
        )
        self.refresh_btn.pack(side="left", padx=5, expand=True, fill="x")

        # Reparo de Segurança (Destaque)
        ctk.CTkLabel(actions_frame, text="☢️ REPARO CRÍTICO", font=self.fonts["small_bold"], text_color=C["red"]).pack(anchor="w", padx=15, pady=(10, 0))
        
        self.deep_fix_btn = ctk.CTkButton(
            actions_frame, text="🛡️ RESTAURAR SEGURANÇA TOTAL (FIX IT ADMIN)", 
            fg_color="#7F1D1D", hover_color="#991B1B", text_color="#FCA5A5",
            font=self.fonts["tab_btn"], height=40, border_width=1, border_color="#F87171",
            command=self.run_deep_security_fix
        )
        self.deep_fix_btn.pack(fill="x", padx=15, pady=(5, 15))

        # Guia de Reparo para o Cliente
        guide_frame = ctk.CTkFrame(self.container, fg_color="#0F172A", border_width=1, border_color="#1E293B", corner_radius=10)
        guide_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(guide_frame, text="📋 GUIA DE RECUPERAÇÃO PARA O CLIENTE", font=self.fonts["small_bold"], text_color="#94A3B8").pack(pady=(10, 5))
        
        steps = [
            "1. Clique no botão vermelho 'RESTAURAR SEGURANÇA TOTAL' acima.",
            "2. Clique no botão abaixo para baixar a ferramenta oficial da Microsoft.",
            "3. Execute o arquivo baixado como Administrador (a tela piscará).",
            "4. REINICIE o computador para finalizar o processo."
        ]
        
        for step in steps:
            ctk.CTkLabel(guide_frame, text=step, font=self.fonts["label_small"], text_color="#64748B", anchor="w").pack(fill="x", padx=20)

        self.download_tool_btn = ctk.CTkButton(
            guide_frame, text="📥 BAIXAR FERRAMENTA DE REPARO (MICROSOFT)", 
            fg_color="#334155", hover_color="#475569",
            font=self.fonts["small_bold"], height=32,
            command=lambda: webbrowser.open("https://catalog.s.download.windowsupdate.com/c/msdownload/update/software/defu/2024/02/securityhealthsetup_e16941e14861a6d24750ecdf05c548189b33182a.exe")
        )
        self.download_tool_btn.pack(pady=15, padx=20, fill="x")

        # Lista de Pontos
        self.list_frame = ctk.CTkScrollableFrame(self.container, fg_color=C["card"], border_width=1, border_color=C["border"], corner_radius=10)
        self.list_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(self.list_frame, text="📅 HISTÓRICO DE PONTOS DE RESTAURAÇÃO", font=self.fonts["small_bold"], text_color=C["cyan"]).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.points_container = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        self.points_container.pack(fill="both", expand=True)

        self.load_points()

    def load_points(self):
        for child in self.points_container.winfo_children():
            child.destroy()
        
        ctk.CTkLabel(self.points_container, text="Buscando histórico no sistema...", font=self.fonts["label"], text_color=C["muted"]).pack(pady=20)
        
        threading.Thread(target=self._load_points_thread, daemon=True).start()

    def _load_points_thread(self):
        points = utils.get_restore_points()
        # Inverter para mostrar os mais recentes primeiro
        if isinstance(points, list):
            points = points[::-1]
        
        self.app.after(0, lambda: self._render_points(points))

    def _render_points(self, points):
        for child in self.points_container.winfo_children():
            child.destroy()

        if not points:
            ctk.CTkLabel(self.points_container, text="Nenhum ponto de restauração encontrado ou o serviço está desativado.", font=self.fonts["label"], text_color=C["muted"]).pack(pady=20)
            return

        # Cabeçalhos
        header = ctk.CTkFrame(self.points_container, fg_color="#1E2631", height=30)
        header.pack(fill="x", pady=2)
        ctk.CTkLabel(header, text="DATA / HORA", font=self.fonts["small_bold"], width=130, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(header, text="DESCRIÇÃO", font=self.fonts["small_bold"], anchor="w").pack(side="left", padx=10, expand=True, fill="x")
        ctk.CTkLabel(header, text="AÇÃO", font=self.fonts["small_bold"], width=80).pack(side="right", padx=10)

        for p in points:
            row = ctk.CTkFrame(self.points_container, fg_color="transparent")
            row.pack(fill="x", pady=1)
            
            ctk.CTkLabel(row, text=p.get("Date", "N/A"), font=self.fonts["label"], width=130, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=p.get("Description", "N/A"), font=self.fonts["label"], anchor="w").pack(side="left", padx=10, expand=True, fill="x")
            
            restore_btn = ctk.CTkButton(
                row, text="REVERTER", width=70, height=24, fg_color="#F43F5E", hover_color="#BE123C",
                font=ctk.CTkFont("Segoe UI", 9, "bold"), command=lambda sn=p.get("SequenceNumber"): self.restore_to(sn)
            )
            restore_btn.pack(side="right", padx=10, pady=5)
            
            # Separador
            ctk.CTkFrame(self.points_container, fg_color="#1E2631", height=1).pack(fill="x", padx=10)

    def create_rp(self):
        self.app.log("🛡️ Solicitando criação de ponto de restauração ao Windows...", "info")
        threading.Thread(target=self._create_rp_thread, daemon=True).start()

    def _create_rp_thread(self):
        cmd = "Checkpoint-Computer -Description 'FluxOS_Manual_Backup' -RestorePointType 'MODIFY_SETTINGS'"
        utils.run_cmd(cmd)
        self.app.log("✅ Ponto de restauração 'FluxOS_Manual_Backup' criado com sucesso!", "success")
        self.app.after(0, self.load_points)

    def restore_to(self, sequence_number):
        from tkinter import messagebox
        if messagebox.askyesno("Confirmar Restauração", f"Deseja realmente restaurar o sistema para o ponto #{sequence_number}?\n\n⚠️ O Windows será REINICIADO e todas as alterações feitas após esse ponto serão perdidas."):
            self.app.log(f"⚠️ Iniciando restauração crítica para o ponto #{sequence_number}...", "warning")
            # Comando de restauração requer reinicialização e não pode ser feito de forma totalmente silenciosa sem riscos
            cmd = f"Restore-Computer -RestorePoint {sequence_number} -Confirm:$false"
            threading.Thread(target=lambda: utils.run_cmd(cmd), daemon=True).start()
            self.app.log("🚀 Comando enviado. Aguarde o Windows processar a reinicialização.", "success")

    def run_deep_security_fix(self):
        from tkinter import messagebox
        if messagebox.askyesno("Confirmar Reparo Crítico", "Deseja realizar o Reparo Profundo de Segurança?\n\nIsso removerá bloqueios de 'Administrador de TI' e restaurará o Windows Defender aos padrões de fábrica.\n\n⚠️ O PC poderá ficar lento por alguns segundos durante o reparo."):
            self.app.log("☢️ Iniciando protocolo de Reparo Profundo de Segurança...", "warning")
            threading.Thread(target=lambda: utils.deep_security_repair(self.app.log), daemon=True).start()
