SERVICES_MAP = {
    "Nível 1: Aplicativos & Bloatwares": [
        {"id": "chrome", "name": "Google Chrome", "type": "process", "checked": True},
        {"id": "msedge", "name": "Microsoft Edge", "type": "process", "checked": True},
        {"id": "onedrive", "name": "Microsoft OneDrive", "type": "process", "checked": True},
        {"id": "teams", "name": "Microsoft Teams", "type": "process", "checked": True},
        {"id": "discord", "name": "Discord Client", "type": "process", "checked": True},
        {"id": "spotify", "name": "Spotify Background", "type": "process", "checked": True},
        {"id": "zoom", "name": "Zoom Meeting Service", "type": "process", "checked": True},
        {"id": "skype", "name": "Skype", "type": "process", "checked": True},
        {"id": "whatsapp", "name": "WhatsApp", "type": "process", "checked": True},
        {"id": "slack", "name": "Slack Client", "type": "process", "checked": True},
        {"id": "telegram", "name": "Telegram Desktop", "type": "process", "checked": True},
        {"id": "anydesk", "name": "AnyDesk Remote", "type": "process", "checked": True},
        {"id": "winword", "name": "Microsoft Word", "type": "process", "checked": True},
        {"id": "excel", "name": "Microsoft Excel", "type": "process", "checked": True},
        {"id": "powerpnt", "name": "Microsoft PowerPoint", "type": "process", "checked": True},
        {"id": "notepad", "name": "Notepad", "type": "process", "checked": True},
        {"id": "calc", "name": "Windows Calculator", "type": "process", "checked": True},
        {"id": "acrobat", "name": "Adobe Acrobat Reader", "type": "process", "checked": True},
        {"id": "dropbox", "name": "Dropbox Client", "type": "process", "checked": True},
        {"id": "teamviewer", "name": "TeamViewer", "type": "process", "checked": True}
    ],
    "Nível 2: Impressão & Manutenção": [
        {"id": "Spooler", "name": "Spooler de Impressão", "type": "service", "checked": True},
        {"id": "WSearch", "name": "Windows Search (Indexador)", "type": "service", "checked": True},
        {"id": "SysMain", "name": "SysMain (Superfetch)", "type": "service", "checked": True},
        {"id": "Themes", "name": "Temas Visuais do Windows", "type": "service", "checked": False},
        {"id": "TabletInputService", "name": "Teclado Virtual / Caneta", "type": "service", "checked": True},
        {"id": "PcaSvc", "name": "Assistente de Compatibilidade", "type": "service", "checked": True},
        {"id": "WerSvc", "name": "Relatório de Erros do Windows", "type": "service", "checked": True},
        {"id": "Fax", "name": "Serviço de Fax", "type": "service", "checked": True},
        {"id": "PrintWorkflowUserSvc", "name": "Fluxo de Trabalho de Impressão", "type": "service", "checked": True},
        {"id": "StiSvc", "name": "Aquisição de Imagens", "type": "service", "checked": True},
        {"id": "DPS", "name": "Serviço de Diretivas de Diagnóstico", "type": "service", "checked": True},
        {"id": "WdiServiceHost", "name": "Host de Serviço de Diagnóstico", "type": "service", "checked": True},
        {"id": "WdiSystemHost", "name": "Host de Sistema de Diagnóstico", "type": "service", "checked": True},
        {"id": "vmicguest", "name": "Hyper-V Guest", "type": "service", "checked": True},
        {"id": "vmictimesync", "name": "Hyper-V Time Sync", "type": "service", "checked": True},
        {"id": "vmicrdv", "name": "Hyper-V Remote Desktop", "type": "service", "checked": True},
        {"id": "vmicvmsession", "name": "Hyper-V VM Session", "type": "service", "checked": True}
    ],
    "Nível 3: Telemetria & Rastreamento": [
        {"id": "DiagTrack", "name": "Telemetria da Microsoft", "type": "service", "checked": True},
        {"id": "PimIndexMaintenanceSvc", "name": "Manutenção de Índice Pim", "type": "service", "checked": True},
        {"id": "ContactData", "name": "Dados de Contatos", "type": "service", "checked": True},
        {"id": "UserDataSvc", "name": "Acesso a Dados de Usuário", "type": "service", "checked": True},
        {"id": "OneSyncSvc", "name": "Sincronização do Host", "type": "service", "checked": True},
        {"id": "DusmSvc", "name": "Uso de Dados", "type": "service", "checked": True},
        {"id": "AppReadiness", "name": "Preparação de Aplicativos", "type": "service", "checked": True}
    ],
    "Nível 4: Xbox & Conexões Secundárias": [
        {"id": "XblAuthManager", "name": "Autenticação do Xbox Live", "type": "service", "checked": True},
        {"id": "XblGameSave", "name": "Salvar Jogos do Xbox Live", "type": "service", "checked": True},
        {"id": "XboxNetApiSvc", "name": "Rede do Xbox Live", "type": "service", "checked": True},
        {"id": "XboxGipSvc", "name": "Acessórios do Xbox", "type": "service", "checked": True},
        {"id": "bthserv", "name": "Serviço de Bluetooth", "type": "service", "checked": True},
        {"id": "BTAGCategoryService", "name": "Áudio Bluetooth", "type": "service", "checked": True},
        {"id": "BluetoothUserService", "name": "Serviço de Usuário de Bluetooth", "type": "service", "checked": True},
        {"id": "NfcService", "name": "NFC Service", "type": "service", "checked": True},
        {"id": "PhoneSvc", "name": "Serviço de Telefone", "type": "service", "checked": True},
        {"id": "SensorSvc", "name": "Serviço de Sensores", "type": "service", "checked": True},
        {"id": "SensorDataSvc", "name": "Dados dos Sensores", "type": "service", "checked": True},
        {"id": "SensorsSrv", "name": "Servidor de Sensores", "type": "service", "checked": True},
    ],
    "Nível 5: Redes & Streaming": [
        {"id": "SharedAccess", "name": "Compartilhamento de Internet", "type": "service", "checked": True},
        {"id": "lfsvc", "name": "Serviço de Geolocalização", "type": "service", "checked": True},
        {"id": "MapsBroker", "name": "Gerenciador de Mapas Baixados", "type": "service", "checked": True},
        {"id": "WpcProvider", "name": "Controles dos Pais", "type": "service", "checked": True},
        {"id": "RetailDemo", "name": "Modo de Demonstração de Varejo", "type": "service", "checked": True},
        {"id": "AJRouter", "name": "Roteamento AllJoyn", "type": "service", "checked": True},
    ],
    "Nível 6: Segurança & Biometria": [
        {"id": "WbioSrvc", "name": "Serviço Biométrico do Windows", "type": "service", "checked": True},
        {"id": "KeyIso", "name": "Isolamento de Chaves CNG", "type": "service", "checked": False},
        {"id": "VaultSvc", "name": "Gerenciador de Credenciais", "type": "service", "checked": False},
        {"id": "AppIDSvc", "name": "Identidade do Aplicativo", "type": "service", "checked": True},
        {"id": "CryptSvc", "name": "Serviços Criptográficos", "type": "service", "checked": False}
    ],
    "Nível 7: God Mode (Extreme)": [
        {"id": "explorer.exe", "name": "Windows Explorer (God Mode)", "type": "process", "checked": True},
        {"id": "ShellExperienceHost.exe", "name": "Shell Experience", "type": "process", "checked": True},
        {"id": "SearchHost.exe", "name": "Search Host", "type": "process", "checked": True},
        {"id": "StartMenuExperienceHost.exe", "name": "Start Menu Host", "type": "process", "checked": True}
    ],
    "Nível 8: Polish (Serviços Fantasmas)": [
        {"id": "SDRSVC", "name": "Backup do Windows", "type": "service", "checked": True},
        {"id": "VSS", "name": "Cópia de Sombra de Volume", "type": "service", "checked": True},
        {"id": "wbengine", "name": "Mecanismo de Backup", "type": "service", "checked": True},
        {"id": "defragsvc", "name": "Otimizar Unidades", "type": "service", "checked": True}
    ],
    "Nível 9: Engine (Núcleo)": [
        {"id": "Power", "name": "Serviço de Energia (Ajuste)", "type": "service", "checked": False},
        {"id": "DcomLaunch", "name": "Iniciador de Processos DCOM", "type": "service", "checked": False},
        {"id": "RpcSs", "name": "Chamada de Procedimento Remoto", "type": "service", "checked": False}
    ],
    "Nível 10: NVIDIA GPU Elite": [
        {"id": "gpu_latency", "name": "Latência Ultra (Kernel Response)", "type": "gpu_tweak", "checked": True},
        {"id": "gpu_shaders", "name": "Shader Cache 10GB (Fim dos Stutters)", "type": "gpu_tweak", "checked": True},
        {"id": "gpu_clean", "name": "Limpeza de Telemetria NVIDIA", "type": "gpu_tweak", "checked": True},
        {"id": "gpu_hags", "name": "Hardware GPU Scheduling (HAGS)", "type": "gpu_tweak", "checked": True},
        {"id": "gpu_unleashed", "name": "GPU Unleashed (Max Performance)", "type": "gpu_tweak", "checked": True}
    ]
}
