import streamlit as st
import random
import time

# --- CONFIGURAÇÃO VISUAL E ANIMAÇÕES ---
st.set_page_config(page_title="Dark Castle: Definitive Edition", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    .stApp { background-color: #050505; font-family: 'VT323', monospace; color: #4af626; font-size: 20px; }
    
    .hero-panel { 
        border: 2px solid #4af626; padding: 15px; border-radius: 10px; 
        background: rgba(0,255,0,0.05); margin-bottom: 10px;
    }
    .stat-tag { color: #ffcc00; font-weight: bold; }
    
    @keyframes explode { 0% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.5); color: orange; } 100% { transform: scale(0); opacity: 0; } }
    .player-explode { animation: explode 1s infinite; font-size: 50px; text-align: center; }
    
    .boss-sliced { color: #ff0000; font-weight: bold; letter-spacing: 5px; transform: skewX(-20deg); text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO DO JOGO ---
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False, 'hero_class': "Viajante", 'hp': 100, 'max_hp': 100, 
        'gold': 50, 'log': ["O castelo te espera..."], 'enemy': None,
        'weapon': {"name": "Punhal Velho", "atk": 8, "type": "weapon", "value": 10},
        'armor': {"name": "Trapos", "def": 2, "type": "armor", "value": 5},
        'floor': 1, 'kills': 0, 'inventory': [], 'state': 'playing'
    })

FLOOR_GOALS = {1: 3, 2: 4, 3: 5, 4: 2, 5: 1}

def add_log(msg):
    st.session_state.log.insert(0, f"[{time.strftime('%H:%M')}] {msg}")

def start_game(role):
    st.session_state.game_active = True
    st.session_state.hero_class = role
    if role == "Guerreiro":
        st.session_state.update({'hp': 150, 'max_hp': 150, 'weapon': {"name": "Machado de Ferro", "atk": 15, "type": "weapon", "value": 30}, 'armor': {"name": "Peitoral", "def": 5, "type": "armor", "value": 25}})
    else:
        st.session_state.update({'hp': 90, 'max_hp': 90, 'weapon': {"name": "Cajado Rúnico", "atk": 10, "type": "weapon", "value": 30}, 'armor': {"name": "Manto", "def": 3, "type": "armor", "value": 20}})
    st.rerun()

# --- TELAS DE ESTADO (MORTE/VITÓRIA) ---
if not st.session_state.game_active:
    st.title("🏰 DARK CASTLE: ASCENSÃO")
    with st.expander("📖 GUIA DO AVENTUREIRO", expanded=True):
        st.markdown("""
        - **Abates:** Derrote monstros para subir de andar.
        - **Mercado:** Agora você pode comprar novos equipamentos e vender o que não usa no Inventário.
        - **Chefão:** O Lorde das Sombras aguarda no Andar 5.
        """)
    st.subheader("Escolha sua classe:")
    c1, c2 = st.columns(2)
    if c1.button("🛡️ GUERREIRO"): start_game("Guerreiro")
    if c2.button("🔮 MAGO"): start_game("Mago")

elif st.session_state.state == 'player_dead':
    st.markdown("<div class='player-explode'>💥 EXPLODINDO 💥</div>", unsafe_allow_html=True)
    st.error("VOCÊ FOI DERROTADO!")
    if st.button("RECOMEÇAR"): st.session_state.clear(); st.rerun()

elif st.session_state.state == 'player_win':
    st.balloons()
    st.success("VITÓRIA LENDÁRIA!")
    st.markdown("<h2 class='boss-sliced'>// L // O // R // D // E // F // A // T // I // A // D // O //</h2>", unsafe_allow_html=True)
    if st.button("JOGAR NOVAMENTE"): st.session_state.clear(); st.rerun()

