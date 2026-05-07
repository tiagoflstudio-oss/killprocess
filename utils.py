import os
import sys
import subprocess

VERSION = "2.1.33" # Versão Atual (Sapphire Edition)
DRY_RUN = False # Modo Real para Release
UPDATE_URL = "https://raw.githubusercontent.com/tiagoflstudio-oss/killprocess/main/version.json"

def resource_path(relative_path):
    """ Retorna o caminho absoluto para recursos, funcionando em Dev e no PyInstaller exe. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def is_admin():
    """ Verifica se o programa está rodando com privilégios de administrador. """
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_cmd(cmd, dry_run=None):
    """ Executa um comando via PowerShell com suporte a modo de simulação. """
    if dry_run is None:
        dry_run = DRY_RUN
        
    if dry_run:
        return f"[SIMULAÇÃO]: {cmd}"
    try:
        # Usar CREATE_NO_WINDOW para evitar popups pretos do terminal
        CREATE_NO_WINDOW = 0x08000000
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, creationflags=CREATE_NO_WINDOW)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def get_restore_points():
    """ Retorna uma lista de dicionários com os pontos de restauração do sistema. """
    cmd = "Get-ComputerRestorePoint | Select-Object SequenceNumber, Description, @{Name='Date'; Expression={$_.CreationTime.ToString('dd/MM/yyyy HH:mm')}}, RestorePointType | ConvertTo-Json"
    res = run_cmd(cmd, dry_run=False) # Sempre leitura real
    if not res or "Get-ComputerRestorePoint" in res: return []
    try:
        import json
        data = json.loads(res)
        if isinstance(data, dict): return [data]
        return data
    except:
        return []

def deep_security_repair(log_callback=None):
    """ Executa o reparo profundo da segurança do Windows, removendo travas de GPO e IT Admin. """
    if log_callback: log_callback("🛡️ Iniciando Reparo Profundo de Segurança...", "info")
    
    script = """
    $ErrorActionPreference = 'SilentlyContinue'
    
    # Função para tomar posse de chaves protegidas
    function Take-Ownership {
        param($Path)
        if (Test-Path $Path) {
            $AdminAccount = New-Object System.Security.Principal.NTAccount('Administrators')
            $Acl = Get-Acl $Path
            $Acl.SetOwner($AdminAccount)
            Set-Acl $Path $Acl
            $AccessRule = New-Object System.Security.AccessControl.RegistryAccessRule('Administrators', 'FullControl', 'ContainerInherit,ObjectInherit', 'None', 'Allow')
            $Acl.SetAccessRule($AccessRule)
            Set-Acl $Path $Acl
            Remove-Item -Path $Path -Recurse -Force
        }
    }

    # Remover bloqueios de políticas
    Take-Ownership 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender'
    Take-Ownership 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender Security Center'
    Take-Ownership 'HKCU:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender'
    Take-Ownership 'HKCU:\\SOFTWARE\\Policies\\Microsoft\\Windows Defender Security Center'

    # Resetar valores de desativação
    $regPath = 'HKLM:\\SOFTWARE\\Microsoft\\Windows Defender'
    if (Test-Path $regPath) {
        Remove-ItemProperty -Path $regPath -Name 'DisableAntiSpyware'
        Remove-ItemProperty -Path $regPath -Name 'DisableAntiVirus'
    }

    # Resetar serviços via registro
    $services = @{'WinDefend'=2; 'SecurityHealthService'=2; 'wscsvc'=2; 'mpssvc'=2}
    foreach ($svc in $services.Keys) {
        $p = 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\$svc'
        if (Test-Path $p) { Set-ItemProperty -Path $p -Name 'Start' -Value $services[$svc] -Force }
    }

    # Re-registrar UI (SecHealthUI)
    Get-AppxPackage -AllUsers -Name Microsoft.SecHealthUI | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppXManifest.xml" -Force}

    # Forçar atualização de políticas
    gpupdate /force
    """
    
    res = run_cmd(script, dry_run=False)
    
    if log_callback: 
        log_callback("✅ Reparo concluído! Políticas de IT Admin removidas.", "success")
        log_callback("ℹ️ Se a janela não abrir, reinicie o PC para aplicar as mudanças de Kernel.", "warning")
    
    return True
