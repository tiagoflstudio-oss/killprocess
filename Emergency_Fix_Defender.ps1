# FLUX OS - ULTRA EMERGENCY RECOVERY SCRIPT (Windows Defender & Security UI)
# IMPORTANTE: Execute como ADMINISTRADOR

$ErrorActionPreference = "SilentlyContinue"

Write-Host "--- [ FLUX OS SAPPHIRE - REPARO DE EMERGÊNCIA ] ---" -ForegroundColor Cyan
Write-Host "Iniciando restauração crítica da segurança do Windows..." -ForegroundColor White

# 1. Matar processos que podem estar travando o serviço
Write-Host "[1/5] Encerrando processos de interface..." -ForegroundColor Yellow
Stop-Process -Name "SecHealthUI" -Force
Stop-Process -Name "SecurityHealthService" -Force

# 2. Remover Bloqueios de Registro e Políticas (GPO)
Write-Host "[2/5] Removendo bloqueios de registro e políticas..." -ForegroundColor Yellow
$regPaths = @(
    "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender",
    "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection",
    "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender\Spynet",
    "HKLM:\SOFTWARE\Microsoft\Windows Defender",
    "HKLM:\SOFTWARE\Microsoft\Windows Defender Security Center"
)

foreach ($path in $regPaths) {
    if (Test-Path $path) {
        Remove-ItemProperty -Path $path -Name "DisableAntiSpyware" -Force
        Remove-ItemProperty -Path $path -Name "DisableAntiVirus" -Force
        Remove-ItemProperty -Path $path -Name "DisableRealtimeMonitoring" -Force
        Remove-Item -Path $path -Recurse -Force
        Write-Host "  -> Limpo: $path" -ForegroundColor Gray
    }
}

# 3. Restaurar Serviços via Registro (Força Bruta no Kernel)
Write-Host "[3/5] Restaurando serviços no Kernel..." -ForegroundColor Yellow
$services = @{
    "WinDefend" = 2;             # Auto
    "WdNisSvc"  = 3;             # Manual
    "Sense"     = 3;             # Manual
    "WdFilter"  = 0;             # Boot
    "WdBoot"    = 0;             # Boot
    "SecurityHealthService" = 2; # Auto (Interface)
    "wscsvc"    = 2;             # Security Center
    "mpssvc"    = 2;             # Firewall
    "AppXSvc"   = 2;             # AppX Deployment (Necessário para a UI)
}

foreach ($svc in $services.Keys) {
    $s_path = "HKLM:\SYSTEM\CurrentControlSet\Services\$svc"
    if (Test-Path $s_path) {
        Set-ItemProperty -Path $s_path -Name "Start" -Value $services[$svc] -Force
    }
}

# 4. Re-registrar a Interface de Segurança do Windows (AppX)
Write-Host "[4/5] Reinstalando Interface de Segurança (AppX)..." -ForegroundColor Yellow
Get-AppxPackage -AllUsers -Name "Microsoft.SecHealthUI" | Foreach {
    Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppXManifest.xml" -Force
}

# 5. Aplicar Preferências do Defender
Write-Host "[5/5] Forçando ativação do monitoramento..." -ForegroundColor Yellow
Set-MpPreference -DisableRealtimeMonitoring $false
Set-MpPreference -DisableBehaviorMonitoring $false
Set-MpPreference -DisableBlockAtFirstSeen $false
Set-MpPreference -DisableIOAVProtection $false
Set-MpPreference -DisablePrivacyMode $true

# Atualizar políticas de grupo
gpupdate /force

Write-Host "`n✅ REPARO CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
Write-Host "----------------------------------------------------"
Write-Host "PRÓXIMO PASSO OBRIGATÓRIO:" -ForegroundColor Red
Write-Host "1. Reinicie o computador imediatamente." -ForegroundColor White
Write-Host "2. Após reiniciar, a Central de Segurança voltará ao normal." -ForegroundColor White
Write-Host "----------------------------------------------------"
Read-Host "Pressione Enter para sair..."
