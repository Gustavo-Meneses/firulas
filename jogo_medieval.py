import streamlit as st
import random
import time

# --- ESTÉTICA, UI E ANIMAÇÕES ---
st.set_page_config(page_title="Dark Castle: Definitive Edition", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    .stApp { background-color: #050505; font-family: 'VT323', monospace; color: #4af626; font-size: 20px; }
    
    /* Animações */
    @keyframes monsterDeath {
        0% { transform: scale(1); opacity: 1; }
        100% { transform: scale(0) rotate(90deg); opacity: 0; }
    }
    .monster-die { animation: monsterDeath 1.5s forwards; text-align: center; font-size: 40px; color: red; }

    @keyframes explode {
        0% { transform: scale(1); }
        50% { transform: scale(1.5); color: orange; }
        100% { transform: scale(0); opacity: 0; }
    }
    .player-explode { animation: explode 1s infinite; font-size: 50px; text-align: center; }

    .hero-panel { background: rgba(0, 255, 0, 0.05); border: 2px solid #4af626; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
    .stat-tag { color: #ffcc00; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO SEGURA ---
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False, 'hero_class': "Viajante", 'level': 1, 'hp': 100, 'max_hp': 100, 
        'mana': 50, 'gold': 0, 'log': ["O castelo te espera..."], 'enemy': None,
        'weapon': {"name": "Punhal Velho", "atk": 8, "type": "weapon"},
        'armor': {"name": "Trapos", "def": 2, "type": "armor"},
        'floor': 1, 'kills_on_floor': 0, 'in_shop': False, 'chest_found': False,
        'inventory': [], 'game_state': 'playing'
    })

# Metas de monstros por andar
FLOOR_GOALS = {1: 3, 2: 4, 3: 5, 4: 2, 5: 1}

def add_log(msg):
    st.session_state.log.insert(0, msg)

def start_game(role):
    st.session_state.game_active = True
    st.session_state.hero_class = role
    if role == "Guerreiro":
        st.session_state.hp = st.session_state.max_hp = 150
        st.session_state.weapon = {"name": "Machado de Ferro", "atk": 15, "type": "weapon"}
        st.session_state.armor = {"name": "Peitoral de Couro", "def": 5, "type": "armor"}
    else:
        st.session_state.hp = st.session_state.max_hp = 90
        st.session_state.mana = 120
        st.session_state.weapon = {"name": "Cajado Rúnico", "atk": 10, "type": "weapon"}
        st.session_state.armor = {"name": "Manto de Seda", "def": 3, "type": "armor"}
    st.rerun()

# --- LÓGICA DO BOSS ADAPTATIVO ---
def spawn_boss():
    power = st.session_state.weapon.get('atk', 0) + st.session_state.armor.get('def', 0)
    if power < 30: hp, atk, diff = 300, 20, "50%"
    elif power < 60: hp, atk, diff = 500, 35, "70%"
    else: hp, atk, diff = 800, 50, "90%"
    st.session_state.enemy = {"name": "🔥 LORDE DAS SOMBRAS", "hp": hp, "max_hp": hp, "atk": atk, "difficulty": diff}

# --- TELA INICIAL (COM INFORMAÇÕES GERAIS) ---
if not st.session_state.game_active:
    st.title("🏰 DARK CASTLE: ASCENSÃO")
    
    with st.expander("📖 GUIA DO AVENTUREIRO (COMO JOGAR)", expanded=True):
        st.markdown("""
        - **Objetivo:** Explore os andares até o 5º nível para derrotar o Lorde das Sombras.
        - **Andares:** Cada andar exige um número de abates para avançar (Andar 1: 3 | Andar 2: 4 | Andar 3: 5 | Andar 4: 2).
        - **Bolsa & Itens:** Use o inventário para equipar armas/armaduras encontradas ou tomar poções.
        - **O Chefe:** O Lorde das Sombras adapta sua força baseada nos seus itens atuais.
        - **Morte:** Se seu HP chegar a 0, você explode e perde o progresso!
        """)
    
    st.subheader("Escolha sua classe para iniciar:")
    col1, col2 = st.columns(2)
    if col1.button("🛡️ GUERREIRO", use_container_width=True): start_game("Guerreiro")
    if col2.button("🔮 MAGO", use_container_width=True): start_game("Mago")

# --- TELAS DE FIM DE JOGO / ANIMAÇÕES ---
elif st.session_state.game_state == 'player_dead':
    st.markdown("<div class='player-explode'>💥 EXPLODINDO 💥</div>", unsafe_allow_html=True)
    if st.session_state.enemy and "LORDE" in st.session_state.enemy['name']:
        st.markdown("<h2 style='color:red; text-align:center;'>HA HA HA! TÃO PREVISÍVEL...</h2>", unsafe_allow_html=True)
    st.error("VOCÊ MORREU!")
    if st.button("Tentar Novamente"): st.session_state.clear(); st.rerun()

elif st.session_state.game_state == 'player_win':
    st.balloons()
    st.success("O LORDE FOI FATIADO! VOCÊ VENCEU!")
    st.markdown("<h1 style='text-align:center;'>⚔️ HERÓI LENDÁRIO ⚔️</h1>", unsafe_allow_html=True)
    if st.button("Jogar Novamente"): st.session_state.clear(); st.rerun()

# --- LOOP DE JOGO ATIVO ---
else:
    # HUD do Personagem (Proteção contra HP negativo na barra)
    avatar = "🛡️" if st.session_state.hero_class == "Guerreiro" else "🔮"
    current_hp = max(0, st.session_state.hp)
    hp_ratio = max(0.0, min(1.0, current_hp / st.session_state.max_hp))
    
    st.markdown(f"""
    <div class="hero-panel">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="font-size: 50px;">{avatar}</div>
            <div style="flex-grow: 1;">
                <div><b>{st.session_state.hero_class.upper()}</b> | ANDAR {st.session_state.floor}</div>
                <div style="font-size: 14px;">Abates no andar: {st.session_state.kills_on_floor} / {FLOOR_GOALS.get(st.session_state.floor, 1)}</div>
                <div>💰 {st.session_state.gold}G | ❤️ {current_hp}/{st.session_state.max_hp}</div>
            </div>
        </div>
        <div style="margin-top: 10px; border-top: 1px solid #4af626; padding-top: 5px; font-size: 15px;">
            ⚔️ {st.session_state.weapon.get('name', 'Nenhum')} <span class='stat-tag'>(+{st.session_state.weapon.get('atk', 0)} ATK)</span> | 
            🛡️ {st.session_state.armor.get('name', 'Nenhum')} <span class='stat-tag'>(+{st.session_state.armor.get('def', 0)} DEF)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(hp_ratio)

    # Lógica de Combate
    if st.session_state.enemy:
        enemy = st.session_state.enemy
        st.subheader(f"👹 {enemy['name']}")
        
        c1, c2 = st.columns(2)
        if c1.button("⚔️ ATACAR"):
            dmg = st.session_state.weapon.get('atk', 5) + random.randint(5, 12)
            enemy['hp'] -= dmg
            add_log(f"💥 Você causou {dmg} de dano!")
            
            if enemy['hp'] <= 0:
                if "LORDE" in enemy['name']: st.session_state.game_state = 'player_win'
                else:
                    add_log("🏆 Monstro derrotado!")
                    st.session_state.gold += 50
                    st.session_state.kills_on_floor += 1
                    st.session_state.enemy = None
                    if st.session_state.kills_on_floor >= FLOOR_GOALS.get(st.session_state.floor, 3):
                        st.session_state.floor += 1
                        st.session_state.kills_on_floor = 0
                st.rerun()
            else:
                edmg = max(2, enemy.get('atk', 15) - st.session_state.armor.get('def', 0))
                st.session_state.hp -= edmg
                if st.session_state.hp <= 0: st.session_state.game_state = 'player_dead'
                st.rerun()

    # Lógica de Exploração
    elif st.session_state.chest_found:
        st.info("🎁 Você encontrou um baú!")
        if st.button("Abrir Baú"):
            item = random.choice([{"name": "Espada Curta", "atk": 20, "type": "weapon"}, {"name": "Escudo Leve", "def": 10, "type": "armor"}, {"name": "Poção", "type": "potion"}])
            st.session_state.inventory.append(item)
            add_log(f"🎁 Encontrou: {item['name']}!")
            st.session_state.chest_found = False
            st.rerun()

    else:
        if st.button("👣 EXPLORAR PRÓXIMA SALA"):
            if st.session_state.floor == 5: spawn_boss()
            else:
                roll = random.random()
                if roll < 0.6: st.session_state.enemy = {"name": f"Orc do Andar {st.session_state.floor}", "hp": 50 + st.session_state.floor*10, "atk": 10 + st.session_state.floor*3}
                elif roll < 0.85: st.session_state.chest_found = True
                else: add_log("👣 Corredor vazio...")
            st.rerun()

    # Log de mensagens
    st.write("---")
    for line in st.session_state.log[:3]: st.
