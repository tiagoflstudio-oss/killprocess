import customtkinter as ctk
from styles import C, get_fonts
from services import SERVICES_MAP

class ManagementTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.fonts = get_fonts()
        
        self._build_header()
        self._build_content()

    def _build_header(self):
        # Cabeçalho
        manage_lbl = ctk.CTkLabel(self, text="Processos & Serviços", font=self.fonts["title"], text_color="#F8FAFC")
        manage_lbl.pack(anchor="w", pady=(5, 2))

        self.manage_sub = ctk.CTkLabel(
            self, text="Selecione um nível de otimização para ver e ajustar suas opções detalhadamente.", 
            font=self.fonts["label"], text_color="#94A3B8"
        )
        self.manage_sub.pack(anchor="w", pady=(0, 20))

    def _build_content(self):
        self.management_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.management_content_frame.pack(fill="both", expand=True)

        # ---------------------------------------------------------
        # GRID DE CARDS (Níveis de Otimização)
        # ---------------------------------------------------------
        self.levels_grid_frame = ctk.CTkFrame(self.management_content_frame, fg_color="transparent")
        self.levels_grid_frame.pack(fill="both", expand=True)

        self.levels_grid_frame.grid_columnconfigure((0, 1), weight=1)

        level_cards_data = [
            {"id": "Nível 1: Aplicativos & Bloatwares", "title": "🟢 Nível 1", "subtitle": "Apps & Bloatware", "row": 0, "col": 0},
            {"id": "Nível 2: Impressão & Manutenção", "title": "🟡 Nível 2", "subtitle": "Impressão & Servs.", "row": 0, "col": 1},
            {"id": "Nível 3: Telemetria & Rastreamento", "title": "🟠 Nível 3", "subtitle": "Telemetria & Rastr.", "row": 1, "col": 0},
            {"id": "Nível 4: Xbox & Conexões Secundárias", "title": "🔴 Nível 4", "subtitle": "Xbox & Conexões", "row": 1, "col": 1},
            {"id": "Nível 5: Redes & Streaming", "title": "🌐 Nível 5", "subtitle": "Redes & Streaming", "row": 2, "col": 0},
            {"id": "Nível 6: Segurança & Biometria", "title": "🔒 Nível 6", "subtitle": "Segur. & Biometria", "row": 2, "col": 1},
            {"id": "Nível 7: God Mode (Extreme)", "title": "👑 Modo Deus", "subtitle": "God Mode Supremo", "row": 3, "col": 0},
            {"id": "Nível 8: Polish (Serviços Fantasmas)", "title": "✨ Nível 8", "subtitle": "Gaming Polish", "row": 3, "col": 1},
            {"id": "Nível 9: Engine (Núcleo)", "title": "⚙️ Nível 9", "subtitle": "Deep Engine", "row": 4, "col": 0},
            {"id": "Nível 10: NVIDIA GPU Elite", "title": "💎 Nível 10", "subtitle": "NVIDIA GPU Elite", "row": 4, "col": 1}
        ]

        for c in level_cards_data:
            btn_card = ctk.CTkButton(
                self.levels_grid_frame, text=f"{c['title']} - {c['subtitle']}",
                fg_color="#10151B", hover_color="#1E2631", border_width=1, border_color="#1E2631",
                font=self.fonts["section"], height=60, corner_radius=10,
                command=lambda cat=c["id"]: self.show_level_options(cat)
            )
            btn_card.grid(row=c["row"], column=c["col"], padx=4, pady=4, sticky="nsew")

        # ---------------------------------------------------------
        self.level_details_frame = ctk.CTkFrame(self.management_content_frame, fg_color="transparent")
        
        self.back_btn = ctk.CTkButton(
            self.level_details_frame, text="⬅️ Voltar aos Níveis", fg_color="#10151B", hover_color="#1E2631", border_width=1, border_color="#1E2631",
            font=self.fonts["label"], height=32, corner_radius=6, command=self.show_levels_grid
        )
        self.back_btn.pack(anchor="w", pady=(0, 8))

        self.scroll_frame = ctk.CTkScrollableFrame(self.level_details_frame, fg_color="#10151B", border_width=1, border_color="#1E2631", corner_radius=10)
        self.scroll_frame.pack(fill="both", expand=True)

        self.category_frames = {}

        for category, items in SERVICES_MAP.items():
            frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            self.category_frames[category] = frame

            cat_lbl = ctk.CTkLabel(frame, text=category.upper(), font=self.fonts["section"], text_color="#00FFFF")
            cat_lbl.pack(anchor="w", padx=10, pady=(10, 5))

            for item in items:
                row_frame = ctk.CTkFrame(frame, fg_color="transparent")
                row_frame.pack(fill="x", padx=10, pady=2)

                cb = ctk.CTkCheckBox(
                    row_frame, text=f"{item['name']} ({item['id']})", 
                    font=self.fonts["label"], fg_color="#00FFFF", hover_color="#00CCCC"
                )
                if item["checked"]:
                    cb.select()
                cb.pack(side="left", anchor="w")
                self.app.checkboxes[item["id"]] = cb

    def show_level_options(self, category):
        self.levels_grid_frame.pack_forget()
        self.manage_sub.configure(text=f"Personalizando opções detalhadas para: {category}")

        for frame in self.category_frames.values():
            frame.pack_forget()

        self.category_frames[category].pack(fill="both", expand=True)
        self.level_details_frame.pack(fill="both", expand=True)

    def show_levels_grid(self):
        self.level_details_frame.pack_forget()
        self.manage_sub.configure(text="Selecione um nível de otimização para ver e ajustar suas opções detalhadamente.")
        self.levels_grid_frame.pack(fill="both", expand=True)
