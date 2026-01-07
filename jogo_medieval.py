import streamlit as st
import random
import time

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Dark Castle: Ascensão", page_icon="🏰", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    .stApp { background-color: #050505; font-family: 'VT323', monospace; color: #4af626; font-size: 20px; }
    
    .hero-panel { 
        border: 2px solid #4af626; padding: 15px; border-radius: 10px; 
        background: rgba(0,255,0,0.05); margin-bottom: 10px;
    }
    
    .floor-badge {
        background-color: #ffcc00; color: black; padding: 5px 20px;
        border-radius: 20px; font-weight: bold; font-size: 26px;
        display: inline-block; margin-bottom: 15px; border: 2px solid #fff;
    }

    .rare-item { color: #00ffff !important; font-weight: bold; text-shadow: 0 0 10px #00ffff; }
    .berserk-alert { color: #ff4b4b; font-weight: bold; animation: blinker 0.8s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO DO JOGO ---
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False, 'hero_class': "Viajante", 'hp': 100, 'max_hp': 100, 
        'mana': 50, 'max_mana': 50, 'gold': 120, 'log': ["O castelo te espera..."], 'enemy': None,
        'weapon': {"name": "Punhal Velho", "atk": 8, "type": "weapon", "rarity": "comum", "value": 10},
        'armor': {"name": "Trapos", "def": 2, "type": "armor", "rarity": "comum", "value": 5},
        'floor': 1, 'kills': 0, 'inventory': [], 'state': 'playing',
        'market_stock': []
    })

def add_log(msg):
    st.session_state.log.insert(0, f"[{time.strftime('%H:%M')}] {msg}")

def start_game(role):
    stats = {
        "Guerreiro": {'hp': 160, 'mana': 30, 'atk': 15, 'def': 8, 'w': "Espada Curta"},
        "Mago": {'hp': 90, 'mana': 120, 'atk': 10, 'def': 3, 'w': "Cajado Aprendiz"},
        "Berserker": {'hp': 200, 'mana': 20, 'atk': 12, 'def': 4, 'w': "Machado Gasto"},
        "Assassino": {'hp': 110, 'mana': 50, 'atk': 18, 'def': 2, 'w': "Adagas Duplas"}
    }
    p = stats[role]
    st.session_state.update({
        'game_active': True, 'hero_class': role, 'hp': p['hp'], 'max_hp': p['hp'],
        'mana': p['mana'], 'max_mana': p['mana'],
        'weapon': {"name": p['w'], "atk": p['atk'], "type": "weapon", "rarity": "comum", "value": 30},
        'armor': {"name": "Armadura Inicial", "def": p['def'], "type": "armor", "rarity": "comum", "value": 20},
        'state': 'playing', 'floor': 1, 'kills': 0, 'inventory': [], 'market_stock': [], 'enemy': None
    })
    st.rerun()

# --- INTERFACE INICIAL ---
if not st.session_state.game_active:
    st.markdown("<h1 style='text-align: center;'>🏰 DARK CASTLE: ASCENSÃO</h1>", unsafe_allow_html=True)
    st.write("---")
    st.subheader("Selecione sua Classe:")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🛡️ GUERREIRO"): start_game("Guerreiro")
    if c2.button("🔮 MAGO"): start_game("Mago")
    if c3.button("🪓 BERSERKER"): start_game("Berserker")
    if c4.button("🗡️ ASSASSINO"): start_game("Assassino")

