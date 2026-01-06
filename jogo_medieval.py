import streamlit as st
import random
import time

# --- ESTÉTICA, UI E ANIMAÇÕES ---
st.set_page_config(page_title="Dark Castle: Definitive Edition", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    .stApp { background-color: #050505; font-family: 'VT323', monospace; color: #4af626; font-size: 20px; }
    
    /* Animação: Morte do Monstro */
    @keyframes monsterDeath {
        0% { transform: scale(1); opacity: 1; }
        100% { transform: scale(0) rotate(90deg); opacity: 0; }
    }
    .monster-die { animation: monsterDeath 1.5s forwards; text-align: center; font-size: 40px; color: red; }

    /* Animação: Explosão do Player */
    @keyframes explode {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.5); color: orange; }
        100% { transform: scale(0); opacity: 0; }
    }
    .player-explode { animation: explode 1s infinite; font-size: 50px; text-align: center; }

    .hero-panel { background: rgba(0, 255, 0, 0.05); border: 2px solid #4af626; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
    .stat-tag { color: #ffcc00; font-weight: bold; }
    .boss-sliced { color: #ff0000; font-weight: bold; letter-spacing: 5px; transform: skewX(-20deg); }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO SEGURA DO ESTADO ---
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

# --- TELA INICIAL ---
if not st.session_state.game_active:
    st.title("🏰 DARK CASTLE: ASCENSÃO")
    
    # Restauração das Informações Gerais
    with st.expander("📖 GUIA DO AVENTUREIRO (COMO JOGAR)", expanded=True):
        st.markdown("""
        - **Objetivo:** Explore os andares até o 5º nível para derrotar o Lorde.
        - **Progresso:** Derrote o número de monstros exigido para subir de andar.
        - **Combate:** No Andar 5, o Lorde adapta sua força (50%, 70% ou 90%) ao seu poder.
        - **Bolsa:** Equipe itens novos para aumentar seu ATK e DEF.
        """)
    
    st.subheader("Escolha sua classe para começar:")
    c1, c2 = st.columns(2)
    if c1.button("🛡️ GUERREIRO", use_container_width=True): start_game("Guerreiro")
    if c2.button("🔮 MAGO", use_container_width=True): start_game("Mago")

# --- TELAS DE FIM DE JOGO ---
elif st.session_state.game_state == 'player_dead':
    st.markdown("<div class='player-explode'>💥 EXPLODINDO 💥</div>", unsafe_allow_html=True)
    if st.session_state.enemy and "LORDE" in st.session_state.enemy.get('name', ''):
        st.markdown("<h2 style='color:red; text-align:center;'>HA HA HA! FRACO!</h2>", unsafe_allow_html=True)
    st.error("VOCÊ MORREU!")
    if st.button("Tentar Novamente"): st.session_state.clear(); st.rerun()

elif st.session_state.game_state == 'player_win':
    st.balloons()
    st.success("O LORDE FOI FATIADO! VOCÊ VENCEU O JOGO!")
    st.markdown("<h2 class='boss-sliced' style='text-align:center;'>// L // O // R // D // E //</h2>", unsafe_allow_html=True)
    if st.button("Jogar Novamente"): st.session_state.clear(); st.rerun()

# --- INTERFACE DE JOGO ATIVO ---
else:
    # HUD do Herói com trava de segurança para st.progress
    avatar = "🛡️" if st.session_state.hero_class == "Guerreiro" else "🔮"
    # Cálculo seguro da vida (entre 0.0 e 1.0) para evitar o erro da imagem 86b0ec
    safe_hp_ratio = max(0.0, min(1.0, st.session_state.hp / st.session_state.max_hp))
    
    st.markdown(f"""
    <div class="hero-panel">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="font-size: 50px;">{avatar}</div>
            <div style="flex-grow: 1;">
                <div><b>{st.session_state.hero_class.upper()}</b> | ANDAR {st.session_state.floor}</div>
                <div>HP: {max(0, st.session_state.hp)}/{st.session_state.max_hp} | 💰 {st.session_state.gold}G</div>
            </div>
        </div>
        <div style="margin-top: 10px; border-top: 1px solid #4af626; padding-top: 5px; font-size: 14px;">
            ⚔️ {st.session_state.weapon.get('name', '???')} (+{st.session_state.weapon.get('atk', 0)} ATK) | 
            🛡️ {st.session_state.armor.get('name', '???')} (+{st.session_state.armor.get('def', 0)} DEF)
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(safe_hp_ratio)

    # Lógica de Combate
    if st.session_state.enemy:
        enemy = st.session_state.enemy
        st.subheader(f"👹 {enemy.get('name', 'Inimigo')}")
        st.write(f"Vida Inimiga: {max(0, enemy.get('hp', 0))}")
        
        c1, c2 = st.columns(2)
        if c1.button("⚔️ ATACAR"):
            dmg = st.session_state.weapon.get('atk', 10) + random.randint(5, 12)
            enemy['hp'] -= dmg
            add_log(f"💥 Causou {dmg} de dano!")
            
            if enemy['hp'] <= 0:
                if "LORDE" in enemy.get('name', ''):
                    st.session_state.game_state = 'player_win'
                else:
                    st.session_state.gold += 50
                    st.session_state.kills_on_floor += 1
                    st.session_state.enemy = None
                    add_log("🏆 Vitória!")
                    if st.session_state.kills_on_floor >= FLOOR_GOALS.get(st.session_state.floor, 3):
                        st.session_state.floor += 1
                        st.session_state.kills_on_floor = 0
                st.rerun()
            else:
                edmg = max(2, enemy.get('atk', 15) - st.session_state.armor.get('def', 0))
                st.session_state.hp -= edmg
                if st.session_state.hp <= 0:
                    st.session_state.game_state = 'player_dead'
                st.rerun()

    # Exploração
    elif st.session_state.chest_found:
        st.title("🎁 BAÚ ENCONTRADO!")
        if st.button("Abrir Baú"):
            # Loot melhor no andar 4
            if st.session_state.floor == 4:
                item = {"name": "Espada de Plasma", "atk": 50, "type": "weapon"}
            else:
                item = {"name": "Poção", "type": "potion"}
            st.session_state.inventory.append(item)
            add_log(f"🎁 Recebeu {item['name']}!")
            st.session_state.chest_found = False
            st.rerun()
    
    else:
        st.title(f"🏰 SALA DE EXPLORAÇÃO")
        st.write(f"Derrote {FLOOR_GOALS.get(st.session_state.floor, 3) - st.session_state.kills_on_floor} inimigos para subir.")
        if st.button("👣 PROCURAR MONSTRO"):
            if st.session_state.floor == 5:
                # Spawn do Boss Adaptativo
                power = st.session_state.weapon.get('atk', 0) + st.session_state.armor.get('def', 0)
                if power < 30: hp, atk = 300, 20
                elif power < 60: hp, atk = 500, 35
                else: hp, atk = 800, 50
                st.session_state.enemy = {"name": "🔥 LORDE DAS SOMBRAS", "hp": hp, "atk": atk}
            else:
                roll = random.random()
                if roll < 0.7: 
                    st.session_state.enemy = {"name": "Monstro", "hp": 60 + st.session_state.floor*10, "atk": 15 + st.session_state.floor*2}
                else: 
                    st.session_state.chest_found = True
            st.rerun()

    st.write("---")
    # Histórico de log fixado
    for line in st.session_state.log[:3]:
        st.write(f"`{line}`")
