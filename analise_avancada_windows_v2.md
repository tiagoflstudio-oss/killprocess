# 🔬 Relatório de Análise Avançada: Killprocess v2.1 (Deep Kernel)

## 📅 Data: 06 de Maio de 2026
## 🎯 Objetivo: Transformar o Windows 11 em uma plataforma de latência zero para e-Sports.

---

## 1. 🚀 Oportunidades de Otimização (O que não temos hoje)

### A. MSI Mode (Message Signaled Interrupts)
Atualmente, a maioria dos dispositivos usa o modo de interrupção legado (Line-Based), que causa picos de CPU. 
- **Plano**: Criar um módulo que detecta o ID da GPU no registro e ativa o modo MSI com prioridade "High". Isso reduz drasticamente o *input lag*.

### B. Win32PrioritySeparation (Process Scheduler)
O Windows divide o tempo de CPU de forma genérica.
- **Plano**: Ajustar o registro para `0x26` (38 Decimal). Isso dá fatias de tempo mais curtas e constantes para o processo em primeiro plano (o jogo), garantindo que o movimento do mouse seja processado sem atraso por tarefas de fundo.

### C. Network Throttling & TCP Stack
O Windows limita o tráfego de rede para economizar CPU.
- **Plano**: Definir `NetworkThrottlingIndex` para `0xFFFFFFFF`. Isso desativa o "estrangulamento" de pacotes, essencial para jogos competitivos.

### D. Purga da Standby List (Memória RAM)
O Windows mantém dados "úteis" na RAM que muitas vezes causam travamentos (stutter) quando o jogo precisa de memória limpa imediatamente.
- **Plano**: Implementar um script `EmptyWorkingSet` ou similar para limpar a memória em espera antes de lançar o jogo.

---

## 2. 🛡️ Novo "Nível 8: Kernel & Hardware Optimization"
Proposta de inclusão de uma nova aba ou nível no Cockpit:

1.  **Interrupt Affinity**: Forçar drivers de rede e vídeo a rodarem em núcleos específicos.
2.  **Disable VBS/HVCI**: Opção para desativar a Isolação de Núcleo (ganho de ~5-10% de FPS, com trade-off de segurança).
3.  **FSE Fix (Full Screen Optimizations)**: Ajustes globais para garantir que o Windows não tente "ajudar" o jogo com o modo de otimização de tela cheia que, às vezes, causa latência.

---

## 3. 📝 Plano de Execução (Fase 6)

1.  **Pesquisa de Scripts de Registro**: Mapear as chaves exatas de `SystemProfile` e `PriorityControl`.
2.  **Módulo de Detecção MSI**: Criar lógica Python para ler o `Enum\PCI` e identificar a placa de vídeo.
3.  **Prototipagem de UI**: Desenhar os novos botões no layout Sapphire (sempre pedindo autorização antes de implementar).

---
### ⚠️ Nota de Segurança
Todas essas alterações são reversíveis pelo botão "Restaurar Padrões", que será atualizado para incluir a limpeza desses novos registros de Kernel.

**Aguardando ordens para iniciar o detalhamento técnico ou a implementação.**