# --- LÓGICA DE JOGO ---
elif st.session_state.state == 'playing':
    # Indicador de Andar
    st.markdown(f"<div style='text-align: center;'><span class='floor-badge'>ANDAR {st.session_state.floor}</span></div>", unsafe_allow_html=True)

    # Painel de Status
    hp_ratio = st.session_state.hp / st.session_state.max_hp
    is_berserk = st.session_state.hero_class == "Berserker" and hp_ratio < 0.3
    rarity_class = "class='rare-item'" if st.session_state.weapon.get('rarity') == 'raro' else ""

    st.markdown(f"""
    <div class="hero-panel">
        <div style="display: flex; justify-content: space-between;">
            <span><b>{st.session_state.hero_class.upper()}</b></span>
            <span style="color:#ffd700;">💰 {st.session_state.gold}G</span>
        </div>
        <div style="margin: 10px 0;">
            ❤️ HP: {st.session_state.hp}/{st.session_state.max_hp} {f'<span class="berserk-alert"> [FÚRIA +90% ATK]</span>' if is_berserk else ''}<br>
            🧪 MANA: {st.session_state.mana}/{st.session_state.max_mana}
        </div>
        <div style="font-size: 15px; border-top: 1px dotted #4af626; padding-top: 5px;">
            EQUIPADO: <span {rarity_class}>{st.session_state.weapon['name']} (+{st.session_state.weapon['atk']} ATK)</span> | 
            <span>{st.session_state.armor['name']} (+{st.session_state.armor['def']} DEF)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_c, tab_i, tab_m = st.tabs(["⚔️ COMBATE", "🎒 MOCHILA", "🛒 MERCADO"])

    with tab_c:
        if st.session_state.enemy:
            en = st.session_state.enemy
            st.subheader(f"👹 {en['name']}")
            st.progress(max(0.0, en['hp']/en['max_hp']))
            
            col_at, col_mg = st.columns(2)
            
            # Botão Ataque Físico
            if col_at.button("⚔️ ATACAR"):
                dmg = st.session_state.weapon['atk'] + random.randint(5, 12)
                if is_berserk: dmg = int(dmg * 1.9) # Bônus Berserker
                
                stun = False
                if st.session_state.hero_class == "Assassino" and random.random() < 0.25:
                    stun = True
                    add_log("⚡ STUN! Inimigo atordoado!")

                en['hp'] -= dmg
                add_log(f"Causou {dmg} de dano!")

                if en['hp'] <= 0:
                    st.session_state.gold += 50 + (st.session_state.floor * 10)
                    st.session_state.kills += 1
                    st.session_state.enemy = None
                    if st.session_state.kills >= 3:
                        st.session_state.floor += 1
                        st.session_state.kills = 0
                    st.rerun()
                else:
                    # Defesa / Esquiva
                    if stun: pass
                    elif st.session_state.hero_class == "Assassino" and random.random() < 0.30:
                        add_log("💨 Esquivou do ataque!")
                    else:
                        edmg = max(2, en['atk'] - st.session_state.armor['def'])
                        st.session_state.hp -= edmg
                        if st.session_state.hp <= 0: st.session_state.state = 'player_dead'
                    st.rerun()

            # Botão Especial Mago
            if st.session_state.hero_class == "Mago":
                if col_mg.button("🔥 MAGIA (15 Mana)"):
                    if st.session_state.mana >= 15:
                        st.session_state.mana -= 15
                        m_dmg = st.session_state.weapon['atk'] + 25
                        if st.session_state.weapon.get('rarity') == 'raro':
                            m_dmg = int(m_dmg * 1.7) # Bônus Magia Rara
                            add_log("✨ MAGIA POTENCIALIZADA!")
                        en['hp'] -= m_dmg
                        add_log(f"Magia causou {m_dmg} de dano!")
                        if en['hp'] <= 0:
                            st.session_state.enemy = None; st.session_state.kills += 1; st.session_state.gold += 50
                        st.rerun()
                    else: st.warning("Sem mana!")

        else:
            if st.button("👣 EXPLORAR SALA"):
                # +20% chance de baú (Base 30% + 20% = 50%)
                if random.random() < 0.50:
                    gain = 40 + (st.session_state.floor * 15)
                    st.session_state.gold += gain
                    add_log(f"🎁 Achou um baú! +{gain}G")
                else:
                    st.session_state.enemy = {
                        "name": random.choice(["Ogro", "Sombra", "Cavaleiro Caído"]),
                        "hp": 60 + (st.session_state.floor * 20),
                        "max_hp": 60 + (st.session_state.floor * 20),
                        "atk": 12 + (st.session_state.floor * 4)
                    }
                st.rerun()

    with tab_i:
        if not st.session_state.inventory: st.write("Mochila vazia.")
        for i, item in enumerate(st.session_state.inventory):
            c1, c2 = st.columns([3, 1])
            info = f"{item['name']} (+{item.get('atk', item.get('def', 0))} {item['type'].upper()})"
            c1.write(info)
            if c2.button("Equipar", key=f"eq_{i}"):
                slot = item['type']
                old = st.session_state[slot]
                st.session_state[slot] = item
                st.session_state.inventory[i] = old
                st.rerun()

    with tab_m:
        col_b, col_s = st.columns(2)
        with col_b:
            st.subheader("🛒 Comprar")
            # Poções Fixas
            if st.button("❤️ Vida (40G) [+50 HP]"):
                if st.session_state.gold >= 40:
                    st.session_state.gold -= 40; st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + 50); st.rerun()
            if st.button("🧪 Mana (40G) [+40 Mana]"):
                if st.session_state.gold >= 40:
                    st.session_state.gold -= 40; st.session_state.mana = min(st.session_state.max_mana, st.session_state.mana + 40); st.rerun()
            
            st.divider()
            # Itens de Ataque e Defesa (50/50)
            if not st.session_state.market_stock:
                w_list = [{"name": "Espada Longa", "atk": 40, "price": 150, "type": "weapon", "rarity": "comum", "value": 70},
                          {"name": "Cajado de Cristal", "atk": 38, "price": 140, "type": "weapon", "rarity": "comum", "value": 65}]
                a_list = [{"name": "Armadura Pesada", "def": 25, "price": 140, "type": "armor", "rarity": "comum", "value": 65},
                          {"name": "Manto Arcano", "def": 18, "price": 120, "type": "armor", "rarity": "comum", "value": 55}]
                
                # Itens Raros (2%)
                if random.random() < 0.02:
                    w_list.append({"name": "EXCALIBUR", "atk": 120, "price": 500, "type": "weapon", "rarity": "raro", "value": 250})
                if random.random() < 0.02:
                    a_list.append({"name": "ÉGIDE DIVINA", "def": 80, "price": 500, "type": "armor", "rarity": "raro", "value": 250})
                
                st.session_state.market_stock = [random.choice(w_list), random.choice(a_list)]

            for i, it in enumerate(st.session_state.market_stock):
                label = f"⭐ {it['name']}" if it['rarity'] == 'raro' else it['name']
                attr = f"ATK: {it['atk']}" if it['type'] == 'weapon' else f"DEF: {it['def']}"
                if st.button(f"{label} ({attr}) - {it['price']}G", key=f"buy_{i}"):
                    if st.session_state.gold >= it['price']:
                        st.session_state.gold -= it['price']
                        st.session_state.inventory.append(it)
                        st.session_state.market_stock.pop(i) # Remove após compra
                        st.rerun()
            
            if st.button("🔄 Renovar Estoque (20G)"):
                if st.session_state.gold >= 20:
                    st.session_state.gold -= 20; st.session_state.market_stock = []; st.rerun()

        with col_s:
            st.subheader("💰 Vender")
            for i, inv_item in enumerate(st.session_state.inventory):
                if st.button(f"Vender {inv_item['name']} (+{inv_item['value']}G)", key=f"sell_{i}"):
                    st.session_state.gold += inv_item['value']
                    st.session_state.inventory.pop(i)
                    st.rerun()

    # Log inferior
    st.divider()
    for l in st.session_state.log[:3]: st.write(f"`{l}`")

elif st.session_state.state == 'player_dead':
    st.error("VOCÊ MORREU!")
    if st.button("RECOMEÇAR"): st.session_state.clear(); st.rerun()
