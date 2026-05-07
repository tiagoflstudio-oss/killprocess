import os

with open("gui.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "def draw_radar_chart(self):" in line:
        new_lines.append(line)
        new_lines.append('        cx, cy = 100, 100\n')
        new_lines.append('        r = 70\n')
        new_lines.append('        self.radar_canvas.delete("all")\n')
        new_lines.append('        for i in range(1, 6):\n')
        new_lines.append('            r_ring = (r / 5) * i\n')
        new_lines.append('            self.radar_canvas.create_oval(cx-r_ring, cy-r_ring, cx+r_ring, cy+r_ring, outline="#1E2631", width=1)\n')
        new_lines.append('        import psutil\n')
        new_lines.append('        mem = psutil.virtual_memory()\n')
        new_lines.append('        v1 = 0.3 + (mem.percent / 100.0) * 0.6\n')
        new_lines.append('        v2 = 0.9 if self.autoboost_enabled else 0.5\n')
        new_lines.append('        v3 = 0.95 if hasattr(self, "god_mode_active") and self.god_mode_active else 0.6\n')
        new_lines.append('        v4 = 0.85 if self.shell_explorer_closed else 0.45\n')
        new_lines.append('        v5 = 0.9 if self.autoboost_enabled else 0.7\n')
        new_lines.append('        vals = [v1, v2, v3, v4, v5]\n')
        new_lines.append('        poly_points = []\n')
        new_lines.append('        import math\n')
        new_lines.append('        for i, v in enumerate(vals):\n')
        new_lines.append('            angle = i * (2 * math.pi / 5) - math.pi / 2\n')
        new_lines.append('            x = cx + v * r * math.cos(angle)\n')
        new_lines.append('            y = cy + v * r * math.sin(angle)\n')
        new_lines.append('            poly_points.append(x)\n')
        new_lines.append('            poly_points.append(y)\n')
        new_lines.append('        if len(poly_points) >= 6:\n')
        new_lines.append('            self.radar_canvas.create_polygon(poly_points, fill="#00FF66", outline="#00FFFF", width=2, stipple="gray25")\n')
        new_lines.append('            self.radar_canvas.create_polygon(poly_points, fill="", outline="#00FFFF", width=1.5)\n')
        
        # Skip old implementation until toggle_dry_run
        skip = True
        continue
    
    if skip:
        if "def toggle_dry_run(self):" in line:
            skip = False
        else:
            continue
            
    new_lines.append(line)

with open("gui.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
