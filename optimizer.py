import os
import sys
import io
import subprocess
import time

# =====================================================================
# 🚀 Killprocess - Core Engine & Advanced Optimizer (Python 3.12)
# =====================================================================

# Variável de Controle do Modo Simulação (Dry Run)
DRY_RUN = False

def is_admin():
    """Verifica se o script está rodando como administrador."""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

# Flag para execução silenciosa
CREATE_NO_WINDOW = 0x08000000

def run_cmd(cmd):
    """Executa um comando no Windows de forma segura."""
    if DRY_RUN:
        return f"[SIMULAÇÃO]: Executando comando -> {cmd}"
    try:
        # Execução silenciosa via PowerShell
        result = subprocess.run(
            ["powershell", "-Command", cmd], 
            capture_output=True, 
            text=True,
            creationflags=CREATE_NO_WINDOW
        )
        return result.stdout.strip()
    except Exception as e:
        return str(e)

# =====================================================================
# 🛡️ Sistema de Backup, Segurança e Ponto de Restauração
# =====================================================================

def create_restore_point():
    """Fase 2: Cria um ponto de restauração do Windows para máxima segurança."""
    print("\n🛡️ Criando Ponto de Restauração do Windows...")
    if DRY_RUN:
        print("[SIMULAÇÃO] Ponto de Restauração criado com sucesso!")
        return
    # Habilita restauração de sistema caso esteja desativada e cria o ponto
    cmd = (
        "Enable-ComputerRestore -Drive 'C:\\'; "
        "Checkpoint-Computer -Description 'Killprocess_GameMode_Backup' "
        "-RestorePointType 'MODIFY_SETTINGS'"
    )
    result = run_cmd(cmd)
    print("✅ Ponto de Restauração 'Killprocess_GameMode_Backup' criado com sucesso!")

def backup_active_services():
    """Fase 2: Exporta a lista de todos os serviços que estavam ativos."""
    print("📋 Fazendo backup da lista de serviços ativos...")
    if DRY_RUN:
        print("[SIMULAÇÃO] Lista de serviços ativos salva em 'active_services_backup.txt'.")
        return
    
    # Exporta a lista via PowerShell
    cmd = "Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object -ExpandProperty Name"
    running_services = run_cmd(cmd)
    
    if running_services:
        with open("active_services_backup.txt", "w", encoding="utf-8") as f:
            f.write(running_services)
        print("✅ Backup salvo em 'active_services_backup.txt'.")
    else:
        print("⚠️ Atenção: Nenhum serviço ativo encontrado para backup.")

# =====================================================================
# ⚙️ Gerenciamento de Processos e Serviços
# =====================================================================

def stop_process(process_name):
    """Encerra um processo pelo nome."""
    print(f"🛑 Encerrando processo: {process_name}...")
    if DRY_RUN:
        print(f"[SIMULAÇÃO]: Processo {process_name} encerrado.")
    else:
        run_cmd(f"Stop-Process -Name '{process_name}' -Force")

def stop_service(service_name):
    """Encerra e desativa um serviço do Windows."""
    print(f"🛑 Desativando serviço: {service_name}...")
    if DRY_RUN:
        print(f"[SIMULAÇÃO]: Serviço {service_name} parado e desativado.")
    else:
        run_cmd(f"Stop-Service -Name '{service_name}' -Force")
        run_cmd(f"Set-Service -Name '{service_name}' -StartupType Disabled")

def start_service(service_name):
    """Ativa e inicia um serviço do Windows."""
    print(f"🟢 Reativando serviço: {service_name}...")
    if DRY_RUN:
        print(f"[SIMULAÇÃO]: Serviço {service_name} ativado e iniciado.")
    else:
        run_cmd(f"Set-Service -Name '{service_name}' -StartupType Automatic")
        run_cmd(f"Start-Service -Name '{service_name}'")

# =====================================================================
# 🎚️ Níveis de Otimização
# =====================================================================

def optimize_level_1():
    print("\n--- 🟢 Executando Otimização Nível 1: Limpeza Segura ---")
    apps_to_kill = ["chrome", "msedge", "onedrive", "teams", "discord", "spotify"]
    for app in apps_to_kill:
        stop_process(app)
    run_cmd("[System.GC]::Collect()")
    print("✅ Nível 1 concluído com sucesso!")

def optimize_level_2():
    print("\n--- 🟡 Executando Otimização Nível 2: Gamer (Standard) ---")
    optimize_level_1()
    stop_service("Spooler")       # Impressora
    stop_service("WSearch")       # Windows Search
    stop_service("SysMain")       # Superfetch / SysMain
    print("✅ Nível 2 concluído com sucesso!")

