import streamlit as st
import random
import time

# --- CONFIGURAÇÃO VISUAL E ESTILO ---
st.set_page_config(page_title="Dark Castle: Definitive Edition", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    .stApp { background-color: #050505; font-family: 'VT323', monospace; color: #4af626; font-size: 20px; }
    .hero-panel { border: 2px solid #4af626; padding: 15px; border-radius: 10px; background: rgba(0,255,0,0.05); margin-bottom: 10px; }
    .stat-tag { color: #ffcc00; font-weight: bold; }
    .rare-tag { color: #00ffff; font-weight: bold; text-shadow: 0 0 5px #00ffff; }
    .berserk-alert { color: #ff4b4b; font-weight: bold; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO DO JOGO ---
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False, 'hero_class': "Viajante", 'hp': 100, 'max_hp': 100, 
        'gold': 80, 'log': ["O castelo te espera..."], 'enemy': None,
        'weapon': {"name": "Punhal Velho", "atk": 8, "type": "weapon", "value": 10, "rarity": "comum"},
        'armor': {"name": "Trapos", "def": 2, "type": "armor", "value": 5},
        'floor': 1, 'kills': 0, 'inventory': [], 'state': 'playing',
        'market_stock': [] # Controle de reposição de itens
    })

FLOOR_GOALS = {1: 3, 2: 4, 3: 5, 4: 2, 5: 1}

def add_log(msg):
    st.session_state.log.insert(0, f"[{time.strftime('%H:%M')}] {msg}")

def start_game(role):
    st.session_state.game_active = True
    st.session_state.hero_class = role
    if role == "Guerreiro":
        st.session_state.update({'hp': 160, 'max_hp': 160, 'weapon': {"name": "Espada Curta", "atk": 15, "type": "weapon", "value": 30, "rarity": "comum"}})
    elif role == "Mago":
        st.session_state.update({'hp': 90, 'max_hp': 90, 'weapon': {"name": "Cajado de Aprendiz", "atk": 10, "type": "weapon", "value": 30, "rarity": "comum"}})
    elif role == "Berserker":
        st.session_state.update({'hp': 200, 'max_hp': 200, 'weapon': {"name": "Machado Quebrado", "atk": 12, "type": "weapon", "value": 20, "rarity": "comum"}})
    elif role == "Assassino":
        st.session_state.update({'hp': 110, 'max_hp': 110, 'weapon': {"name": "Adagas Duplas", "atk": 18, "type": "weapon", "value": 40, "rarity": "comum"}})
    st.rerun()

# --- TELA INICIAL ---
if not st.session_state.game_active:
    st.title("🏰 DARK CASTLE: ASCENSÃO")
    st.subheader("Selecione sua Classe:")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🛡️ GUERREIRO"): start_game("Guerreiro")
    if c2.button("🔮 MAGO"): start_game("Mago")
    if c3.button("🪓 BERSERKER"): start_game("Berserker")
    if c4.button("🗡️ ASSASSINO"): start_game("Assassino")
    
    with st.expander("📝 NOTAS DA ATUALIZAÇÃO"):
        st.write("- **Berserker:** +90% ATK quando HP < 30%.")
        st.write("- **Assassino:** 30% de chance de desviar e causa Stun (inimigo não ataca).")
        st.write("- **Mago:** Magia causa +70% dano se usar item Raro.")
        st.write("- **Exploração:** +20% de chance de achar Baús.")

# --- LÓGICA DE JOGO ATIVO ---
elif st.session_state.state == 'playing':
    # HUD
    safe_hp_ratio = max(0.0, min(1.0, st.session_state.hp / st.session_state.max_hp))
    is_berserk = st.session_state.hero_class == "Berserker" and (st.session_state.hp / st.session_state.max_hp) < 0.3
    
    st.markdown(f"""
    <div class="hero-panel">
        <div style="display: flex; justify-content: space-between;">
            <div><b>{st.session_state.hero_class.upper()}</b> | ANDAR {st.session_state.floor}</div>
            <div style="color:#ffd700;">💰 {st.session_state.gold}G</div>
        </div>
        <div>❤️ HP: {max(0, st.session_state.hp)}/{st.session_state.max_hp} {'<span class="berserk-alert">(FÚRIA ATIVA!)</span>' if is_berserk else ''}</div>
        <div style="font-size: 14px; opacity: 0.8;">
            ⚔️ {st.session_state.weapon['name']} (+{st.session_state.weapon['atk']} ATK) 
            {f' <span class="rare-tag">[RARIDADE: {st.session_state.weapon["rarity"].upper()}]</span>' if st.session_state.weapon.get('rarity') == 'raro' else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(safe_hp_ratio)

    tab_f, tab_i, tab_s = st.tabs(["⚔️ COMBATE", "🎒 INVENTÁRIO", "🛒 MERCADO"])

    with tab_f:
        if st.session_state.enemy:
            en = st.session_state.enemy
            st.write(f"👹 **{en['name']}** | HP: {max(0, en['hp'])}")
            st.progress(max(0.0, min(1.0, en['hp'] / en['max_hp'])))
            
            c1, c2 = st.columns(2)
            
            # Botão de Ataque Padrão
            if c1.button("⚔️ ATACAR"):
                base_atk = st.session_state.weapon['atk']
                if is_berserk: base_atk *= 1.9 # +90% de bônus
                
                dmg = int(base_atk + random.randint(5, 15))
                stunned = False
                
                # Especial Assassino: Stun (25% chance)
                if st.session_state.hero_class == "Assassino" and random.random() < 0.25:
                    stunned = True
                    add_log("⚡ STUN! O inimigo está atordoado!")

                en['hp'] -= dmg
                add_log(f"Você causou {dmg} de dano!")
                
                if en['hp'] <= 0:
                    st.session_state.gold += 40
                    st.session_state.kills += 1
                    st.session_state.enemy = None
                    if st.session_state.kills >= FLOOR_GOALS.get(st.session_state.floor, 3):
                        st.session_state.floor += 1; st.session_state.kills = 0
                    st.rerun()
                else:
                    # Defesa / Esquiva
                    if stunned:
                        add_log("Inimigo atordoado não atacou.")
                    elif st.session_state.hero_class == "Assassino" and random.random() < 0.30:
                        add_log("💨 ESQUIVA! Você desviou do ataque!")
                    else:
                        edmg = max(2, en['atk'] - st.session_state.armor.get('def', 0))
                        st.session_state.hp -= edmg
                        if st.session_state.hp <= 0: st.session_state.state = 'player_dead'
                    st.rerun()

            # Botão Especial do Mago
            if st.session_state.hero_class == "Mago":
                if c2.button("🔥 ATAQUE DE MAGIA"):
                    mag_dmg = st.session_state.weapon['atk'] + 20
                    if st.session_state.weapon.get('rarity') == 'raro':
                        mag_dmg *= 1.7 # +70% dano raro
                        add_log("✨ MAGIA POTENCIALIZADA!")
                    
                    en['hp'] -= int(mag_dmg)
                    add_log(f"Magia causou {int(mag_dmg)} de dano!")
                    # Inimigo contra-ataca
                    edmg = max(5, en['atk'] - 2)
                    st.session_state.hp -= edmg
                    if en['hp'] <= 0: 
                        st.session_state.enemy = None; st.session_state.kills += 1
                    st.rerun()

        else:
            if st.button("👣 EXPLORAR ANDAR"):
                # Ajuste de Probabilidade: Baú (+20% em cima da base de 30% = 50% chance)
                if random.random() < 0.50: 
                    item_puro = {"name": "Tesouro", "value": 50, "type": "gold"}
                    st.session_state.gold += 50
                    add_log("🎁 Baú encontrado! +50G")
                else:
                    st.session_state.enemy = {"name": "Monstro", "hp": 70, "max_hp": 70, "atk": 18}
                st.rerun()

    with tab_i:
        for idx, item in enumerate(st.session_state.inventory):
            c1, c2 = st.columns([3, 1])
            c1.write(f"{item['name']} (+{item.get('atk', 0)} ATK)")
            if c2.button("Equipar", key=f"inv_{idx}"):
                old = st.session_state['weapon']
                st.session_state['weapon'] = item
                st.session_state.inventory[idx] = old
                st.rerun()

    with tab_s:
        # Lógica de Mercado com Reposição e Itens Raros (2%)
        if not st.session_state.market_stock:
            # Gerar novos itens
            pool = [
                {"name": "Espada Pesada", "atk": 40, "price": 150, "type": "weapon", "rarity": "comum"},
                {"name": "Dagas de Vidro", "atk": 38, "price": 140, "type": "weapon", "rarity": "comum"},
                {"name": "Grimório Negro", "atk": 35, "price": 160, "type": "weapon", "rarity": "comum"}
            ]
            # Chance de 2% de item RARO aparecer
            if random.random() < 0.02:
                pool.append({"name": "EXCALIBUR (Lendária)", "atk": 120, "price": 400, "type": "weapon", "rarity": "raro"})
            if random.random() < 0.02:
                pool.append({"name": "CAJADO DE MERLIN", "atk": 100, "price": 400, "type": "weapon", "rarity": "raro"})
            
            st.session_state.market_stock = random.sample(pool, 2)

        st.subheader("Itens Disponíveis")
        for idx, it in enumerate(st.session_state.market_stock):
            label = f"⭐ {it['name']}" if it['rarity'] == 'raro' else it['name']
            if st.button(f"{label} - {it['price']}G", key=f"shop_{idx}"):
                if st.session_state.gold >= it['price']:
                    st.session_state.gold -= it['price']
                    st.session_state.inventory.append(it)
                    st.session_state.market_stock.pop(idx) # Remove após compra
                    add_log(f"Comprou {it['name']}!")
                    st.rerun()
                else: st.error("Ouro insuficiente!")
        
        if st.button("🔄 Atualizar Estoque (20G)"):
            if st.session_state.gold >= 20:
                st.session_state.gold -= 20
                st.session_state.market_stock = []
                st.rerun()

    st.divider()
    for line in st.session_state.log[:3]: st.write(f"`{line}`")

elif st.session_state.state == 'player_dead':
    st.error("VOCÊ MORREU!")
    if st.button("RECOMEÇAR"): st.session_state.clear(); st.rerun()
