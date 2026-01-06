import streamlit as st
import random
import time

# --- CONFIGURAÇÃO DA VIBE (CSS & ESTÉTICA) ---
st.set_page_config(page_title="Dark Castle 8-Bit", page_icon="🏰", layout="centered")

# O segredo do Vibe Coding: CSS injetado para criar atmosfera
st.markdown("""
<style>
    /* Importando fonte retro simulada */
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

    /* Fundo e Fonte Geral */
    .stApp {
        background-color: #050505;
        font-family: 'VT323', monospace;
        font-size: 22px;
    }
    
    /* Títulos Neon */
    h1, h2, h3 {
        color: #4af626 !important;
        text-shadow: 0 0 10px #228d10;
        font-family: 'VT323', monospace;
        letter-spacing: 2px;
    }

    /* Botões Retro */
    .stButton>button {
        background-color: #111;
        color: #4af626;
        border: 2px solid #4af626;
        border-radius: 0px;
        font-family: 'VT323', monospace;
        font-size: 20px;
        transition: all 0.3s;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background-color: #4af626;
        color: #000;
        box-shadow: 0 0 15px #4af626;
    }

    /* Efeito de Scanline (Monitor CRT) */
    .scanlines {
        position: fixed;
        left: 0;
        top: 0;
        width: 100vw;
        height: 100vh;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        background-size: 100% 4px, 6px 100%;
        pointer-events: none;
        z-index: 9999;
    }

    /* Containers de Status */
    div[data-testid="stMetricValue"] {
        font-family: 'VT323', monospace;
        color: #ffcc00;
    }
</style>
<div class="scanlines"></div>
""", unsafe_allow_html=True)

# --- BIBLIOTECA DE ASSETS (ASCII ART) ---
ASCII_ARTS = {
    "title": """
    ▓█████▄  ▄▄▄       ██▀███   ██ ▄█▀
    ▒██▀ ██▌▒████▄    ▓██ ▒ ██▒ ██▄█▒ 
    ░██   █▌▒██  ▀█▄  ▓██ ░▄█ ▒▓███▄░ 
    ░▓█▄   ▌░██▄▄▄▄██ ▒██▀▀█▄  ▓██ █▄ 
    ░▒████▓  ▓█   ▓██▒░██▓ ▒██▒▒██▒ █▄
     ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒▓ ░▒▓░▒ ▒▒ ▓▒
     ░ ▒  ▒   ▒   ▒▒ ░  ░▒ ░ ▒░░ ░▒ ▒░
     ░ ░  ░   ░   ▒     ░░   ░ ░ ░░ ░ 
       ░          ░  ░   ░     ░  ░   
    """,
    "warrior": "🛡️ GUERREIRO",
    "mage": "🔮 MAGO",
    "enemy_goblin": """
      (    )
     ((((  ))))
    (  '  '   )
     (   ^   )
      (  -  )
    """,
    "enemy_dragon": """
         / \  //\
   |\___/|      /   \//  \\
   /0  0  \__  /    //  | \ \    
  /     /  \/_/    //   |  \  \  
  @_^_@'/   \/_   //    |   \   \ 
  //_^_/     \/_ //     |    \    \
 ( //) |        \///      |     \     \
    """
}

# --- LÓGICA DO JOGO (ENGINE) ---

def init_game():
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
    if 'hero_class' not in st.session_state:
        st.session_state.hero_class = None
    if 'xp' not in st.session_state:
        st.session_state.xp = 0
    if 'level' not in st.session_state:
        st.session_state.level = 1

def start_adventure(classe):
    st.session_state.game_active = True
    st.session_state.hero_class = classe
    st.session_state.hp = 120 if classe == "warrior" else 80
    st.session_state.max_hp = st.session_state.hp
    st.session_state.mana = 20 if classe == "warrior" else 100
    st.session_state.gold = 0
    st.session_state.log = ["⚔️ A portão do castelo se abre com um rangido..."]
    st.session_state.enemy = None

def render_sidebar():
    with st.sidebar:
        st.title("📜 PERFIL")
        if st.session_state.game_active:
            role = ASCII_ARTS[st.session_state.hero_class]
            st.write(f"**Classe:** {role}")
            st.write(f"**Nível:** {st.session_state.level}")
            
            # Barras de Progresso
            hp_percent = st.session_state.hp / st.session_state.max_hp
            st.write(f"❤️ VIDA: {st.session_state.hp}")
            st.progress(max(0.0, min(1.0, hp_percent)))
            
            st.write(f"💙 MANA: {st.session_state.mana}")
            st.progress(min(1.0, st.session_state.mana / 100))
            
            st.write(f"⭐ XP: {st.session_state.xp}")
            
            st.markdown("---")
            st.write("🎒 **Inventário:**")
            st.write(f"💰 Ouro: {st.session_state.gold}")
            if st.button("🔴 Sair do Jogo"):
                st.session_state.clear()
                st.rerun()

