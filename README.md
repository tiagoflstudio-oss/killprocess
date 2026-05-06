# 🚀 FLUX OS - Otimizador Supremo do Windows para Gamers

O **FLUX OS** é um aplicativo projetado para desativar serviços e processos em segundo plano do Windows, liberando o máximo de CPU, Memória RAM e reduzindo a latência para jogos.

---

## 🎚️ Níveis de Otimização (7 Níveis Completos)

O sistema de otimização foi expandido para **7 níveis**, permitindo que o usuário escolha a agressividade com que os processos serão encerrados.

### 🟢 Nível 1: Aplicativos & Bloatwares
Focado em fechar softwares em segundo plano que consumem RAM e CPU.
- **Exemplos:** Google Chrome, MS Edge, Discord, OneDrive, WhatsApp, Teams, Skype.

### 🟡 Nível 2: Impressão & Manutenção
Desativa serviços que consomem recursos de I/O em segundo plano.
- **Exemplos:** Spooler de impressão, Windows Search (Indexador), SysMain (Superfetch), Hyper-V.

### 🟠 Nível 3: Telemetria & Rastreamento
Desativa rastreamento, envio de dados de diagnóstico e manutenção de índice.
- **Exemplos:** DiagTrack (Telemetria Microsoft), PimIndexMaintenanceSvc, UserDataSvc.

### 🔴 Nível 4: Xbox & Conexões Secundárias
Focado em serviços de console e periféricos que gamers de PC competitivos não utilizam.
- **Exemplos:** Autenticação do Xbox Live, Xbox Game Save, Bluetooth, NFC, Telefonia e Sensores.

### 🌐 Nível 5: Redes & Streaming
Impede o consumo de rede e banda em segundo plano para máxima estabilidade e menor ping nos jogos.
- **Exemplos:** Compartilhamento de Internet (ICS), Geolocalização, Mapas Baixados, Controles dos Pais, Modo Demonstração de Varejo.

### 🔒 Nível 6: Segurança & Criptografia
Para jogadores hardcore que querem máxima performance na CPU.
- **Exemplos:** Gerenciador de Credenciais, Cartão Inteligente, Windows Insider Service, Registro Remoto, Biometria.

### 👑 Nível 7: Modo Deus (God Mode)
O nível supremo de otimização barebone.
- **Ações:** Força a seleção de absolutamente todas as checkboxes da interface visual e desativa unconditionally todos os processos e serviços mapeados no programa.

---

## 🛠️ Desenvolvimento e Build

Para gerar uma nova versão do executável (`.exe`) de forma automatizada, utilize o script de build incluído:

1.  Certifique-se de ter o Python instalado.
2.  Instale as dependências (se necessário): `pip install -r requirements.txt`
3.  Execute o script de build:
    ```bash
    python build.py
    ```
4.  O executável final será gerado na pasta `dist/` com o nome **Flux_OS_Sapphire.exe**.

> [!IMPORTANT]
> O executável gerado solicitará automaticamente privilégios de Administrador ao ser iniciado, garantindo que todas as otimizações de Kernel e Registro funcionem corretamente.

