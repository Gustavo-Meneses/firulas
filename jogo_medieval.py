import streamlit as st
import random

# --- CONFIGURAÇÃO DA VIBE (CSS & ESTÉTICA) ---
st.set_page_config(page_title="Dark Castle: Loot & Glory", page_icon="⚔️", layout="centered")

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

# --- ASSETS (ASCII) ---
ASCII_DRAGON = """
      _,   _
     /  `./ )
    |  _   / 
    |_| |_|
"""
ASCII_GOBLIN = " (0_0) <(GRRR!)"

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

# --- ENGINE DO JOGO ---

if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False, 'hero_class': None, 'level': 1, 'xp': 0,
        'hp': 100, 'max_hp': 100, 'mana': 50, 'gold': 0, 'log': [],
        'enemy': None, 'weapon': {"name": "Punhos", "atk": 2},
        'armor': {"name": "Roupas Comuns", "def": 0}
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

def roll_loot():
    if random.random() < 0.4: # 40% chance de cair loot
        tipo = random.choice(["weapon", "armor"])
        item = random.choice(LOOT_TABLE[tipo])
        add_log(f"💎 O inimigo deixou cair: {item['name']} ({item['rarity']})!")
        
        # Comparar e equipar automaticamente se for melhor (Lógica de Vibe Coding)
        if tipo == "weapon" and item['atk'] > st.session_state.weapon['atk']:
            st.session_state.weapon = item
            add_log("⚔️ Você equipou a arma nova!")
        elif tipo == "armor" and item.get('def', 0) > st.session_state.armor.get('def', 0):
            st.session_state.armor = item
            add_log("🛡️ Você equipou a armadura nova!")

def combat_turn(action):
    enemy = st.session_state.enemy
    # Dano do Jogador
    if action == "attack":
        dmg = st.session_state.weapon['atk'] + random.randint(5, 10)
        msg = f"💥 Você usou {st.session_state.weapon['name']} e causou {dmg} de dano!"
    else: # Magia
        if st.session_state.mana >= 20:
            st.session_state.mana -= 20
            dmg = 35 + (st.session_state.level * 5)
            msg = f"🔮 Magia Arcana causou {dmg} de dano!"
        else:
            dmg = 0
            msg = "❌ Sem mana! Você falhou no feitiço."
    
    enemy['hp'] -= dmg
    add_log(msg)

    if enemy['hp'] <= 0:
        gold_gain = random.randint(15, 40)
        xp_gain = 30
        st.session_state.gold += gold_gain
        st.session_state.xp += xp_gain
        add_log(f"🏆 Vitória! +{gold_gain}G e +{xp_gain}XP")
        roll_loot()
        st.session_state.enemy = None
        if st.session_state.xp >= st.session_state.level * 100:
            st.session_state.level += 1
            st.session_state.max_hp += 20
            st.session_state.hp = st.session_state.max_hp
            add_log(f"🆙 SUBIU DE NÍVEL: {st.session_state.level}!")
    else:
        # Dano do Inimigo (Reduzido pela Defesa)
        raw_enemy_dmg = random.randint(10, 20)
        mitigation = st.session_state.armor.get('def', 0)
        final_enemy_dmg = max(2, raw_enemy_dmg - mitigation)
        st.session_state.hp -= final_enemy_dmg
        add_log(f"🩸 O {enemy['name']} causou {final_enemy_dmg} de dano (Defesa bloqueou {mitigation}).")

# --- INTERFACE ---

if not st.session_state.game_active:
    st.title("🏰 DARK CASTLE 8-BIT")
    st.write("Selecione sua classe para iniciar o Vibe Coding...")
    c1, c2 = st.columns(2)
    if c1.button("🛡️ GUERREIRO"): start_game("Guerreiro") ; st.rerun()
    if c2.button("🔮 MAGO"): start_game("Mago") ; st.rerun()
else:
    # Sidebar Status
    with st.sidebar:
        st.header(f"Level {st.session_state.level} {st.session_state.hero_class}")
        st.metric("❤️ Vida", f"{st.session_state.hp}/{st.session_state.max_hp}")
        st.metric("💧 Mana", st.session_state.mana)
        st.metric("💰 Ouro", st.session_state.gold)
        st.write("---")
        st.write(f"⚔️ **Arma:** {st.session_state.weapon['name']} (+{st.session_state.weapon.get('atk')} ATK)")
        st.write(f"🛡️ **Corpo:** {st.session_state.armor['name']} (+{st.session_state.armor.get('def')} DEF)")
        if st.button("♻️ Reiniciar"): st.session_state.clear() ; st.rerun()

    # Área Principal
    if st.session_state.enemy:
        enemy = st.session_state.enemy
        st.subheader(f"COMBATE: {enemy['name']}")
        st.code(enemy['art'])
        st.progress(max(0, enemy['hp'])/100)
        
        col1, col2 = st.columns(2)
        if col1.button("⚔️ Atacar"): combat_turn("attack") ; st.rerun()
        if col2.button("🔥 Magia"): combat_turn("magic") ; st.rerun()
    else:
        st.subheader("Você explora os corredores úmidos...")
        if st.button("👣 Avançar"):
            if random.random() < 0.6:
                st.session_state.enemy = random.choice([
                    {"name": "Goblin", "hp": 50, "art": ASCII_GOBLIN},
                    {"name": "Dragão Pequeno", "hp": 100, "art": ASCII_DRAGON}
                ])
                add_log("❗ Um inimigo bloqueia seu caminho!")
            else:
                add_log("👣 O corredor parece seguro... por enquanto.")
            st.rerun()
        
        if st.button("🍺 Beber Poção (30G)"):
            if st.session_state.gold >= 30:
                st.session_state.gold -= 30
                st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + 40)
                add_log("🧪 Você recuperou 40 de Vida.")
                st.rerun()

    st.write("---")
    st.write("📜 **HISTÓRICO:**")
    for line in st.session_state.log[:5]:
        st.write(f"`{line}`")
