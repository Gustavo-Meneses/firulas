import streamlit as st
import random

# --- ESTÉTICA RETRO ---
st.set_page_config(page_title="Dark Castle: Loot & Mimics", page_icon="🏰", layout="centered")

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
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO SEGURA ---
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False, 'hero_class': "Viajante", 'level': 1, 'xp': 0,
        'hp': 100, 'max_hp': 100, 'mana': 50, 'gold': 0, 'log': ["O castelo te espera..."],
        'enemy': None, 'weapon': {"name": "Punhos", "atk": 5},
        'armor': {"name": "Roupas", "def": 0}, 'floor': 1, 'progress_floor': 0, 
        'in_shop': False, 'chest_found': False
    })

def add_log(msg):
    st.session_state.log.insert(0, msg)

def start_game(role):
    st.session_state.game_active = True
    st.session_state.hero_class = role
    if role == "Guerreiro":
        st.session_state.hp = st.session_state.max_hp = 150
        st.session_state.weapon = {"name": "Machado Inicial", "atk": 12}
    else:
        st.session_state.hp = st.session_state.max_hp = 90
        st.session_state.mana = 120
        st.session_state.weapon = {"name": "Cajado de Aprendiz", "atk": 8}

# --- LÓGICA DE BAÚS ---
def open_chest():
    st.session_state.chest_found = False
    luck = random.random()
    if luck < 0.6: # Loot
        gold_gain = random.randint(20, 60)
        st.session_state.gold += gold_gain
        add_log(f"🎁 O baú continha {gold_gain}G e uma erva medicinal! (+10 HP)")
        st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + 10)
    elif luck < 0.9: # Monstro (Trap)
        st.session_state.enemy = {"name": "Mimic (Baú Monstro)", "hp": 40, "atk": 15}
        add_log("⚠️ O BAÚ ERA UM MIMIC! PREPARE-SE!")
    else: # Vazio
        add_log("🕳️ O baú estava vazio e cheio de teias de aranha.")

# --- LÓGICA DE COMBATE ---
def combat_turn(action):
    enemy = st.session_state.enemy
    dmg = st.session_state.weapon['atk'] + random.randint(5, 15) if action == "attack" else (45 + st.session_state.level * 5 if st.session_state.mana >= 25 else 0)
    if action == "magic": st.session_state.mana -= 25 if st.session_state.mana >= 25 else 0
    
    enemy['hp'] -= dmg
    add_log(f"⚔️ Você causou {dmg} de dano!")

    if enemy['hp'] <= 0:
        gold_win = random.randint(20, 50) * st.session_state.floor
        st.session_state.gold += gold_win
        st.session_state.xp += 40
        add_log(f"🏆 Vitória! +{gold_win}G. Progresso: +1")
        st.session_state.progress_floor += 1
        st.session_state.enemy = None
        
        if st.session_state.progress_floor >= 3:
            st.session_state.floor += 1
            st.session_state.progress_floor = 0
            add_log(f"🔼 ANDAR {st.session_state.floor} ALCANÇADO!")
    else:
        mitigation = st.session_state.armor.get('def', 0)
        enemy_dmg = max(2, (enemy['atk'] + random.randint(0, 5)) - mitigation)
        st.session_state.hp -= enemy_dmg
        add_log(f"🩸 Dano recebido: {enemy_dmg}")
        if st.session_state.hp <= 0: st.session_state.hp = 0

# --- INTERFACE ---
with st.sidebar:
    st.header(f"💠 {st.session_state.hero_class} | Lvl {st.session_state.level}")
    hp_ratio = max(0.0, min(1.0, st.session_state.hp / st.session_state.max_hp))
    st.progress(hp_ratio)
    st.write(f"❤️ HP: {st.session_state.hp}/{st.session_state.max_hp} | 💰 {st.session_state.gold}G")
    st.write(f"🏰 Andar: {st.session_state.floor} | 🔋 Mana: {st.session_state.mana}")
    st.write("---")
    if st.button("💀 REINICIAR"):
        st.session_state.clear()
        st.rerun()

