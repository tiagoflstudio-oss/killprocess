import customtkinter as ctk
import psutil
import subprocess
import threading
from styles import C, get_fonts
import utils

class ScanTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.fonts = get_fonts()
        
        self._build_header()
        self._build_controls()
        self._build_filter()
        self._build_table_header()
        self._build_scroll_area()
        
        self.scanned_checkboxes = {}
        self.scanned_frames = {}

    def _build_header(self):
        scan_lbl = ctk.CTkLabel(self, text="Escaneamento Avançado de Processos", font=self.fonts["title"], text_color="#F8FAFC")
        scan_lbl.pack(anchor="w", pady=(5, 2))

        scan_sub = ctk.CTkLabel(self, text="Visualize todos os processos do sistema operacional e escolha quais encerrar com segurança.", font=self.fonts["label"], text_color="#94A3B8")
        scan_sub.pack(anchor="w", pady=(0, 10))

    def _build_controls(self):
        ctrl_frame = ctk.CTkFrame(self, fg_color="transparent")
        ctrl_frame.pack(fill="x", pady=(5, 10))

        self.scan_run_btn = ctk.CTkButton(
            ctrl_frame, text="🔍 ESCANEAR TUDO EM TEMPO REAL", fg_color="#10B981", hover_color="#059669",
            font=self.fonts["tab_btn"], height=46, corner_radius=12, text_color="#0D0F12",
            command=self.run_process_scan
        )
        self.scan_run_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.kill_selected_btn = ctk.CTkButton(
            ctrl_frame, text="⚡ ENCERRAR PROCESSOS SELECIONADOS", fg_color="#1F2937", hover_color="#10B981", border_width=1, border_color="#1E2B2A",
            font=self.fonts["tab_btn"], height=46, corner_radius=12,
            command=self.kill_scanned_processes
        )
        self.kill_selected_btn.pack(side="right", fill="x", expand=True, padx=(10, 0))

    def _build_filter(self):
        filter_frame = ctk.CTkFrame(self, fg_color="#11161A", border_width=1, border_color="#1E2B2A", corner_radius=12)
        filter_frame.pack(fill="x", pady=(5, 10))

        f_lbl = ctk.CTkLabel(filter_frame, text="🔍 FILTRAR PROCESSOS:", font=self.fonts["small_bold"], text_color="#10B981")
        f_lbl.pack(side="left", padx=(15, 10), pady=12)

        self.scan_filter_entry = ctk.CTkEntry(
            filter_frame, fg_color="#0D0F12", border_color="#1E2B2A", text_color="#E2E8F0", 
            placeholder_text="Ex: chrome, steam, edge...", height=36, corner_radius=8
        )
        self.scan_filter_entry.pack(side="left", fill="x", expand=True, padx=(0, 15), pady=12)
        self.scan_filter_entry.bind("<KeyRelease>", lambda e: self.filter_scan_list())

        # Select All / Select Safe
        sel_frame = ctk.CTkFrame(self, fg_color="transparent")
        sel_frame.pack(fill="x", pady=(0, 5))

        ctk.CTkButton(sel_frame, text="✅ Selecionar Todos", fg_color="#11161A", hover_color="#10B981", border_width=1, border_color="#1E2B2A",
                      font=self.fonts["small_bold"], height=32, corner_radius=8, command=self.select_all_scanned).pack(side="left", padx=5)
        ctk.CTkButton(sel_frame, text="🛡️ Selecionar Sugeridos", fg_color="#11161A", hover_color="#3B82F6", border_width=1, border_color="#1E2B2A",
                      font=self.fonts["small_bold"], height=32, corner_radius=8, command=self.select_safe_scanned).pack(side="left", padx=5)
        ctk.CTkButton(sel_frame, text="❌ Desmarcar Tudo", fg_color="#11161A", hover_color="#EF4444", border_width=1, border_color="#1E2B2A",
                      font=self.fonts["small_bold"], height=32, corner_radius=8, command=self.deselect_all_scanned).pack(side="left", padx=5)

        self.scan_selection_lbl = ctk.CTkLabel(sel_frame, text="Nenhum processo listado", font=self.fonts["small_bold"], text_color="#94A3B8")
        self.scan_selection_lbl.pack(side="right", padx=15)

    def _build_table_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="#0D0F12", height=30, corner_radius=6)
        header_frame.pack(fill="x", padx=5, pady=(5, 0))
        header_frame.pack_propagate(False)

        headers = [("EXECUTÁVEL", 240), ("MEMÓRIA", 140), ("DESCRIÇÃO", 240), ("RECOMENDAÇÃO", 220)]
        for i, (text, width) in enumerate(headers):
            lbl = ctk.CTkLabel(header_frame, text=text, font=self.fonts["small_bold"], text_color=C["cyan"])
            lbl.grid(row=0, column=i, padx=25, sticky="w")
            header_frame.grid_columnconfigure(i, weight=1, minsize=width)

    def _build_scroll_area(self):
        self.scan_scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#080B0F", border_width=1, border_color="#1E2B2A", corner_radius=0)
        self.scan_scroll_frame.pack(fill="both", expand=True, padx=5, pady=(0, 10))

    def run_process_scan(self):
        self.app.log("\n🔍 Iniciando Escaneamento de Processos...", "info")
        
        for widget in self.scan_scroll_frame.winfo_children():
            widget.destroy()
            
        self.scanned_checkboxes = {}
        self.scanned_frames = {}

        def scan_logic():
            active_p = {}
            for proc in psutil.process_iter(['name', 'memory_info']):
                try:
                    p_info = proc.info
                    name = p_info['name'].lower()
                    mem = p_info['memory_info'].rss / (1024 * 1024)
                    if name in active_p:
                        active_p[name]['instances'] += 1
                        active_p[name]['mem_val'] += mem
                    else:
                        active_p[name] = {'instances': 1, 'mem_val': mem}
                except: continue

            # Formata memória
            for k in active_p:
                active_p[k]['mem'] = f"{active_p[k]['mem_val']:.1f} MB"

            self.app.after(0, lambda: self._render_scan_results(active_p))

        threading.Thread(target=scan_logic, daemon=True).start()

    def _render_scan_results(self, active_p):
        CRITICAL_SYSTEM_PROCESSES = {"system", "idle", "smss.exe", "wininit.exe", "winlogon.exe", "services.exe", "lsass.exe", "csrss.exe", "svchost.exe", "explorer.exe", "taskmgr.exe"}
        known_bloatware = {"chrome.exe", "msedge.exe", "discord.exe", "spotify.exe", "teams.exe", "skype.exe", "anydesk.exe", "teamviewer.exe", "steam.exe", "epicgameslauncher.exe", "onedrive.exe", "whatsapp.exe", "telegram.exe", "officeclicktorun.exe", "cortana.exe"}
        
        PROCESS_DATA = {
            "lsass.exe": {"desc": "Serviço de Segurança Local", "effect": "Crítico. Não fechar (reinicia o PC)"},
            "csrss.exe": {"desc": "Cliente/Servidor de Execução", "effect": "Crítico. Não fechar (tela azul)"},
            "services.exe": {"desc": "Gerenciador de Serviços", "effect": "Crítico. Não fechar (trava o Windows)"},
            "taskhostw.exe": {"desc": "Host de Tarefas do Windows", "effect": "Crítico. Não recomendável fechar"},
            "spoolsv.exe": {"desc": "Serviço de Impressão do Windows", "effect": "Geralmente seguro fechar se não estiver imprimindo"},
            "ctfmon.exe": {"desc": "Suporte a Idiomas e Teclado", "effect": "Crítico. Não recomendável fechar"}
        }

        for p_name, data in sorted(active_p.items()):
            p_frame = ctk.CTkFrame(self.scan_scroll_frame, fg_color="transparent")
            p_frame.pack(fill="x", padx=15, pady=2)

            p_frame.grid_columnconfigure(0, weight=3, minsize=240)
            p_frame.grid_columnconfigure(1, weight=2, minsize=140)
            p_frame.grid_columnconfigure(2, weight=3, minsize=240)
            p_frame.grid_columnconfigure(3, weight=3, minsize=220)

            is_critical = p_name in CRITICAL_SYSTEM_PROCESSES
            is_suggested = p_name in known_bloatware

            cb = ctk.CTkCheckBox(p_frame, text=p_name, font=self.fonts["label"], fg_color="#10B981", hover_color="#059669", command=self.update_selection_counter)

            meta = PROCESS_DATA.get(p_name, {})
            if is_critical:
                cb.configure(state="disabled")
                desc_text = meta.get("desc", "Processo essencial do sistema")
                effect_text = meta.get("effect", "Não recomendável fechar")
                text_color = "#94A3B8"
            elif is_suggested:
                cb.select()
                desc_text = meta.get("desc", "Software de terceiro em segundo plano")
                effect_text = meta.get("effect", "Otimização Gamer Recomendada")
                text_color = "#10B981"
            else:
                desc_text = meta.get("desc", "Aplicativo / Serviço de Segundo Plano")
                effect_text = meta.get("effect", "Geralmente seguro fechar")
                text_color = "#38BDF8"

            cb.grid(row=0, column=0, padx=10, pady=4, sticky="w")
            ctk.CTkLabel(p_frame, text=f"{data['instances']} inst. | {data['mem']}", font=self.fonts["label"], text_color="#E2E8F0").grid(row=0, column=1, padx=10, pady=4, sticky="w")
            ctk.CTkLabel(p_frame, text=desc_text, font=self.fonts["label_small"], text_color="#94A3B8").grid(row=0, column=2, padx=10, pady=4, sticky="w")
            ctk.CTkLabel(p_frame, text=effect_text, font=self.fonts["label_italic"], text_color=text_color).grid(row=0, column=3, padx=10, pady=4, sticky="w")

            self.scanned_checkboxes[p_name] = cb
            self.scanned_frames[p_name] = p_frame

        self.scan_filter_entry.delete(0, "end")
        self.update_selection_counter()
        self.app.log("✅ Escaneamento de processos concluído.", "success")

    def update_selection_counter(self):
        total = len(self.scanned_checkboxes)
        marked = sum(1 for cb in self.scanned_checkboxes.values() if cb.get())
        if total == 0:
            self.scan_selection_lbl.configure(text="Nenhum processo listado", text_color="#94A3B8")
        else:
            self.scan_selection_lbl.configure(text=f"📌 Marcados: {marked} de {total}", text_color="#10B981")

    def select_all_scanned(self):
        for p_name, cb in self.scanned_checkboxes.items():
            if cb.cget("state") != "disabled": cb.select()
        self.update_selection_counter()

    def select_safe_scanned(self):
        known_bloatware = {"chrome.exe", "msedge.exe", "discord.exe", "spotify.exe", "teams.exe", "skype.exe", "anydesk.exe", "teamviewer.exe", "steam.exe", "epicgameslauncher.exe", "onedrive.exe", "whatsapp.exe", "telegram.exe", "officeclicktorun.exe", "cortana.exe"}
        for p_name, cb in self.scanned_checkboxes.items():
            if p_name in known_bloatware and cb.cget("state") != "disabled": cb.select()
            elif cb.cget("state") != "disabled": cb.deselect()
        self.update_selection_counter()

    def deselect_all_scanned(self):
        for p_name, cb in self.scanned_checkboxes.items():
            if cb.cget("state") != "disabled": cb.deselect()
        self.update_selection_counter()

    def filter_scan_list(self):
        query = self.scan_filter_entry.get().strip().lower()
        for p_name, frame in self.scanned_frames.items():
            if query in p_name: frame.pack(fill="x", padx=15, pady=3)
            else: frame.pack_forget()

    def kill_scanned_processes(self):
        to_kill = []
        for p_file, cb in self.scanned_checkboxes.items():
            if cb.get() and cb.cget("state") != "disabled": to_kill.append(p_file)

        if not to_kill:
            self.app.log("⚠️ Nenhum processo selecionado para encerramento.", "warning")
            return

        self.app.log(f"\n⚡ Iniciando encerramento de {len(to_kill)} processos...", "info")

        for p in to_kill:
            if utils.DRY_RUN: self.app.log(f"[SIMULAÇÃO] Encerrando {p} via Scan.", "info")
            else:
                try:
                    subprocess.run(["taskkill", "/F", "/IM", p], capture_output=True, text=True)
                    self.app.log(f"✔️ {p} encerrado com sucesso!", "success")
                except Exception as e:
                    self.app.log(f"❌ Falha ao encerrar {p}: {e}", "error")

        self.run_process_scan()