# --- INTERFACE DE JOGO ATIVO ---
else:
    # HUD: Painel do Herói
    avatar = "🛡️" if st.session_state.hero_class == "Guerreiro" else "🔮"
    safe_hp_ratio = max(0.0, min(1.0, st.session_state.hp / st.session_state.max_hp)) # Correção para erro de barra de progresso
    
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
            EQUIPADO: ⚔️ {st.session_state.weapon['name']} (+{st.session_state.weapon['atk']} ATK) | 
            🛡️ {st.session_state.armor['name']} (+{st.session_state.armor['def']} DEF)
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(safe_hp_ratio)

    # ABAS DO JOGO
    tab_fight, tab_inv, tab_shop = st.tabs(["⚔️ COMBATE", "🎒 INVENTÁRIO", "🛒 MERCADO"])

    with tab_fight:
        if st.session_state.enemy:
            en = st.session_state.enemy
            st.subheader(f"👹 {en['name']}")
            st.markdown(f"<div style='color:red;'>HP Inimigo: {max(0, en['hp'])}</div>", unsafe_allow_html=True)
            st.progress(max(0.0, min(1.0, en['hp'] / en['max_hp'])))
            
            c1, c2 = st.columns(2)
            if c1.button("⚔️ ATACAR"):
                dmg = st.session_state.weapon['atk'] + random.randint(5, 12)
                en['hp'] -= dmg
                add_log(f"Causou {dmg} de dano!")
                if en['hp'] <= 0:
                    if "LORDE" in en['name']: st.session_state.state = 'player_win'
                    else:
                        st.session_state.gold += 50
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
            st.write(f"Progresso: {st.session_state.kills} / {FLOOR_GOALS.get(st.session_state.floor, 3)} monstros")
            if st.button("👣 PROCURAR MONSTRO"):
                if st.session_state.floor == 5:
                    st.session_state.enemy = {"name": "🔥 LORDE DAS SOMBRAS", "hp": 500, "max_hp": 500, "atk": 40}
                else:
                    st.session_state.enemy = {"name": "Criatura", "hp": 60, "max_hp": 60, "atk": 15}
                st.rerun()

    with tab_inv:
        st.subheader("Itens na Bolsa")
        if not st.session_state.inventory:
            st.write("Seu inventário está vazio.")
        else:
            for idx, item in enumerate(st.session_state.inventory):
                c1, c2 = st.columns([3, 1])
                c1.write(f"• {item['name']} " + (f"(+{item['atk']} ATK)" if item['type'] == 'weapon' else f"(+{item['def']} DEF)"))
                if c2.button("Equipar", key=f"eq_{idx}"):
                    target = 'weapon' if item['type'] == 'weapon' else 'armor'
                    old = st.session_state[target]
                    st.session_state[target] = item
                    st.session_state.inventory[idx] = old
                    st.rerun()

    with tab_shop:
        col_buy, col_sell = st.columns(2)
        
        with col_buy:
            st.subheader("🛒 Comprar")
            shop_items = [
                {"name": "Espada de Aço", "atk": 35, "type": "weapon", "price": 120, "value": 60},
                {"name": "Manto Arcano", "def": 20, "type": "armor", "price": 100, "value": 50},
                {"name": "Poção", "type": "potion", "price": 40}
            ]
            for it in shop_items:
                if st.button(f"{it['name']} ({it['price']}G)"):
                    if st.session_state.gold >= it['price']:
                        if it['type'] == "potion":
                            st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + 50)
                            add_log("Curou 50 HP!")
                        else:
                            st.session_state.inventory.append(it)
                        st.session_state.gold -= it['price']
                        st.rerun()
                    else: st.error("Ouro insuficiente!")

        with col_sell:
            st.subheader("💰 Vender")
            if not st.session_state.inventory:
                st.write("Nada para vender.")
            else:
                for idx, item in enumerate(st.session_state.inventory):
                    sell_value = item.get('value', 20)
                    if st.button(f"Vender {item['name']} (+{sell_value}G)", key=f"sell_{idx}"):
                        st.session_state.gold += sell_value
                        st.session_state.inventory.pop(idx)
                        add_log(f"Vendeu {item['name']} por {sell_value}G.")
                        st.rerun()

    # LOG DE EVENTOS (Correção de erro de sintaxe)
    st.divider()
    for line in st.session_state.log[:3]:
        st.write(f"`{line}`")