def optimize_level_3():
    print("\n--- 🟠 Executando Otimização Nível 3: Gamer Avançado (Hardcore) ---")
    optimize_level_2()
    stop_service("DiagTrack")           # Telemetria
    stop_service("dmwappushservice")    # Telemetria push
    stop_service("wuauserv")            # Windows Update
    stop_service("XblAuthManager")
    stop_service("XblGameSave")
    print("✅ Nível 3 concluído com sucesso!")

def optimize_level_4():
    print("\n--- 🔴 Executando Otimização Nível 4: Gamer Extremo (Ultra Gaming) ---")
    optimize_level_3()
    stop_service("Themes")
    run_cmd("powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c") # Alto Desempenho
    print("✅ Nível 4 concluído com sucesso!")

def optimize_level_5():
    print("\n--- 🔥 Executando Otimização Nível 5: MODO GAMER PRO (BAREBONE) ---")
    # Executa a criação do backup e ponto de restauração para segurança máxima
    create_restore_point()
    backup_active_services()
    
    optimize_level_4()
    
    print("⚠️ ATENÇÃO: Encerrando o Explorer.exe. A barra de tarefas sumirá temporariamente.")
    stop_process("explorer")
    
    stop_service("bthserv")  # Bluetooth
    
def optimize_level_6():
    print("\n--- 🔒 Executando Otimização Nível 6: Segurança & Criptografia ---")
    optimize_level_5()
    stop_service("VaultSvc")
    stop_service("SstpSvc")
    stop_service("SCardSvr")
    stop_service("RemoteRegistry")
    print("✅ Nível 6 concluído com sucesso!")

def optimize_level_7():
    print("\n--- 👑 Executando Otimização Nível 7: MODO DEUS (God Mode) ---")
    optimize_level_6()
    services_god = [
        "PushToInstall", "WMPNetworkSvc", "ClipSVC", "AppPredictionSvc",
        "AppXSvc", "LicenseManager", "tzautoupdate", "WalletService",
        "WpnService", "AxInstSV", "BITS", "CertPropSvc", "defragsvc"
    ]
    for s in services_god:
        stop_service(s)
    print("✅ MODO DEUS ATIVADO COM SUCESSO!")

def restore_all():
    print("\n--- 🔄 Restaurando Padrões do Windows ---")
    services_to_restore = [
        "Spooler", "WSearch", "SysMain", "DiagTrack",
        "dmwappushservice", "wuauserv", "Themes", "bthserv",
        "VaultSvc", "SstpSvc", "SCardSvr", "RemoteRegistry",
        "PushToInstall", "WMPNetworkSvc", "ClipSVC", "AppPredictionSvc",
        "AppXSvc", "LicenseManager", "tzautoupdate", "WalletService",
        "WpnService", "AxInstSV", "BITS", "CertPropSvc", "defragsvc"
    ]
    for service in services_to_restore:
        start_service(service)
        
    print("🟢 Reiniciando Explorer.exe...")
    if DRY_RUN:
        print("[SIMULAÇÃO] Explorer reiniciado.")
    else:
        run_cmd("explorer.exe")
    print("\n✅ Todos os padrões do Windows foram restaurados!")

def clean_temp_files():
    """Limpa arquivos temporários do sistema e do usuário."""
    print("\n🧹 Iniciando Limpeza de Arquivos Temporários...")
    if DRY_RUN:
        print("[SIMULAÇÃO] Arquivos temporários removidos.")
        return
    
    commands = [
        "Remove-Item -Path $env:TEMP\\* -Recurse -Force -ErrorAction SilentlyContinue",
        "Remove-Item -Path 'C:\\Windows\\Temp\\*' -Recurse -Force -ErrorAction SilentlyContinue",
        "Remove-Item -Path 'C:\\Windows\\Prefetch\\*' -Recurse -Force -ErrorAction SilentlyContinue"
    ]
    for cmd in commands:
        run_cmd(cmd)
    print("✅ Limpeza de arquivos temporários concluída!")

def flush_dns():
    """Limpa o cache de DNS e redefine configurações de rede básicas."""
    print("\n🌐 Otimizando Rede (DNS Flush)...")
    if DRY_RUN:
        print("[SIMULAÇÃO] Cache de DNS limpo e rede redefinida.")
        return
    
    run_cmd("ipconfig /flushdns")
    run_cmd("netsh winsock reset")
    print("✅ Cache de DNS limpo e Winsock redefinido!")

def set_ultimate_performance():
    """Ativa o plano de energia de Desempenho Máximo (se disponível) ou Alto Desempenho."""
    print("\n⚡ Otimizando Plano de Energia...")
    if DRY_RUN:
        print("[SIMULAÇÃO] Plano de Energia definido para Desempenho Máximo.")
        return
    
    # Tenta ativar o esquema "Desempenho Máximo" (Ultimate Performance)
    # Se não existir, ele cria.
    cmd = "powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61"
    run_cmd(cmd)
    # Define como ativo
    run_cmd("powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61")
    print("✅ Plano de Energia definido para DESEMPENHO MÁXIMO!")

