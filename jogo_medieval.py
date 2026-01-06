import streamlit as st
import random

# --- ESTÉTICA E UI AVANÇADA ---
st.set_page_config(page_title="Dark Castle: Inventory Edition", page_icon="🏰", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    .stApp { background-color: #050505; font-family: 'VT323', monospace; color: #4af626; font-size: 20px; }
    
    /* HUD Fixa do Personagem */
    .char-hud {
        background: rgba(0, 255, 0, 0.1);
        border: 2px solid #4af626;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .gold-count { color: #ffd700; font-size: 24px; font-weight: bold; }
    
    .stButton>button {
        background-color: #111; color: #4af626; border: 2px solid #4af626;
        border-radius: 0px; font-family: 'VT323', monospace; width: 100%;
    }
    .stButton>button:hover { background-color: #4af626; color: #000; }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO ---
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False, 'hero_class': "Viajante", 'level': 1, 'xp': 0,
        'hp': 100, 'max_hp': 100, 'mana': 50, 'gold': 0, 'log': ["Inicie sua lenda..."],
        'enemy': None, 'weapon': {"name": "Adaga Velha", "atk": 8},
        'armor': {"name": "Trapos", "def": 2}, 'floor': 1, 'progress_floor': 0, 
        'in_shop': False, 'chest_found': False, 'inventory': []
    })

def add_log(msg):
    st.session_state.log.insert(0, msg)

def start_game(role):
    st.session_state.game_active = True
    st.session_state.hero_class = role
    if role == "Guerreiro":
        st.session_state.hp = st.session_state.max_hp = 150
        st.session_state.weapon = {"name": "Machado de Ferro", "atk": 15}
    else:
        st.session_state.hp = st.session_state.max_hp = 90
        st.session_state.mana = 120
        st.session_state.weapon = {"name": "Cajado Rúnico", "atk": 10}
    st.session_state.inventory.append(st.session_state.weapon['name'])

# --- SISTEMA DE LOOT & INVENTÁRIO ---
def open_chest():
    st.session_state.chest_found = False
    luck = random.random()
    if luck < 0.6:
        gold_gain = random.randint(30, 80)
        st.session_state.gold += gold_gain
        item_found = random.choice(["Poção de Mana", "Anel de Cobre", "Pingente Antigo"])
        st.session_state.inventory.append(item_found)
        add_log(f"🎁 Baú: +{gold_gain}G e encontrou [{item_found}]!")
    elif luck < 0.9:
        st.session_state.enemy = {"name": "Mimic faminto", "hp": 50, "atk": 18}
        add_log("⚠️ O BAÚ TINHA DENTES! É UM MIMIC!")
    else:
        add_log("🕳️ O baú se desfez em pó. Vazio.")

# --- LÓGICA DE COMBATE ---
def combat_turn(action):
    enemy = st.session_state.enemy
    dmg = st.session_state.weapon['atk'] + random.randint(5, 15) if action == "attack" else (50 + st.session_state.level * 5 if st.session_state.mana >= 25 else 0)
    if action == "magic": st.session_state.mana -= 25 if st.session_state.mana >= 25 else 0
    
    enemy['hp'] -= dmg
    add_log(f"⚔️ Causou {dmg} de dano!")

    if enemy['hp'] <= 0:
        gold_win = random.randint(25, 55) * st.session_state.floor
        st.session_state.gold += gold_win
        st.session_state.progress_floor += 1
        st.session_state.enemy = None
        add_log(f"🏆 Inimigo derrotado! +{gold_win}G")
    else:
        mitigation = st.session_state.armor.get('def', 0)
        enemy_dmg = max(2, (enemy['atk'] + random.randint(0, 5)) - mitigation)
        st.session_state.hp = max(0, st.session_state.hp - enemy_dmg)
        add_log(f"🩸 Dano recebido: {enemy_dmg}")

# --- UI PRINCIPAL ---

if not st.session_state.game_active:
    st.title("🏰 DARK CASTLE: ASCENSÃO")
    st.info("O objetivo é chegar ao 5º andar. Cuidado com sua vida!")
    c1, c2 = st.columns(2)
    if c1.button("🛡️ GUERREIRO"): start_game("Guerreiro"); st.rerun()
    if c2.button("🔮 MAGO"): start_game("Mago"); st.rerun()
else:
    # 1. BARRA DE VIDA E OURO (HUD)
    hp_percent = (st.session_state.hp / st.session_state.max_hp) * 100
    st.markdown(f"""
    <div class="char-hud">
        <div style="margin-bottom: 5px;">❤️ VIDA: {st.session_state.hp} / {st.session_state.max_hp}</div>
        <div style="background: #333; width: 100%; height: 15px; border: 1px solid #4af626;">
            <div style="background: #4af626; width: {hp_percent}%; height: 100%;"></div>
        </div>
        <div class="gold-count">💰 {st.session_state.gold} Moedas</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. ÍCONE DE BOLSA (INVENTÁRIO)
    with st.expander("🎒 VER BOLSA DE ITENS", expanded=False):
        if st.session_state.inventory:
            for item in set(st.session_state.inventory):
                count = st.session_state.inventory.count(item)
                st.write(f"• {item} (x{count})")
        else:
            st.write("Sua bolsa está vazia.")
        st.write(f"**Defesa Atual:** {st.session_state.armor['def']}")

    st.divider()

    # 3. ESTADOS DE JOGO
    if st.session_state.hp <= 0:
        st.error("💀 VOCÊ MORREU")
        if st.button("RECOMEÇAR"): st.session_state.clear(); st.rerun()

    elif st.session_state.in_shop:
        st.title("🛒 MERCADOR")
        c1, c2 = st.columns(2)
        if c1.button("🛡️ COTA DE MALHA (150G)"):
            if st.session_state.gold >= 150:
                st.session_state.gold -= 150
                st.session_state.armor = {"name": "Cota de Malha", "def": 12}
                st.session_state.inventory.append("Cota de Malha")
                add_log("🛒 Defesa aumentada!")
            else: add_log("❌ Ouro insuficiente!")
        if st.button("🔙 SAIR"): st.session_state.in_shop = False; st.rerun()

    elif st.session_state.enemy:
        st.subheader(f"👹 COMBATE: {st.session_state.enemy['name']}")
        st.progress(max(0, st.session_state.enemy['hp'])/100)
        c1, c2 = st.columns(2)
        if c1.button("⚔️ ATACAR"): combat_turn("attack"); st.rerun()
        if c2.button("🔥 MAGIA"): combat_turn("magic"); st.rerun()

    elif st.session_state.chest_found:
        st.title("🎁 BAÚ ENCONTRADO!")
        c1, c2 = st.columns(2)
        if c1.button("🔓 ABRIR"): open_chest(); st.rerun()
        if c2.button("👣 IGNORAR"): st.session_state.chest_found = False; st.rerun()

    else:
        st.title(f"🏰 ANDAR {st.session_state.floor}")
        c1, c2 = st.columns(2)
        if c1.button("👣 EXPLORAR"):
            roll = random.random()
            if roll < 0.5:
                st.session_state.enemy = {"name": "Zumbi de Elite", "hp": 60, "atk": 15}
            elif roll < 0.8:
                st.session_state.chest_found = True
            else:
                add_log("👣 Nada aqui além de sombras.")
            st.rerun()
        if c2.button("🛒 MERCADOR"): st.session_state.in_shop = True; st.rerun()

    # LOG
    st.divider()
    for line in st.session_state.log[:3]: st.write(f"`{line}`")
