import streamlit as st
import random
import time

# --- CONFIGURAÇÃO E ESTÉTICA ---
st.set_page_config(page_title="Dark Castle: Definitive", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    .stApp { background-color: #050505; font-family: 'VT323', monospace; color: #4af626; font-size: 20px; }
    .hero-panel { border: 2px solid #4af626; padding: 15px; border-radius: 10px; background: rgba(0,255,0,0.05); margin-bottom: 10px; }
    .rare-tag { color: #00ffff; font-weight: bold; text-shadow: 0 0 8px #00ffff; }
    .berserk-alert { color: #ff4b4b; font-weight: bold; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO SEGURA DO SISTEMA ---
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False, 'hero_class': "Viajante", 'hp': 100, 'max_hp': 100, 
        'gold': 100, 'log': ["O castelo te espera..."], 'enemy': None,
        'weapon': {"name": "Punhal Velho", "atk": 8, "type": "weapon", "rarity": "comum", "value": 10},
        'armor': {"name": "Trapos", "def": 2, "type": "armor", "rarity": "comum", "value": 5},
        'floor': 1, 'kills': 0, 'inventory': [], 'state': 'playing',
        'market_stock': []
    })

FLOOR_GOALS = {1: 3, 2: 4, 3: 5, 4: 2, 5: 1}

def add_log(msg):
    st.session_state.log.insert(0, f"[{time.strftime('%H:%M')}] {msg}")

def start_game(role):
    st.session_state.game_active = True
    st.session_state.hero_class = role
    stats = {
        "Guerreiro": {'hp': 160, 'max_hp': 160, 'atk': 15, 'def': 5, 'w_name': "Espada de Ferro", 'a_name': "Peitoral de Couro"},
        "Mago": {'hp': 90, 'max_hp': 90, 'atk': 10, 'def': 3, 'w_name': "Cajado de Madeira", 'a_name': "Túnica Leve"},
        "Berserker": {'hp': 200, 'max_hp': 200, 'atk': 12, 'def': 4, 'w_name': "Machado Pesado", 'a_name': "Pele de Urso"},
        "Assassino": {'hp': 110, 'max_hp': 110, 'atk': 18, 'def': 2, 'w_name': "Adagas Gêmeas", 'a_name': "Traje Sombrio"}
    }
    p = stats[role]
    st.session_state.update({
        'hp': p['hp'], 'max_hp': p['hp'],
        'weapon': {"name": p['w_name'], "atk": p['atk'], "type": "weapon", "rarity": "comum", "value": 30},
        'armor': {"name": p['a_name'], "def": p['def'], "type": "armor", "rarity": "comum", "value": 20}
    })
    st.rerun()

# --- TELAS DE ESTADO ---
if not st.session_state.game_active:
    st.title("🏰 DARK CASTLE: ASCENSÃO")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🛡️ GUERREIRO"): start_game("Guerreiro")
    if c2.button("🔮 MAGO"): start_game("Mago")
    if c3.button("🪓 BERSERKER"): start_game("Berserker")
    if c4.button("🗡️ ASSASSINO"): start_game("Assassino")
elif st.session_state.state == 'player_dead':
    st.error("VOCÊ MORREU!")
    if st.button("RECOMEÇAR"): st.session_state.clear(); st.rerun()
else:
    # HUD
    hp_ratio = max(0.0, min(1.0, st.session_state.hp / st.session_state.max_hp))
    is_berserk = st.session_state.hero_class == "Berserker" and hp_ratio < 0.3
    
    st.markdown(f"""
    <div class="hero-panel">
        <div style="display: flex; justify-content: space-between;">
            <b>{st.session_state.hero_class.upper()}</b>
            <span style="color:#ffd700;">💰 {st.session_state.gold}G</span>
        </div>
        <div>❤️ HP: {max(0, st.session_state.hp)}/{st.session_state.max_hp} {f'<span class="berserk-alert">(FÚRIA!)</span>' if is_berserk else ''}</div>
        <div style="font-size: 14px;">⚔️ {st.session_state.weapon['name']} (+{st.session_state.weapon['atk']} ATK) | 🛡️ {st.session_state.armor['name']} (+{st.session_state.armor['def']} DEF)</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(hp_ratio)

    tab_fight, tab_inv, tab_shop = st.tabs(["⚔️ COMBATE", "🎒 INVENTÁRIO", "🛒 MERCADO"])

    with tab_fight:
        if st.session_state.enemy:
            en = st.session_state.enemy
            st.write(f"👹 {en['name']} | HP: {max(0, en['hp'])}")
            if st.button("⚔️ ATACAR"):
                dmg = st.session_state.weapon['atk'] + random.randint(5, 10)
                if is_berserk: dmg = int(dmg * 1.9)
                en['hp'] -= dmg
                if en['hp'] <= 0:
                    st.session_state.gold += 50; st.session_state.enemy = None; st.session_state.kills += 1
                else:
                    st.session_state.hp -= max(2, en['atk'] - st.session_state.armor['def'])
                    if st.session_state.hp <= 0: st.session_state.state = 'player_dead'
                st.rerun()
        else:
            if st.button("👣 EXPLORAR"):
                if random.random() < 0.5: st.session_state.gold += 40; add_log("🎁 +40G")
                else: st.session_state.enemy = {"name": "Slug", "hp": 60, "max_hp": 60, "atk": 15}
                st.rerun()

    with tab_inv:
        for idx, item in enumerate(st.session_state.inventory):
            c1, c2 = st.columns([3, 1])
            attr = f"+{item['atk']} ATK" if item['type'] == 'weapon' else f"+{item['def']} DEF"
            c1.write(f"{item['name']} ({attr})")
            if c2.button("Equipar", key=f"inv_{idx}"):
                slot = 'weapon' if item['type'] == 'weapon' else 'armor'
                old = st.session_state[slot]
                st.session_state[slot] = item
                st.session_state.inventory[idx] = old
                st.rerun()

    with tab_shop:
        # LÓGICA DE MERCADO: 50% Ataque / 50% Defesa
        if not st.session_state.market_stock:
            weapons_pool = [
                {"name": "Espada de Aço", "atk": 35, "price": 100, "type": "weapon", "rarity": "comum", "value": 50},
                {"name": "Cajado Rúnico", "atk": 40, "price": 120, "type": "weapon", "rarity": "comum", "value": 60}
            ]
            armors_pool = [
                {"name": "Cota de Malha", "def": 15, "price": 90, "type": "armor", "rarity": "comum", "value": 45},
                {"name": "Peitoral de Ferro", "def": 25, "price": 150, "type": "armor", "rarity": "comum", "value": 75}
            ]
            # 2% de Chance para Itens Raros
            if random.random() < 0.02:
                weapons_pool.append({"name": "EXCALIBUR", "atk": 120, "price": 400, "type": "weapon", "rarity": "raro", "value": 200})
            if random.random() < 0.02:
                armors_pool.append({"name": "ESCUDO DIVINO", "def": 100, "price": 400, "type": "armor", "rarity": "raro", "value": 200})
            
            # Garante um de cada tipo (50/50 de slots no mercado)
            st.session_state.market_stock = [random.choice(weapons_pool), random.choice(armors_pool)]

        st.subheader("🛒 Mercado (Itens de Ataque e Defesa)")
        for i, it in enumerate(st.session_state.market_stock):
            # Exibição clara do quanto cada item dá de atributo
            attr_val = f"⚔️ +{it['atk']} ATK" if it['type'] == 'weapon' else f"🛡️ +{it['def']} DEF"
            rarity_label = "⭐ " if it['rarity'] == 'raro' else ""
            
            if st.button(f"Comprar {rarity_label}{it['name']} [{attr_val}] — {it['price']}G", key=f"buy_{i}"):
                if st.session_state.gold >= it['price']:
                    st.session_state.gold -= it['price']
                    st.session_state.inventory.append(it)
                    st.session_state.market_stock.pop(i)
                    st.rerun()
                else: st.error("Ouro insuficiente!")
        
        if st.button("🔄 Renovar Estoque (20G)"):
            if st.session_state.gold >= 20:
                st.session_state.gold -= 20; st.session_state.market_stock = []; st.rerun()

    st.divider()
    for line in st.session_state.log[:3]: st.write(f"`{line}`")