def combat_turn(action):
    enemy = st.session_state.enemy
    hero_class = st.session_state.hero_class
    
    # Turno do Jogador
    dmg = 0
    log_msg = ""
    
    if action == "attack":
        base_dmg = random.randint(10, 20)
        bonus = 5 if hero_class == "warrior" else 0
        dmg = base_dmg + bonus
        log_msg = f"⚔️ Você atacou com sua arma causando {dmg} de dano!"
    
    elif action == "magic":
        cost = 20
        if st.session_state.mana >= cost:
            st.session_state.mana -= cost
            base_dmg = random.randint(25, 40)
            bonus = 10 if hero_class == "mage" else 0
            dmg = base_dmg + bonus
            log_msg = f"🔥 Você lançou uma bola de fogo causando {dmg} de dano!"
        else:
            log_msg = "💧 Mana insuficiente! Você tropeçou tentando conjurar."
            
    # Aplicar dano
    enemy['hp'] -= dmg
    st.session_state.log.insert(0, log_msg)
    
    # Checar vitória
    if enemy['hp'] <= 0:
        xp_gain = random.randint(20, 50)
        gold_gain = random.randint(10, 30)
        st.session_state.xp += xp_gain
        st.session_state.gold += gold_gain
        st.session_state.enemy = None
        st.session_state.log.insert(0, f"💀 Inimigo derrotado! +{xp_gain} XP | +{gold_gain} Ouro")
        
        # Level Up simplificado
        if st.session_state.xp > 100 * st.session_state.level:
            st.session_state.level += 1
            st.session_state.max_hp += 20
            st.session_state.hp = st.session_state.max_hp
            st.balloons()
            st.session_state.log.insert(0, f"🆙 LEVEL UP! Agora você é nível {st.session_state.level}!")
            
    else:
        # Turno do Inimigo
        enemy_dmg = random.randint(5, 15)
        st.session_state.hp -= enemy_dmg
        st.session_state.log.insert(0, f"🩸 O inimigo contra-atacou! -{enemy_dmg} HP")
        if st.session_state.hp <= 0:
            st.error("💀 VOCÊ MORREU...")
            if st.button("Renascer"):
                st.session_state.clear()
                st.rerun()
            st.stop()

# --- MAIN LOOP ---
init_game()
render_sidebar()

if not st.session_state.game_active:
    st.markdown(f"<pre style='color: #4af626; line-height: 10px;'>{ASCII_ARTS['title']}</pre>", unsafe_allow_html=True)
    st.write("Escolha seu destino, aventureiro:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🛡️ GUERREIRO")
        st.write("Força bruta e alta resistência.")
        if st.button("ESCOLHER GUERREIRO"):
            start_adventure("warrior")
            st.rerun()
            
    with col2:
        st.markdown("### 🔮 MAGO")
        st.write("Poder arcano destrutivo e mana.")
        if st.button("ESCOLHER MAGO"):
            start_adventure("mage")
            st.rerun()

else:
    # Tela de Jogo
    st.title("🏰 O Corredor Escuro")
    
    # Se não tem inimigo, oferecer exploração
    if not st.session_state.enemy:
        st.info("O caminho está livre, mas o silêncio é assustador...")
        
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button("👣 AVANÇAR NO ESCURO", use_container_width=True):
                dice = random.randint(1, 10)
                if dice <= 6: # 60% chance de encontro
                    monsters = [
                        {'name': 'Goblin Saqueador', 'hp': 40, 'art': ASCII_ARTS['enemy_goblin']},
                        {'name': 'Dragão das Sombras', 'hp': 100, 'art': ASCII_ARTS['enemy_dragon']}
                    ]
                    st.session_state.enemy = random.choice(monsters)
                    st.session_state.log.insert(0, f"⚠️ Um {st.session_state.enemy['name']} surgiu das sombras!")
                    st.rerun()
                else:
                    st.session_state.log.insert(0, "🍂 Nada além de poeira e ossos antigos.")
                    st.rerun()
        
        with col_act2:
            if st.button("🏕️ DESCANSAR (Recuperar HP)", use_container_width=True):
                st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + 20)
                st.session_state.mana = min(100, st.session_state.mana + 20)
                st.session_state.log.insert(0, "💤 Você descansou e recuperou forças.")
                st.rerun()

    # Se tem inimigo, modo de combate
    else:
        enemy = st.session_state.enemy
        st.markdown(f"### 👹 {enemy['name']} (HP: {enemy['hp']})")
        st.code(enemy['art']) # Exibe a ASCII art do monstro
