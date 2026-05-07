import os

with open("gui.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
in_broken_loop = False
for line in lines:
    if "def refresh_stats_loop(self):" in line:
        new_lines.append(line)
        new_lines.append('        self.after(500, self.blink_real_mode)\n')
        new_lines.append('        self.after(600, self.blink_clear_btn)\n')
        new_lines.append('        while True:\n')
        new_lines.append('            try:\n')
        new_lines.append('                import psutil\n')
        new_lines.append('                mem = psutil.virtual_memory()\n')
        new_lines.append('                ram_pct = mem.percent / 100.0\n')
        new_lines.append('                if hasattr(self, "ram_lbl"): self.ram_lbl.configure(text=f"RAM {mem.used/(1024**3):.1f}GB")\n')
        new_lines.append('                if hasattr(self, "ram_bar"): self.ram_bar.set(ram_pct)\n')
        new_lines.append('                cpu_p = psutil.cpu_percent()\n')
        new_lines.append('                if hasattr(self, "cpu_lbl"): self.cpu_lbl.configure(text=f"CPU {cpu_p:.0f}%")\n')
        new_lines.append('                if hasattr(self, "cpu_bar"): self.cpu_bar.set(cpu_p/100.0)\n')
        new_lines.append('                procs = len(psutil.pids())\n')
        new_lines.append('                if hasattr(self, "proc_lbl"): self.proc_lbl.configure(text=f"PROC {procs}")\n')
        new_lines.append('                if hasattr(self, "proc_bar"): self.proc_bar.set(min(procs/500, 1.0))\n')
        new_lines.append('                self.draw_radar_chart()\n')
        new_lines.append('            except: pass\n')
        new_lines.append('            time.sleep(1.5)\n')
        in_broken_loop = True
        continue
    
    if in_broken_loop:
        if "def start_optimization" in line or "# =" in line:
            in_broken_loop = False
        else:
            continue
            
    new_lines.append(line)

with open("gui.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
