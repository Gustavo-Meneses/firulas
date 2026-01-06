import streamlit as st
import random
import time

# --- CONFIGURAÇÃO VISUAL E ANIMAÇÕES ---
st.set_page_config(page_title="Dark Castle: Definitive Edition", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    .stApp { background-color: #050505; font-family: 'VT323', monospace; color: #4af626; font-size: 20px; }
    
    /* Painel do Herói */
    .hero-panel { 
        border: 2px solid #4af626; padding: 15px; border-radius: 10px; 
        background: rgba(0,255,0,0.05); margin-bottom: 10px;
    }
    .stat-tag { color: #ffcc00; font-weight: bold; }
    
    /* Animação: Morte/Explosão */
    @keyframes explode { 0% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.5); color: orange; } 100% { transform: scale(0); opacity: 0; } }
    .player-explode { animation: explode 1s infinite; font-size: 50px; text-align: center; }
    
    /* Estilo Boss Fatiado */
    .boss-sliced { color: #ff0000; font-weight: bold; letter-spacing: 5px; transform: skewX(-20deg); text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO DO JOGO ---
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False, 'hero_class': "Viajante", 'hp': 100, 'max_hp': 100, 
        'mana': 50, 'gold': 50, 'log': ["O castelo te espera..."], 'enemy': None,
        'weapon': {"name": "Punhal Velho", "atk": 8, "type": "weapon"},
        'armor': {"name": "Trapos", "def": 2, "type": "armor"},
        'floor': 1, 'kills': 0, 'inventory': [], 'state': 'playing'
    })

FLOOR_GOALS = {1: 3, 2: 4, 3: 5, 4: 2, 5: 1}

def add_log(msg):
    st.session_state.log.insert(0, f"[{time.strftime('%H:%M')}] {msg}")

def start_game(role):
    st.session_state.game_active = True
    st.session_state.hero_class = role
    if role == "Guerreiro":
        st.session_state.update({'hp': 150, 'max_hp': 150, 'weapon': {"name": "Machado de Ferro", "atk": 15, "type": "weapon"}, 'armor': {"name": "Peitoral", "def": 5, "type": "armor"}})
    else:
        st.session_state.update({'hp': 90, 'max_hp': 90, 'mana': 120, 'weapon': {"name": "Cajado Rúnico", "atk": 10, "type": "weapon"}, 'armor': {"name": "Manto", "def": 3, "type": "armor"}})
    st.rerun()

# --- TELAS DE ESTADO (MORTE/VITÓRIA) ---
if not st.session_state.game_active:
    st.title("🏰 DARK CASTLE: ASCENSÃO")
    with st.expander("📖 GUIA DO AVENTUREIRO", expanded=True):
        st.markdown("""
        - **Abates:** Andar 1 (3), Andar 2 (4), Andar 3 (5), Andar 4 (2).
        - **Andar 4:** Loot maior e melhor garantido.
        - **Andar 5:** Chefe Adaptativo (Dificuldade baseada nos seus itens).
        - **Morte:** Se morrer, você explode! Se vencer, o Boss é fatiado.
        """)
    st.subheader("Escolha sua classe:")
    c1, c2 = st.columns(2)
    if c1.button("🛡️ GUERREIRO"): start_game("Guerreiro")
    if c2.button("🔮 MAGO"): start_game("Mago")

elif st.session_state.state == 'player_dead':
    st.markdown("<div class='player-explode'>💥 EXPLODINDO 💥</div>", unsafe_allow_html=True)
    if st.session_state.enemy and "LORDE" in st.session_state.enemy['name']:
        st.markdown("<h2 style='color:red; text-align:center;'>HA HA HA! FRACO!</h2>", unsafe_allow_html=True)
    st.error("VOCÊ FOI DERROTADO!")
    if st.button("RECOMEÇAR JORNADA"): st.session_state.clear(); st.rerun()

elif st.session_state.state == 'player_win':
    st.balloons()
    st.markdown("<div style='text-align:center; font-size:60px;'>🏆</div>", unsafe_allow_html=True)
    st.success("VITÓRIA LENDÁRIA!")
    st.markdown("<h2 class='boss-sliced'>// L // O // R // D // E // F // A // T // I // A // D // O //</h2>", unsafe_allow_html=True)
    if st.button("JOGAR NOVAMENTE"): st.session_state.clear(); st.rerun()

