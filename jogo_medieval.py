import streamlit as st
import random
import time

# --- CONFIGURAÇÃO E DESIGN ---
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

    .instruction-box {
        background: rgba(255, 255, 255, 0.05); border-left: 5px solid #4af626;
        padding: 15px; margin: 10px 0; font-size: 18px; color: #fff;
    }

    .rare-item { color: #00ffff !important; font-weight: bold; text-shadow: 0 0 10px #00ffff; }
    .berserk-alert { color: #ff4b4b; font-weight: bold; animation: blinker 0.8s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO ---
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

# --- TELA INICIAL COM INFORMAÇÕES DE JOGO ---
if not st.session_state.game_active:
    st.markdown("<h1 style='text-align: center;'>🏰 DARK CASTLE: ASCENSÃO</h1>", unsafe_allow_html=True)
    
    with st.expander("📜 COMO JOGAR & CLASSES (LEIA ANTES DE COMEÇAR)", expanded=True):
        st.markdown("""
        <div class="instruction-box">
            <b>🎯 Objetivo:</b> Explore o castelo, derrote inimigos para subir de andar e gerencie seu ouro no mercado.<br><br>
            <b>🛡️ Guerreiro:</b> Alta defesa e vida. Ideal para iniciantes.<br>
            <b>🔮 Mago:</b> Usa Mana para magias poderosas. Itens <span style='color:#00ffff'>RAROS</span> aumentam o dano mágico em 70%.<br>
            <b>🪓 Berserker:</b> Quando sua vida está abaixo de 30%, você entra em <b>FÚRIA</b> (+90% de dano).<br>
            <b>🗡️ Assassino:</b> Possui 30% de chance de esquiva e 25% de chance de atordoar (Stun) o inimigo.<br><br>
            <b>💰 Mercado:</b> Itens de ataque e defesa são repostos automaticamente. Você também pode vender itens da mochila.
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Selecione sua linhagem:")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🛡️ GUERREIRO"): start_game("Guerreiro")
    if c2.button("🔮 MAGO"): start_game("Mago")
    if c3.button("🪓 BERSERKER"): start_game("Berserker")
    if c4.button("🗡️ ASSASSINO"): start_game("Assassino")

# --- TELA DE JOGO ---
elif st.session_state.state == 'playing':
    st.markdown(f"<div style='text-align: center;'><span class='floor-badge'>ANDAR {st.session_state.floor}</span></div>", unsafe_allow_html=True)

    # Status do Jogador
    hp_pct = st.session_state.hp / st.session_state.max_hp
    is_fury = st.session_state.hero_class == "Berserker" and hp_pct < 0.3
    rarity_style = "class='rare-item'" if st.session_state.weapon.get('rarity') == 'raro' else ""

    st.markdown(f"""
    <div class="hero-panel">
        <div style="display: flex; justify-content: space-between;">
            <span><b>{st.session_state.hero_class.upper()}</b></span>
            <span style="color:#ffd700;">💰 {st.session_state.gold}G</span>
        </div>
        <div style="margin: 10px 0;">
            ❤️ HP: {st.session_state.hp}/{st.session_state.max_hp} {f'<span class="berserk-alert"> [FÚRIA ATIVA]</span>' if is_fury else ''}<br>
            🧪 MANA: {st.session_state.mana}/{st.session_state.max_mana}
        </div>
        <div style="font-size: 15px; border-top: 1px dotted #4af626; padding-top: 5px;">
            ⚔️ <span {rarity_style}>{st.session_state.weapon['name']} (+{st.session_state.weapon['atk']} ATK)</span> | 
            🛡️ {st.session_state.armor['name']} (+{st.session_state.armor['def']} DEF)
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_c, tab_i, tab_m = st.tabs(["⚔️ COMBATE", "🎒 MOCHILA", "🛒 MERCADO"])

    with tab_c:
        if st.session_state.enemy:
            en = st.session_state.enemy
            st.subheader(f"👹 {en['name']}")
            st.progress(max(0.0, en['hp']/en['max_hp']))
            
            c_at, c_mg = st.columns(2)
            if c_at.button("⚔️ ATACAR"):
                # Cálculo de Dano Físico
                dmg = st.session_state.weapon['atk'] + random.randint(5, 12)
                if is_fury: dmg = int(dmg * 1.9)
                
                stun = False
                if st.session_state.hero_class == "Assassino" and random.random() < 0.25:
                    stun = True; add_log("⚡ STUN! Inimigo paralisado!")

                en['hp'] -= dmg
                add_log(f"Você causou {dmg} de dano!")

                if en['hp'] <= 0:
                    st.session_state.gold += 50 + (st.session_state.floor * 10)
                    st.session_state.kills += 1; st.session_state.enemy = None
                    if st.session_state.kills >= 3:
                        st.session_state.floor += 1; st.session_state.kills = 0
                        add_log("🌟 Você avançou de andar!")
                    st.rerun()
                else:
                    if not stun:
                        if st.session_state.hero_class == "Assassino" and random.random() < 0.30:
                            add_log("💨 Esquivou do contra-ataque!")
                        else:
                            edmg = max(2, en['atk'] - st.session_state.armor['def'])
                            st.session_state.hp -= edmg
                            if st.session_state.hp <= 0: st.session_state.state = 'player_dead'
                    st.rerun()

            if st.session_state.hero_class == "Mago" and c_mg.button("🔥 MAGIA (15 Mana)"):
                if st.session_state.mana >= 15:
                    st.session_state.mana -= 15
                    m_dmg = st.session_state.weapon['atk'] + 25
                    if st.session_state.weapon.get('rarity') == 'raro':
                        m_dmg = int(m_dmg * 1.7)
                        add_log("✨ MAGIA RARA POTENCIALIZADA!")
                    en['hp'] -= m_dmg
                    if en['hp'] <= 0: st.session_state.enemy = None; st.session_state.kills += 1
                    st.rerun()
                else: st.warning("Mana insuficiente!")
        else:
            if st.button("👣 EXPLORAR SALA"):
                if random.random() < 0.50: # 50% chance de baú
                    gain = 40 + (st.session_state.floor * 10)
                    st.session_state.gold += gain; add_log(f"🎁 Baú encontrado! +{gain}G")
                else:
                    st.session_state.enemy = {
                        "name": random.choice(["Gárgula", "Verme Sombrio", "Guarda Ruim"]),
                        "hp": 50 + (st.session_state.floor * 20), "max_hp": 50 + (st.session_state.floor * 20),
                        "atk": 10 + (st.session_state.floor * 4)
                    }
                st.rerun()

    with tab_i:
        if not st.session_state.inventory: st.write("Inventário vazio.")
        for i, item in enumerate(st.session_state.inventory):
            c1, c2 = st.columns([3, 1])
            attr = f"+{item['atk']} ATK" if item['type'] == 'weapon' else f"+{item['def']} DEF"
            c1.write(f"• {item['name']} ({attr})")
            if c2.button("Equipar", key=f"inv_{i}"):
                slot = item['type']
                old = st.session_state[slot]
                st.session_state[slot] = item
                st.session_state.inventory[i] = old
                st.rerun()

    with tab_m:
        col_compra, col_venda = st.columns(2)
        with col_compra:
            st.subheader("🛒 Comprar")
            if st.button("❤️ Poção de Vida (40G) [+50 HP]"):
                if st.session_state.gold >= 40:
                    st.session_state.gold -= 40; st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + 50); st.rerun()
            if st.button("🧪 Poção de Mana (40G) [+40 Mana]"):
                if st.session_state.gold >= 40:
                    st.session_state.gold -= 40; st.session_state.mana = min(st.session_state.max_mana, st.session_state.mana + 40); st.rerun()
            
            st.divider()
            if not st.session_state.market_stock:
                # 50/50 Mercado: Uma Arma e uma Armadura
                w_list = [{"name": "Espada Longa", "atk": 40, "price": 150, "type": "weapon", "rarity": "comum", "value": 70}]
                a_list = [{"name": "Cota de Malha", "def": 20, "price": 130, "type": "armor", "rarity": "comum", "value": 60}]
                if random.random() < 0.02: # 2% Chance Rara
                    w_list.append({"name": "DESTRUIDORA", "atk": 130, "price": 500, "type": "weapon", "rarity": "raro", "value": 250})
                st.session_state.market_stock = [random.choice(w_list), random.choice(a_list)]

            for i, it in enumerate(st.session_state.market_stock):
                txt = f"⚔️ +{it['atk']} ATK" if it['type'] == 'weapon' else f"🛡️ +{it['def']} DEF"
                if st.button(f"{it['name']} ({txt}) - {it['price']}G", key=f"mkt_{i}"):
                    if st.session_state.gold >= it['price']:
                        st.session_state.gold -= it['price']
                        st.session_state.inventory.append(it)
                        st.session_state.market_stock.pop(i); st.rerun()
        
        with col_venda:
            st.subheader("💰 Vender")
            for i, it_inv in enumerate(st.session_state.inventory):
                if st.button(f"Vender {it_inv['name']} (+{it_inv['value']}G)", key=f"sell_{i}"):
                    st.session_state.gold += it_inv['value']
                    st.session_state.inventory.pop(i); st.rerun()

    st.divider()
    for line in st.session_state.log[:3]: st.write(f"`{line}`")

elif st.session_state.state == 'player_dead':
    st.error("💀 GAME OVER")
    if st.button("RECOMEÇAR"): st.session_state.clear(); st.rerun()
