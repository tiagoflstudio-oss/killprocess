# 🎨 Identidade Visual e UI/UX - Killprocess

O design do **Killprocess** deve ser minimalista, agressivo, focado no público gamer e passar uma sensação de velocidade e máxima performance.

---

## 🎨 Paleta de Cores e Estilo

- **Fundo Principal (Background):** `#09090B` (Preto Carbono profundo / Dark Mode absoluto).
- **Cor de Destaque / Ação (Accent):** `#EC4899` a `#EF4444` (Um gradiente neon agressivo de Rosa para Vermelho).
- **Cor Secundária / Suporte:** `#3B82F6` (Azul Elétrico - usado para o modo de Restauração).
- **Superfícies (Cards/Modais):** `#18181B` com opacidade de `75%` e efeito **Glassmorphism** (Blured background + bordas finas semi-transparentes de `#27272A`).
- **Tipografia:** `Inter` ou `Orbitron` para títulos e métricas, passando a ideia de software futurista/gamer.

---

## 🖥️ Estrutura da Interface (Telas & Componentes)

### 1. Dashboard (Visão Geral)
- **Métricas em tempo real:**
  - Uso de CPU em porcentagem (`%`).
  - Uso de Memória RAM em Gigabytes (`GB`) usados / disponíveis.
  - Quantidade de processos ativos no momento (Ex: "Atualmente 145 processos ativos").
- **Seletor de Níveis:** 
  - Um controle do tipo *Slider* ou botões de rádio estilizados como botões mecânicos ou luzes LED:
    - 🟢 Nível 1: Básico
    - 🟡 Nível 2: Gamer Standard
    - 🟠 Nível 3: Gamer Hardcore
    - 🔴 Nível 4: Gamer Extremo
    - 🔥 Nível 5: Gaming Pro (Barebone)

### 2. Botão de Ação Central
- **Modo Otimizar:** Botão grande em destaque, mudando de cor de acordo com o nível selecionado.
  - "ATIVAR MODO GAMER"
- **Modo Restaurar:** Botão secundário estilizado em Azul Elétrico:
  - "RESTAURAR PADRÕES DO WINDOWS"

---

## ✨ Micro-animações e Interações (UX Spells)

- **Efeito de Pulsação:** O botão "ATIVAR MODO GAMER" deve ter um leve efeito de pulsação luminosa (glow) quando o nível 5 estiver selecionado.
- **Transição de Estados:** Quando o nível 5 é ativado, a tela deve mostrar um contador regressivo de 3 segundos com um efeito visual de "Derrubando processos" antes de fechar o Explorer.
- **Feedback visual de liberação:** Exibir uma notificação sutil dizendo quanto de RAM foi liberado (Ex: `+ 2.4 GB de RAM liberados!`).