def optimize_registry():
    """Aplica tweaks de registro para performance gamer (Registry Gaming)."""
    print("\n🛠️ Aplicando Otimizações de Registro (Gaming Registry)...")
    if DRY_RUN:
        print("[SIMULAÇÃO] Registro do Windows otimizado para jogos.")
        return
    
    # Exemplo de tweaks: Desativar Game DVR, Otimizar resposta de rede, etc.
    commands = [
        # Desativa Game DVR (ajuda no FPS)
        "Set-ItemProperty -Path 'HKCU:\\System\\GameConfigStore' -Name 'GameDVR_Enabled' -Value 0",
        "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR' -Name 'AllowGameDVR' -Value 0",
        # Otimização de Processamento (ajusta prioridade de GPU para games)
        "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games' -Name 'GPU Priority' -Value 8",
        "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games' -Name 'Priority' -Value 6",
        "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games' -Name 'Scheduling Category' -Value 'High'"
    ]
    for cmd in commands:
        run_cmd(cmd)
    print("✅ Registro otimizado para Máxima Performance!")

def optimize_tcp():
    """Aplica otimizações de rede TCP (TCP Otimizado)."""
    print("\n🌐 Aplicando Otimizações de Rede (TCP Autotuning)...")
    if DRY_RUN:
        print("[SIMULAÇÃO] Configurações de rede TCP otimizadas.")
        return
    
    commands = [
        "netsh int tcp set global autotuninglevel=normal",
        "netsh int tcp set global ecncapability=disabled",
        "netsh int tcp set global rss=enabled",
        "netsh int tcp set global chimney=enabled",
        "netsh int tcp set global dca=enabled",
        "netsh int tcp set global netdma=enabled",
        "netsh int tcp set global congestionprovider=ctcp",
        "netsh int tcp set global timestamps=disabled"
    ]
    for cmd in commands:
        run_cmd(cmd)
    print("✅ Rede TCP otimizada para menor latência!")

# =====================================================================
# 💻 Interface via Terminal
# =====================================================================

def main():
    global DRY_RUN
    
    # Configura o terminal para UTF-8 para evitar erros com emojis
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    if not is_admin():
        print("❌ ERRO: Este script precisa ser executado como ADMINISTRADOR.")
        print("Abra o terminal (PowerShell ou CMD) como Administrador e execute novamente.")
        return

    while True:
        mode_text = "[Simulação / Dry-Run]" if DRY_RUN else "[Modo Real]"
        print("\n" + "="*50)
        print(f" 🚀 KILLPROCESS - SELETOR DE NÍVEIS {mode_text}")
        print("="*50)
        print("1 - 🟢 Nível 1: Limpeza Segura (Apps de Usuário)")
        print("2 - 🟡 Nível 2: Gamer Standard (Serviços não críticos)")
        print("3 - 🟠 Nível 3: Gamer Hardcore (Telemetria & Updates)")
        print("4 - 🔴 Nível 4: Gamer Extremo (Plano de Energia + Temas)")
        print("5 - 🔥 Nível 5: MODO GAMER PRO (Fecha Explorer)")
        print("6 - 🔒 Nível 6: Segurança & Criptografia")
        print("7 - 👑 Nível 7: MODO DEUS (God Mode Supremo)")
        print("8 - 🛡️  Criar Ponto de Restauração & Backup dos Serviços")
        print("9 - 🔄 Restaurar todos os padrões do Windows")
        print("S - 🧪 Alternar Modo Simulação / Modo Real")
        print("0 - 🚪 Sair")
        print("="*50)
        
        opcao = input("Selecione uma opção: ").strip().upper()
        
        if opcao == "1":
            optimize_level_1()
        elif opcao == "2":
            optimize_level_2()
        elif opcao == "3":
            optimize_level_3()
        elif opcao == "4":
            optimize_level_4()
        elif opcao == "5":
            optimize_level_5()
        elif opcao == "6":
            optimize_level_6()
        elif opcao == "7":
            optimize_level_7()
        elif opcao == "8":
            create_restore_point()
            backup_active_services()
        elif opcao == "9":
            restore_all()
        elif opcao == "S":
            DRY_RUN = not DRY_RUN
            status = "ATIVADO" if DRY_RUN else "DESATIVADO"
            print(f"Modo Simulação (Dry Run) {status}!")
        elif opcao == "0":
            print("Saindo do Killprocess...")
            break
        else:
            print("Opção inválida!")
        
        time.sleep(1)

if __name__ == "__main__":
    main()