# --- INTERFACE DE JOGO ATIVO ---
else:
    # HUD: Painel do Herói (Sempre visível para saber o que está equipado)
    avatar = "🛡️" if st.session_state.hero_class == "Guerreiro" else "🔮"
    safe_hp_ratio = max(0.0, min(1.0, st.session_state.hp / st.session_state.max_hp))
    
    st.markdown(f"""
    <div class="hero-panel">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="font-size: 40px;">{avatar}</div>
            <div style="flex-grow: 1; margin-left: 20px;">
                <b>{st.session_state.hero_class.upper()}</b> | ANDAR {st.session_state.floor}<br>
                HP: {max(0, st.session_state.hp)}/{st.session_state.max_hp} | 💰 {st.session_state.gold}G
            </div>
        </div>
        <div style="margin-top: 10px; border-top: 1px solid #4af626; padding-top: 5px; font-size: 15px;">
            EQUIPADO: ⚔️ {st.session_state.weapon['name']} <span class='stat-tag'>(+{st.session_state.weapon['atk']} ATK)</span> | 
            🛡️ {st.session_state.armor['name']} <span class='stat-tag'>(+{st.session_state.armor['def']} DEF)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(safe_hp_ratio)

    # SISTEMA DE ABAS (Exploração, Inventário, Mercado)
    tab_fight, tab_inv, tab_shop = st.tabs(["⚔️ COMBATE", "🎒 INVENTÁRIO", "🛒 MERCADO"])

    with tab_fight:
        if st.session_state.enemy:
            en = st.session_state.enemy
            st.subheader(f"👹 {en['name']}")
            # Barra de vida do monstro
            mon_hp_ratio = max(0.0, min(1.0, en['hp'] / en['max_hp']))
            st.markdown(f"<div style='color:red; font-size:14px;'>Vida do Inimigo: {max(0, en['hp'])}</div>", unsafe_allow_html=True)
            st.progress(mon_hp_ratio)
            
            c1, c2 = st.columns(2)
            if c1.button("⚔️ ATACAR"):
                dmg = st.session_state.weapon['atk'] + random.randint(5, 12)
                en['hp'] -= dmg
                add_log(f"Você deu {dmg} de dano!")
                if en['hp'] <= 0:
                    if "LORDE" in en['name']: st.session_state.state = 'player_win'
                    else:
                        st.session_state.gold += 50
                        st.session_state.kills += 1
                        st.session_state.enemy = None
                        add_log("Monstro derrotado!")
                        if st.session_state.kills >= FLOOR_GOALS.get(st.session_state.floor, 3):
                            st.session_state.floor += 1
                            st.session_state.kills = 0
                            add_log(f"Subiu para o andar {st.session_state.floor}!")
                    st.rerun()
                else:
                    edmg = max(2, en['atk'] - st.session_state.armor['def'])
                    st.session_state.hp -= edmg
                    if st.session_state.hp <= 0: st.session_state.state = 'player_dead'
                    st.rerun()
        else:
            st.write(f"Inimigos neste andar: {st.session_state.kills} / {FLOOR_GOALS.get(st.session_state.floor, 3)}")
            if st.button("👣 PROCURAR MONSTRO"):
                if st.session_state.floor == 5:
                    # Chefe Adaptativo
                    pwr = st.session_state.weapon['atk'] + st.session_state.armor['def']
                    if pwr < 30: hp, atk = 300, 20
                    elif pwr < 60: hp, atk = 500, 35
                    else: hp, atk = 800, 55
                    st.session_state.enemy = {"name": "🔥 LORDE DAS SOMBRAS", "hp": hp, "max_hp": hp, "atk": atk}
                else:
                    st.session_state.enemy = {"name": "Criatura Trevosa", "hp": 60 + st.session_state.floor*10, "max_hp": 60 + st.session_state.floor*10, "atk": 15 + st.session_state.floor*2}
                st.rerun()

    with tab_inv:
        st.subheader("Sua Bolsa")
        if not st.session_state.inventory:
            st.write("Vazia.")
        for idx, item in enumerate(st.session_state.inventory):
            c1, c2 = st.columns([3, 1])
            c1.write(f"• {item['name']} (Valor: 20G)")
            if c2.button("Equipar", key=f"inv_{idx}"):
                target = 'weapon' if item['type'] == 'weapon' else 'armor'
                old = st.session_state[target]
                st.session_state[target] = item
                st.session_state.inventory[idx] = old
                st.rerun()

    with tab_shop:
        st.subheader("Mercador")
        shop_items = [
            {"name": "Espada de Aço", "atk": 35, "type": "weapon", "price": 120},
            {"name": "Manto Arcano", "def": 20, "type": "armor", "price": 100},
            {"name": "Poção de Vida", "type": "potion", "price": 40}
        ]
        for it in shop_items:
            if st.button(f"Comprar {it['name']} ({it['price']}G)"):
                if st.session_state.gold >= it['price']:
                    if it['type'] == "potion":
                        st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + 50)
                        add_log("Usou poção de cura!")
                    else:
                        st.session_state.inventory.append(it)
                    st.session_state.gold -= it['price']
                    st.rerun()
                else: st.error("Ouro insuficiente!")

    # LOG DE EVENTOS (RODAPÉ)
    st.divider()
    for line in st.session_state.log[:3]:
        st.write(f"`{line}`")
