import streamlit as st
import random
import time

# --- CONFIGURAÇÃO E ESTÉTICA ---
st.set_page_config(page_title="Dark Castle: Ascensão", page_icon="🏰", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    .stApp { background-color: #050505; font-family: 'VT323', monospace; color: #4af626; font-size: 20px; }
    
    /* Painel do Herói */
    .hero-panel { 
        border: 2px solid #4af626; padding: 15px; border-radius: 10px; 
        background: rgba(0,255,0,0.05); margin-bottom: 10px;
    }
    
    /* Indicador de Andar */
    .floor-badge {
        background-color: #ffcc00; color: black; padding: 5px 15px;
        border-radius: 20px; font-weight: bold; font-size: 24px;
        display: inline-block; margin-bottom: 15px;
    }

    .rare-tag { color: #00ffff; font-weight: bold; text-shadow: 0 0 8px #00ffff; }
    .berserk-alert { color: #ff4b4b; font-weight: bold; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO SEGURA (Evita AttributeError como na Imagem 8) ---
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
    st.session_state.game_active = True
    st.session_state.hero_class = role
    stats = {
        "Guerreiro": {'hp': 160, 'mana': 30, 'atk': 15, 'def': 5, 'w': "Machado de Ferro"},
        "Mago": {'hp': 90, 'mana': 100, 'atk': 10, 'def': 3, 'w': "Cajado Arcano"},
        "Berserker": {'hp': 200, 'mana': 20, 'atk': 12, 'def': 4, 'w': "Machado Quebrado"},
        "Assassino": {'hp': 110, 'mana': 40, 'atk': 18, 'def': 2, 'w': "Adagas Gêmeas"}
    }
    p = stats[role]
    st.session_state.update({
        'hp': p['hp'], 'max_hp': p['hp'], 'mana': p['mana'], 'max_mana': p['mana'],
        'weapon': {"name": p['w'], "atk": p['atk'], "type": "weapon", "rarity": "comum", "value": 30},
        'armor': {"name": "Traje Inicial", "def": p['def'], "type": "armor", "rarity": "comum", "value": 20},
        'state': 'playing', 'floor': 1, 'kills': 0, 'inventory': [], 'market_stock': []
    })
    st.rerun()

# --- TELA INICIAL (Ajustada conforme solicitado) ---
if not st.session_state.game_active:
    st.markdown("<h1 style='text-align: center; color: #4af626;'>🏰 DARK CASTLE: ASCENSÃO</h1>", unsafe_allow_html=True)
    st.write("---")
    st.subheader("Selecione sua linhagem para entrar no castelo:")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        if st.button("🛡️ GUERREIRO"): start_game("Guerreiro")
    with col2: 
        if st.button("🔮 MAGO"): start_game("Mago")
    with col3: 
        if st.button("🪓 BERSERKER"): start_game("Berserker")
    with col4: 
        if st.button("🗡️ ASSASSINO"): start_game("Assassino")

    st.info("Dica: Cada classe possui habilidades únicas e itens iniciais diferentes.")

# --- TELAS DE FIM DE JOGO ---
elif st.session_state.state == 'player_dead':
    st.error("VOCÊ CAIU EM COMBATE...")
    if st.button("TENTAR NOVAMENTE"): st.session_state.clear(); st.rerun()

# --- TELA DE JOGO ATIVO ---
else:
    # 1. Indicador de Andar (Novo)
    st.markdown(f"<div style='text-align: center;'><span class='floor-badge'>🏰 ANDAR {st.session_state.floor}</span></div>", unsafe_allow_html=True)

    # 2. HUD - Painel do Herói (Corrigido para evitar erro de tag HTML da Imagem 9)
    hp_pct = max(0.0, min(1.0, st.session_state.hp / st.session_state.max_hp))
    is_fury = st.session_state.hero_class == "Berserker" and hp_pct < 0.3
    
    st.markdown(f"""
    <div class="hero-panel">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 22px;"><b>{st.session_state.hero_class.upper()}</b></span>
            <span style="color:#ffd700; font-size: 22px;">💰 {st.session_state.gold}G</span>
        </div>
        <div style="margin: 10px 0;">
            ❤️ HP: {max(0, st.session_state.hp)}/{st.session_state.max_hp} {f'<span class="berserk-alert">| FÚRIA ATIVA!</span>' if is_fury else ''}<br>
            🧪 MANA: {st.session_state.mana}/{st.session_state.max_mana}
        </div>
        <div style="font-size: 14px; border-top: 1px solid #4af626; padding-top: 5px;">
            ⚔️ {st.session_state.weapon['name']} (+{st.session_state.weapon['atk']} ATK) | 
            🛡️ {st.session_state.armor['name']} (+{st.session_state.armor['def']} DEF)
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(hp_pct)

    # 3. Abas de Ação
    tab_fight, tab_inv, tab_shop = st.tabs(["⚔️ COMBATE", "🎒 INVENTÁRIO", "🛒 MERCADO"])

    with tab_fight:
        if st.session_state.enemy:
            en = st.session_state.enemy
            st.subheader(f"👹 Inimigo: {en['name']}")
            st.write(f"Vida: {max(0, en['hp'])} / {en['max_hp']}")
            st.progress(max(0.0, min(1.0, en['hp'] / en['max_hp'])))
            
            if st.button("⚔️ ATACAR"):
                dmg = st.session_state.weapon['atk'] + random.randint(5, 12)
                if is_fury: dmg = int(dmg * 1.9)
                en['hp'] -= dmg
                add_log(f"Você causou {dmg} de dano!")
                
                if en['hp'] <= 0:
                    gold_gain = 40 + (st.session_state.floor * 10)
                    st.session_state.gold += gold_gain
                    st.session_state.kills += 1
                    st.session_state.enemy = None
                    add_log(f"Vitória! Ganhou {gold_gain}G.")
                    if st.session_state.kills >= 3:
                        st.session_state.floor += 1
                        st.session_state.kills = 0
                        add_log(f"Você subiu para o andar {st.session_state.floor}!")
                else:
                    edmg = max(2, en['atk'] - st.session_state.armor['def'])
                    st.session_state.hp -= edmg
                    if st.session_state.hp <= 0: st.session_state.state = 'player_dead'
                st.rerun()
        else:
            st.write("A sala parece silenciosa...")
            if st.button("👣 PROCURAR MONSTRO"):
                st.session_state.enemy = {
                    "name": random.choice(["Gárgula", "Esqueleto", "Verme de Sangue"]),
                    "hp": 50 + (st.session_state.floor * 20),
                    "max_hp": 50 + (st.session_state.floor * 20),
                    "atk": 10 + (st.session_state.floor * 5)
                }
                st.rerun()

    with tab_inv:
        if not st.session_state.inventory:
            st.write("Sua mochila está vazia.")
        for i, item in enumerate(st.session_state.inventory):
            c1, c2 = st.columns([3, 1])
            attr = f"+{item['atk']} ATK" if item['type'] == 'weapon' else f"+{item['def']} DEF"
            c1.write(f"• {item['name']} ({attr})")
            if c2.button("Equipar", key=f"eq_{i}"):
                slot = item['type']
                old = st.session_state[slot]
                st.session_state[slot] = item
                st.session_state.inventory[i] = old
                st.rerun()

    with tab_shop:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🛒 COMPRAR")
            # Poções (Sempre disponíveis)
            if st.button("❤️ Poção de Vida (40G)"):
                if st.session_state.gold >= 40:
                    st.session_state.gold -= 40
                    st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + 50)
                    st.rerun()
                else: st.error("Ouro insuficiente!")
            
            if st.button("🧪 Poção de Mana (40G)"):
                if st.session_state.gold >= 40:
                    st.session_state.gold -= 40
                    st.session_state.mana = min(st.session_state.max_mana, st.session_state.mana + 40)
                    st.rerun()
                else: st.error("Ouro insuficiente!")
            
            st.divider()
            
            # Equipamentos (50% Ataque / 50% Defesa)
            if not st.session_state.market_stock:
                w_pool = [{"name": "Espada de Aço", "atk": 35, "price": 120, "type": "weapon", "rarity": "comum", "value": 60}]
                a_pool = [{"name": "Cota de Malha", "def": 15, "price": 100, "type": "armor", "rarity": "comum", "value": 50}]
                if random.random() < 0.05: # Chance rara
                    w_pool.append({"name": "Lâmina Divina", "atk": 100, "price": 400, "type": "weapon", "rarity": "raro", "value": 200})
                st.session_state.market_stock = [random.choice(w_pool), random.choice(a_pool)]

            for i, it in enumerate(st.session_state.market_stock):
                attr = f"+{it['atk']} ATK" if it['type'] == 'weapon' else f"+{it['def']} DEF"
                if st.button(f"Comprar {it['name']} ({attr}) - {it['price']}G", key=f"shop_{i}"):
                    if st.session_state.gold >= it['price']:
                        st.session_state.gold -= it['price']
                        st.session_state.inventory.append(it)
                        st.session_state.market_stock.pop(i)
                        st.rerun()
        
        with col2:
            st.subheader("💰 VENDER")
            if not st.session_state.inventory:
                st.write("Nada para vender.")
            for i, item in enumerate(st.session_state.inventory):
                if st.button(f"Vender {item['name']} (+{item['value']}G)", key=f"sell_{i}"):
                    st.session_state.gold += item['value']
                    st.session_state.inventory.pop(i)
                    st.rerun()

    # Log de Combate (Corrigido erro de sintaxe da Imagem 2)
    st.divider()
    for line in st.session_state.log[:3]:
        st.write(f"`{line}`")
