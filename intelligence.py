import psutil
import os

class ApexBrain:
    def __init__(self):
        self.heavy_processes = [
            "chrome", "msedge", "firefox", "discord", "spotify", "teams", "slack", 
            "steam", "epicgameslauncher", "origingames", "uplay"
        ]

    def analyze_system(self):
        """
        Analisa o sistema em busca de gargalos reais e retorna uma recomendação tática.
        """
        analysis = {
            "ram_usage": psutil.virtual_memory().percent,
            "cpu_usage": psutil.cpu_percent(interval=1.0),
            "disk_usage": psutil.disk_usage('C:').percent,
            "heavy_apps_found": [],
            "telemetry_active": False,
            "recommendation": "",
            "action_target": "",
            "details": ""
        }

        # 1. Scanner de Processos Pesados e Telemetria
        telemetry_procs = ["compat-tel-runner", "telemetry", "diagtrack", "werfault"]
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name'].lower().replace(".exe", "")
                if name in self.heavy_processes:
                    if name not in analysis["heavy_apps_found"]:
                        analysis["heavy_apps_found"].append(name)
                if any(t in name for t in telemetry_procs):
                    analysis["telemetry_active"] = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # 2. Motor de Decisão Tática (Heurísticas Reais)
        
        # PRIORIDADE 1: RAM (Gargalo de Curto Prazo)
        if analysis["ram_usage"] > 85:
            analysis["recommendation"] = "CRÍTICO: SATURAÇÃO DE RAM"
            analysis["details"] = f"Detectamos que {analysis['ram_usage']}% da sua memória está comprometida. Recomendamos o MODO DEUS para encerrar processos não essenciais imediatamente."
            analysis["action_target"] = "GOD"
            
        # PRIORIDADE 2: Processos de Terceiros (Bloatwares)
        elif len(analysis["heavy_apps_found"]) >= 2:
            apps = ", ".join(analysis["heavy_apps_found"][:2]).upper()
            analysis["recommendation"] = "OTIMIZAÇÃO DE APLICATIVOS"
            analysis["details"] = f"Os processos {apps} estão ativos e consumindo recursos de background. O NÍVEL 1 é a melhor escolha agora."
            analysis["action_target"] = "N1"

        # PRIORIDADE 3: Telemetria e CPU
        elif analysis["telemetry_active"] or analysis["cpu_usage"] > 40:
            analysis["recommendation"] = "REDUÇÃO DE LATÊNCIA (CPU)"
            analysis["details"] = "Serviços de telemetria ou alta carga de CPU detectados. O NÍVEL 3 (TELEMETRIA) vai estabilizar seu processamento."
            analysis["action_target"] = "N3"

        # PRIORIDADE 4: Disco e Manutenção
        elif analysis["disk_usage"] > 90:
            analysis["recommendation"] = "MANUTENÇÃO DE ARQUIVOS"
            analysis["details"] = "Seu disco 'C:' está quase cheio, o que causa lentidão. Sugerimos usar a LIMPEZA DE DISCO."
            analysis["action_target"] = "CLEAN"

        # PADRÃO: Estabilidade
        else:
            analysis["recommendation"] = "SISTEMA OTIMIZADO"
            analysis["details"] = "Seu sistema está operando em níveis estáveis. Recomendamos o NÍVEL 2 para manter a performance de serviços."
            analysis["action_target"] = "N2"

        return analysis

# Singleton para uso no GUI
brain = ApexBrain()