# TELA INICIAL COM TUTORIAL
if not st.session_state.game_active:
    st.title("🏰 DARK CASTLE: ASCENSÃO")
    
    with st.expander("📖 GUIA DO AVENTUREIRO (COMO JOGAR)", expanded=True):
        st.write("""
        - **Objetivo:** Explore o castelo até o 5º andar para enfrentar o Lorde das Sombras.
        - **Classes:** Guerreiros têm mais vida e ataque físico. Magos usam Mana para danos explosivos.
        - **Exploração:** Cada 'Explorar' pode gerar um Monstro, um Baú de Loot ou uma sala vazia.
        - **Andares:** Vença 3 combates para subir de andar. Inimigos ficam mais fortes a cada nível.
        - **Baús:** Podem conter ouro e cura, mas cuidado... alguns são monstros disfarçados!
        """)
    
    st.subheader("Escolha sua classe:")
    c1, c2 = st.columns(2)
    if c1.button("🛡️ GUERREIRO"): start_game("Guerreiro"); st.rerun()
    if c2.button("🔮 MAGO"): start_game("Mago"); st.rerun()

elif st.session_state.hp <= 0:
    st.title("💀 FIM DA JORNADA")
    st.write("Você pereceu nas profundezas do castelo.")
    if st.button("TENTAR NOVAMENTE"):
        st.session_state.clear()
        st.rerun()

elif st.session_state.in_shop:
    st.title("🛒 MERCADOR")
    c1, c2 = st.columns(2)
    if c1.button("🗡️ ESPADA MÉDIA (100G)"):
        if st.session_state.gold >= 100:
            st.session_state.gold -= 100
            st.session_state.weapon = {"name": "Espada Média", "atk": 25}
            add_log("🛒 Comprou Espada Média!")
        else: add_log("❌ Sem ouro!")
    if c2.button("🧪 POÇÃO (40G)"):
        if st.session_state.gold >= 40:
            st.session_state.gold -= 40
            st.session_state.hp = st.session_state.max_hp
            add_log("🧪 Vida restaurada!")
        else: add_log("❌ Sem ouro!")
    if st.button("🔙 SAIR"):
        st.session_state.in_shop = False
        st.rerun()

elif st.session_state.enemy:
    st.title(f"👹 COMBATE: {st.session_state.enemy['name']}")
    st.error(f"HP INIMIGO: {st.session_state.enemy['hp']}")
    c1, c2 = st.columns(2)
    if c1.button("⚔️ ATACAR"): combat_turn("attack"); st.rerun()
    if c2.button("🔥 MAGIA"): combat_turn("magic"); st.rerun()

elif st.session_state.chest_found:
    st.title("🎁 UM BAÚ FOI ENCONTRADO!")
    st.write("Deseja arriscar e abri-lo?")
    if st.button("🔓 ABRIR BAÚ"): open_chest(); st.rerun()
    if st.button("🏃 IGNORAR E SEGUIR"): st.session_state.chest_found = False; add_log("👣 Você decidiu não arriscar."); st.rerun()

else:
    st.title(f"🏰 ANDAR {st.session_state.floor}")
    st.write(f"Progresso: {st.session_state.progress_floor}/3")
    c1, c2 = st.columns(2)
    if c1.button("👣 EXPLORAR"):
        roll = random.random()
        if roll < 0.5: # Monstro
            monster_hp = 40 + (st.session_state.floor * 20)
            st.session_state.enemy = {"name": random.choice(["Orc", "Esqueleto"]), "hp": monster_hp, "atk": 10 + st.session_state.floor*5}
            add_log("❗ Monstro à frente!")
        elif roll < 0.8: # Baú
            st.session_state.chest_found = True
            add_log("🎁 Você encontrou um baú misterioso!")
        else:
            add_log("👣 Apenas um corredor vazio...")
        st.rerun()
    if c2.button("🛒 MERCADOR"):
        st.session_state.in_shop = True
        st.rerun()

st.write("---")
for line in st.session_state.log[:3]: st.write(f"`{line}`")
