# FLUX OS - Script de Recuperação de Emergência (Defender)
# Execute este script como ADMINISTRADOR

Write-Host "--- Iniciando Recuperação Profunda do Windows Defender ---" -ForegroundColor Cyan

# 1. Limpar Políticas de Grupo e Bloqueios
$policies = @(
    "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender",
    "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection",
    "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender\Spynet",
    "HKLM:\SOFTWARE\Microsoft\Windows Defender"
)

foreach ($poly in $policies) {
    if (Test-Path $poly) {
        Write-Host "Limpando políticas e bloqueios em $poly..."
        # Remover valores específicos que costumam desativar o Defender
        Remove-ItemProperty -Path $poly -Name "DisableAntiSpyware" -ErrorAction SilentlyContinue
        Remove-ItemProperty -Path $poly -Name "DisableAntiVirus" -ErrorAction SilentlyContinue
        Remove-ItemProperty -Path $poly -Name "DisableRealtimeMonitoring" -ErrorAction SilentlyContinue
    }
}

# 2. Restaurar Serviços (Modo Direto via Registro para ignorar bloqueios de permissão do Service Manager)
Write-Host "Restaurando inicialização dos serviços no Kernel..." -ForegroundColor Yellow
$services = @{
    "WinDefend" = 2;             # Auto
    "WdNisSvc"  = 3;             # Manual
    "Sense"     = 3;             # Manual
    "WdFilter"  = 0;             # Boot
    "WdBoot"    = 0;             # Boot
    "WdNisDrv"  = 3;             # Manual
    "SecurityHealthService" = 2; # Auto (Importante para abrir a interface)
    "wscsvc"    = 2;             # Security Center (Auto)
    "mpssvc"    = 2;             # Firewall (Auto)
}

foreach ($svc in $services.Keys) {
    $path = "HKLM:\SYSTEM\CurrentControlSet\Services\$svc"
    if (Test-Path $path) {
        Write-Host "Resetando $svc para o padrão..."
        Set-ItemProperty -Path $path -Name "Start" -Value $services[$svc] -Force -ErrorAction SilentlyContinue
    }
}

# 3. Reativar Preferências e Resetar Interface
Write-Host "Reativando monitoramento e resetando interface (SecHealthUI)..." -ForegroundColor Cyan
Set-MpPreference -DisableRealtimeMonitoring $false -ErrorAction SilentlyContinue
Set-MpPreference -DisableBehaviorMonitoring $false -ErrorAction SilentlyContinue

# Comando para resetar a janela de segurança que não abre
Get-AppXPackage -AllUsers -Name Microsoft.SecHealthUI | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppXManifest.xml"} -ErrorAction SilentlyContinue

# 4. Atualizar Sistema e Forçar Início
Write-Host "Atualizando políticas do Windows..." -ForegroundColor Green
gpupdate /force

Write-Host "Tentando iniciar serviços críticos..." -ForegroundColor Cyan
Start-Service WinDefend -ErrorAction SilentlyContinue
Start-Service SecurityHealthService -ErrorAction SilentlyContinue

Write-Host "`n✅ PROCESSO CONCLUÍDO!" -ForegroundColor Green
Write-Host "IMPORTANTE: Se o Defender ainda não aparecer ativo, REINICIE o computador agora." -ForegroundColor White
Write-Host "As alterações de Kernel só entram em vigor após o Boot." -ForegroundColor Yellow
Read-Host "Pressione Enter para fechar..."
