import streamlit as st
import random
import time

# --- CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Dark Castle: Definitive", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    .stApp { background-color: #050505; font-family: 'VT323', monospace; color: #4af626; font-size: 20px; }
    .hero-panel { border: 2px solid #4af626; padding: 15px; border-radius: 10px; margin-bottom: 10px; background: rgba(0,255,0,0.05); }
    .stat-tag { color: #ffcc00; font-weight: bold; }
    .monster-bar { color: #ff4b4b; font-weight: bold; text-align: center; margin-bottom: 5px; }
    /* Animações */
    @keyframes monsterDeath { 0% {transform: scale(1);} 100% {transform: scale(0); opacity:0;} }
    .m-die { animation: monsterDeath 1s forwards; color: red; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO ---
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False, 'hero_class': "Viajante", 'hp': 100, 'max_hp': 100, 
        'mana': 50, 'gold': 50, 'log': ["Bem-vindo ao castelo..."], 'enemy': None,
        'weapon': {"name": "Adaga", "atk": 8, "type": "weapon"},
        'armor': {"name": "Trapos", "def": 2, "type": "armor"},
        'floor': 1, 'kills': 0, 'inventory': [], 'state': 'playing'
    })

FLOOR_GOALS = {1: 3, 2: 4, 3: 5, 4: 2, 5: 1}

def add_log(msg):
    st.session_state.log.insert(0, msg)

def start_game(role):
    st.session_state.game_active = True
    st.session_state.hero_class = role
    if role == "Guerreiro":
        st.session_state.update({'hp': 150, 'max_hp': 150, 'weapon': {"name": "Machado", "atk": 15, "type": "weapon"}})
    else:
        st.session_state.update({'hp': 90, 'max_hp': 90, 'mana': 120, 'weapon': {"name": "Cajado", "atk": 10, "type": "weapon"}})
    st.rerun()

# --- TELAS DE ESTADO ---
if not st.session_state.game_active:
    st.title("🏰 DARK CASTLE: ASCENSÃO")
    with st.expander("📖 GUIA DO AVENTUREIRO", expanded=True):
        st.write("Derrote monstros para subir andares. No Andar 5, o Boss final espera.")
    c1, c2 = st.columns(2)
    if c1.button("🛡️ GUERREIRO"): start_game("Guerreiro")
    if c2.button("🔮 MAGO"): start_game("Mago")

elif st.session_state.state == 'player_dead':
    st.markdown("<h1 style='color:red; text-align:center;'>💥 VOCÊ EXPLODIU! 💥</h1>", unsafe_allow_html=True)
    if st.button("RECOMEÇAR"): st.session_state.clear(); st.rerun()

elif st.session_state.state == 'player_win':
    st.balloons()
    st.success("O LORDE FOI FATIADO!")
    if st.button("JOGAR NOVAMENTE"): st.session_state.clear(); st.rerun()

# --- JOGO ATIVO ---
else:
    # 1. PAINEL DO HERÓI
    avatar = "🛡️" if st.session_state.hero_class == "Guerreiro" else "🔮"
    safe_hp = max(0.0, min(1.0, st.session_state.hp / st.session_state.max_hp))
    
    st.markdown(f"""
    <div class="hero-panel">
        <div style="display: flex; justify-content: space-between;">
            <span>{avatar} <b>{st.session_state.hero_class.upper()}</b> | ANDAR {st.session_state.floor}</span>
            <span style="color:#ffd700;">💰 {st.session_state.gold}G</span>
        </div>
        <div style="font-size: 15px; margin-top:5px;">
            ❤️ HP: {max(0, st.session_state.hp)}/{st.session_state.max_hp} | 
            ⚔️ {st.session_state.weapon['name']} (+{st.session_state.weapon['atk']}) | 
            🛡️ {st.session_state.armor['name']} (+{st.session_state.armor['def']})
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(safe_hp)

    # 2. ABAS DE SISTEMA (MERCADO E INVENTÁRIO)
    tab_exp, tab_inv, tab_shop = st.tabs(["👣 EXPLORAÇÃO", "🎒 INVENTÁRIO", "🛒 MERCADO"])

    with tab_exp:
        if st.session_state.enemy:
            en = st.session_state.enemy
            st.markdown(f"<div class='monster-bar'>👹 {en['name']} | HP: {max(0, en['hp'])}</div>", unsafe_allow_html=True)
            st.progress(max(0.0, min(1.0, en['hp'] / en['max_hp'])))
            
            c1, c2 = st.columns(2)
            if c1.button("⚔️ ATACAR"):
                dmg = st.session_state.weapon['atk'] + random.randint(5, 12)
                en['hp'] -= dmg
                add_log(f"Causou {dmg} de dano!")
                if en['hp'] <= 0:
                    if "LORDE" in en['name']: st.session_state.state = 'player_win'
                    else:
                        st.session_state.gold += 40
                        st.session_state.kills += 1
                        st.session_state.enemy = None
                        if st.session_state.kills >= FLOOR_GOALS.get(st.session_state.floor, 3):
                            st.session_state.floor += 1; st.session_state.kills = 0
                    st.rerun()
                else:
                    edmg = max(2, en['atk'] - st.session_state.armor['def'])
                    st.session_state.hp -= edmg
                    if st.session_state.hp <= 0: st.session_state.state = 'player_dead'
                    st.rerun()
        else:
            st.write(f"Abates necessários: {st.session_state.kills}/{FLOOR_GOALS.get(st.session_state.floor, 3)}")
            if st.button("👣 PROCURAR PERIGO"):
                if st.session_state.floor == 5:
                    st.session_state.enemy = {"name": "LORDE DAS SOMBRAS", "hp": 500, "max_hp": 500, "atk": 40}
                else:
                    st.session_state.enemy = {"name": "Zumbi", "hp": 60, "max_hp": 60, "atk": 15}
                st.rerun()

    with tab_inv:
        if not st.session_state.inventory:
            st.write("Bolsa vazia.")
        for idx, item in enumerate(st.session_state.inventory):
            col1, col2 = st.columns([3, 1])
            col1.write(f"• {item['name']} " + (f"(+{item['atk']} ATK)" if 'atk' in item else f"(+{item['def']} DEF)" if 'def' in item else ""))
            if col2.button("Equipar", key=f"inv_{idx}"):
                target = 'weapon' if item['type'] == 'weapon' else 'armor'
                old = st.session_state[target]
                st.session_state[target] = item
                st.session_state.inventory[idx] = old
                st.rerun()

    with tab_shop:
        st.subheader("Itens do Dia")
        items = [
            {"name": "Espada Longa", "atk": 30, "type": "weapon", "price": 100},
            {"name": "Escudo de Aço", "def": 15, "type": "armor", "price": 80}
        ]
        for it in items:
            if st.button(f"🛒 {it['name']} ({it['price']}G)"):
                if st.session_state.gold >= it['price']:
                    st.session_state.gold -= it['price']
                    st.session_state.inventory.append(it)
                    add_log(f"Comprou {it['name']}!")
                    st.rerun()
                else: st.error("Ouro insuficiente!")

    # 3. HISTÓRICO
    st.divider()
    for line in st.session_state.log[:3]:
        st.write(f"`{line}`")
