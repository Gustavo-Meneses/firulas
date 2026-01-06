import streamlit as st
import random

# --- CONFIGURAÇÃO DA VIBE ---
st.set_page_config(page_title="Dark Castle: Market & Glory", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    .stApp { background-color: #050505; font-family: 'VT323', monospace; color: #4af626; font-size: 20px; }
    h1, h2, h3 { color: #4af626 !important; text-shadow: 0 0 10px #228d10; }
    .stButton>button {
        background-color: #111; color: #4af626; border: 2px solid #4af626;
        border-radius: 0px; font-family: 'VT323', monospace; width: 100%;
    }
    .stButton>button:hover { background-color: #4af626; color: #000; box-shadow: 0 0 15px #4af626; }
    .scanlines {
        position: fixed; left: 0; top: 0; width: 100vw; height: 100vh;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%);
        background-size: 100% 4px; pointer-events: none; z-index: 9999;
    }
</style>
<div class="scanlines"></div>
""", unsafe_allow_html=True)

# --- DATABASE DE ITENS ---
LOOT_TABLE = {
    "weapon": [
        {"name": "Adaga de Ferro", "atk": 5, "rarity": "Comum"},
        {"name": "Espada de Aço", "atk": 12, "rarity": "Raro"},
        {"name": "Machado Sangrento", "atk": 25, "rarity": "Épico"}
    ],
    "armor": [
        {"name": "Trapos Velhos", "def": 2, "rarity": "Comum"},
        {"name": "Cota de Malha", "def": 8, "rarity": "Raro"},
        {"name": "Armadura de Placas", "def": 20, "rarity": "Épico"}
    ]
}

# --- ENGINE DO JOGO (CORREÇÃO DE ATRIBUTOS) ---

# Inicialização segura de todos os estados
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False,
        'hero_class': "Viajante",
        'level': 1,
        'xp': 0,
        'hp': 100,
        'max_hp': 100,
        'mana': 50,
        'gold': 0,
        'log': ["Bem-vindo ao Dark Castle..."],
        'enemy': None,
        'weapon': {"name": "Punhos", "atk": 2}, # Garantindo que exista desde o início
        'armor': {"name": "Roupas Comuns", "def": 0},
        'in_shop': False
    })

def add_log(msg):
    st.session_state.log.insert(0, msg)

def start_game(role):
    st.session_state.game_active = True
    st.session_state.hero_class = role
    if role == "Guerreiro":
        st.session_state.hp = st.session_state.max_hp = 120
        st.session_state.weapon = {"name": "Espada Curta", "atk": 8}
    else:
        st.session_state.hp = st.session_state.max_hp = 80
        st.session_state.mana = 100
        st.session_state.weapon = {"name": "Cajado de Madeira", "atk": 4}

def combat_turn(action):
    enemy = st.session_state.enemy
    if action == "attack":
        dmg = st.session_state.weapon.get('atk', 2) + random.randint(5, 10)
        msg = f"💥 Dano causado: {dmg}"
    else:
        if st.session_state.mana >= 20:
            st.session_state.mana -= 20
            dmg = 35 + (st.session_state.level * 5)
            msg = f"🔮 Magia Arcana: {dmg}"
        else:
            dmg = 0
            msg = "❌ Sem Mana!"
    
    enemy['hp'] -= dmg
    add_log(msg)

    if enemy['hp'] <= 0:
        gold_gain = random.randint(15, 40)
        st.session_state.gold += gold_gain
        st.session_state.xp += 30
        add_log(f"🏆 Inimigo derrotado! +{gold_gain}G")
        st.session_state.enemy = None
    else:
        # Contra-ataque
        mitigation = st.session_state.armor.get('def', 0)
        dmg_taken = max(2, random.randint(10, 20) - mitigation)
        st.session_state.hp -= dmg_taken
        add_log(f"🩸 Dano recebido: {dmg_taken}")

# --- INTERFACE ---

# Sidebar (Agora segura contra AttributeErrors)
with st.sidebar:
    st.header(f"💠 {st.session_state.hero_class}")
    st.write(f"Nível: {st.session_state.level}")
    st.progress(min(1.0, st.session_state.hp / st.session_state.max_hp))
    st.write(f"❤️ HP: {st.session_state.hp} | 💰 Gold: {st.session_state.gold}")
    st.write("---")
    st.write(f"⚔️ **Arma:** {st.session_state.weapon['name']}")
    st.write(f"🛡️ **Defesa:** {st.session_state.armor['name']}")
    if st.button("♻️ Resetar"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# Conteúdo Principal
if not st.session_state.game_active:
    st.title("🏰 DARK CASTLE")
    st.write("Selecione sua classe:")
    c1, c2 = st.columns(2)
    if c1.button("🛡️ GUERREIRO"): start_game("Guerreiro"); st.rerun()
    if c2.button("🔮 MAGO"): start_game("Mago"); st.rerun()

elif st.session_state.in_shop:
    st.title("🛒 MERCADO DA VILA")
    st.write("Gaste suas moedas de ouro:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("--- EQUIPAMENTOS ---")
        if st.button("🗡️ Espada Longa (100G)"):
            if st.session_state.gold >= 100:
                st.session_state.gold -= 100
                st.session_state.weapon = {"name": "Espada Longa", "atk": 20}
                add_log("🛒 Comprou Espada Longa!")
            else: add_log("❌ Ouro insuficiente!")
            
    with col2:
        st.write("--- CONSUMÍVEIS ---")
        if st.button("🧪 Poção de Vida (30G)"):
            if st.session_state.gold >= 30:
                st.session_state.gold -= 30
                st.session_state.hp = st.session_state.max_hp
                add_log("🧪 Vida restaurada!")
            else: add_log("❌ Ouro insuficiente!")

    if st.button("🔙 SAIR DA LOJA"):
        st.session_state.in_shop = False
        st.rerun()

elif st.session_state.enemy:
    enemy = st.session_state.enemy
    st.subheader(f"👹 COMBATE: {enemy['name']}")
    st.code(f"HP: {enemy['hp']}")
    col1, col2 = st.columns(2)
    if col1.button("⚔️ ATACAR"): combat_turn("attack"); st.rerun()
    if col2.button("🔥 MAGIA"): combat_turn("magic"); st.rerun()

else:
    st.title("🌿 O CAMINHO")
    st.write("O que deseja fazer?")
    c1, c2 = st.columns(2)
    if c1.button("👣 EXPLORAR"):
        if random.random() < 0.6:
            st.session_state.enemy = {"name": "Goblin", "hp": 50}
            add_log("❗ Inimigo avistado!")
        else: add_log("👣 Caminhada tranquila...")
        st.rerun()
    if c2.button("🛒 IR À LOJA"):
        st.session_state.in_shop = True
        st.rerun()

st.write("---")
for line in st.session_state.log[:3]: st.write(f"`{line}`")
