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
    .floor-indicator { font-size: 28px; color: #ffcc00; text-align: center; font-weight: bold; margin-bottom: 10px; border: 1px solid #ffcc00; border-radius: 5px; }
    .rare-tag { color: #00ffff; font-weight: bold; text-shadow: 0 0 8px #00ffff; }
    .berserk-alert { color: #ff4b4b; font-weight: bold; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO SEGURA DO SISTEMA ---
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False, 'hero_class': "Viajante", 'hp': 100, 'max_hp': 100, 
        'mana': 50, 'max_mana': 50, 'gold': 120, 'log': ["O castelo te espera..."], 'enemy': None,
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
        "Guerreiro": {'hp': 160, 'mana': 30, 'atk': 15, 'def': 5, 'w_name': "Espada de Ferro", 'a_name': "Peitoral de Couro"},
        "Mago": {'hp': 90, 'mana': 100, 'atk': 10, 'def': 3, 'w_name': "Cajado de Madeira", 'a_name': "Túnica Leve"},
        "Berserker": {'hp': 200, 'mana': 20, 'atk': 12, 'def': 4, 'w_name': "Machado Pesado", 'a_name': "Pele de Urso"},
        "Assassino": {'hp': 110, 'mana': 40, 'atk': 18, 'def': 2, 'w_name': "Adagas Gêmeas", 'a_name': "Traje Sombrio"}
    }
    p = stats[role]
    st.session_state.update({
        'hp': p['hp'], 'max_hp': p['hp'], 'mana': p['mana'], 'max_mana': p['mana'],
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
    # INDICADOR DE ANDAR (Visualização de Nível Ajustada)
    st.markdown(f"<div class='floor-indicator'>📍 ANDAR {st.session_state.floor}</div>", unsafe_allow_html=True)

    # HUD
    hp_ratio = max(0.0, min(1.0, st.session_state.hp / st.session_state.max_hp))
    mana_ratio = max(0.0, min(1.0, st.session_state.mana / st.session_state.max_mana))
    is_berserk = st.session_state.hero_class == "Berserker" and hp_ratio < 0.3
    
    st.markdown(f"""
    <div class="hero-panel">
        <div style="display: flex; justify-content: space-between;">
            <b>{st.session_state.hero_class.upper()}</b>
            <span style="color:#ffd700;">💰 {st.session_state.gold}G</span>
        </div>
        <div>❤️ HP: {max(0, st.session_state.hp)}/{st.session_state.max_hp} {f'<span class="berserk-alert">(FÚRIA!)</span>' if is_berserk else ''}</div>
        <div>🧪 MANA: {max(0, st.session_state.mana)}/{st.session_state.max_mana}</div>
        <div style="font-size: 14px; border-top: 1px solid #4af626; margin-top: 5px; padding-top: 5px;">
            ⚔️ {st.session_state.weapon['name']} (+{st.session_state.weapon['atk']} ATK) | 🛡️ {st.session_state.armor['name']} (+{st.session_state.armor['def']} DEF)
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(hp_ratio, text="Vida")
    st.progress(mana_ratio, text="Mana")

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
                    if st.session_state.kills >= FLOOR_GOALS.get(st.session_state.floor, 3):
                        st.session_state.floor += 1; st.session_state.kills = 0
                else:
                    st.session_state.hp -= max(2, en['atk'] - st.session_state.armor['def'])
                    if st.session_state.hp <= 0: st.session_state.state = 'player_dead'
                st.rerun()
        else:
            st.write(f"Inimigos para o próximo andar: {st.session_state.kills}/{FLOOR_GOALS.get(st.session_state.floor, 3)}")
            if st.button("👣 EXPLORAR"):
                if random.random() < 0.5: 
                    st.session_state.gold += 40
                    add_log("🎁 Encontrou ouro escondido! +40G")
                else: 
                    st.session_state.enemy = {"name": f"Guarda do Andar {st.session_state.floor}", "hp": 50 + (st.session_state.floor * 15), "max_hp": 50 + (st.session_state.floor * 15), "atk": 10 + (st.session_state.floor * 5)}
                st.rerun()

    with tab_inv:
        st.subheader("Itens na Mochila")
        if not st.session_state.inventory: st.write("Vazia.")
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
        col_buy, col_sell = st.columns(2)
        
        with col_buy:
            st.subheader("🛒 Comprar")
            # Estoque de Poções (Sempre disponíveis)
            if st.button("❤️ Poção de Vida (40G) [+50 HP]"):
                if st.session_state.gold >= 40:
                    st.session_state.gold -= 40
                    st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + 50)
                    add_log("❤️ Usou Poção de Vida!")
                    st.rerun()
                else: st.error("Ouro insuficiente!")

            if st.button("🧪 Poção de Mana (40G) [+30 Mana]"):
                if st.session_state.gold >= 40:
                    st.session_state.gold -= 40
                    st.session_state.mana = min(st.session_state.max_mana, st.session_state.mana + 30)
                    add_log("🧪 Usou Poção de Mana!")
                    st.rerun()
                else: st.error("Ouro insuficiente!")

            st.divider()
            
            # Estoque de Equipamentos (50% Ataque / 50% Defesa)
            if not st.session_state.market_stock:
                w_pool = [{"name": "Lança de Aço", "atk": 45, "price": 150, "type": "weapon", "rarity": "comum", "value": 75},
                          {"name": "Cajado de Cristal", "atk": 50, "price": 180, "type": "weapon", "rarity": "comum", "value": 90}]
                a_pool = [{"name": "Armadura de Placas", "def": 30, "price": 160, "type": "armor", "rarity": "comum", "value": 80},
                          {"name": "Manto de Proteção", "def": 20, "price": 130, "type": "armor", "rarity": "comum", "value": 65}]
                
                # Chance Rara 2%
                if random.random() < 0.02:
                    w_pool.append({"name": "DESTRUIDORA", "atk": 150, "price": 500, "type": "weapon", "rarity": "raro", "value": 250})
                
                st.session_state.market_stock = [random.choice(w_pool), random.choice(a_pool)]

            for i, it in enumerate(st.session_state.market_stock):
                attr_val = f"⚔️ +{it['atk']} ATK" if it['type'] == 'weapon' else f"🛡️ +{it['def']} DEF"
                if st.button(f"{it['name']} ({attr_val}) — {it['price']}G", key=f"buy_eq_{i}"):
                    if st.session_state.gold >= it['price']:
                        st.session_state.gold -= it['price']
                        st.session_state.inventory.append(it)
                        st.session_state.market_stock.pop(i)
                        st.rerun()
            
            if st.button("🔄 Renovar Equipamentos (20G)"):
                if st.session_state.gold >= 20:
                    st.session_state.gold -= 20; st.session_state.market_stock = []; st.rerun()

        with col_sell:
            st.subheader("💰 Vender Itens")
            if not st.session_state.inventory:
                st.write("Nada para vender no momento.")
            for i, item in enumerate(st.session_state.inventory):
                val = item.get('value', 20)
                if st.button(f"Vender {item['name']} (+{val}G)", key=f"sell_tab_{i}"):
                    st.session_state.gold += val
                    st.session_state.inventory.pop(i)
                    add_log(f"💰 Vendeu {item['name']} por {val}G")
                    st.rerun()

    st.divider()
    for line in st.session_state.log[:3]: st.write(f"`{line}`")
