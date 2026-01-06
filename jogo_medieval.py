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

# --- INICIALIZAÇÃO SEGURA DO ESTADO ---
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False, 'hero_class': "Viajante", 'hp': 100, 'max_hp': 100, 
        'gold': 80, 'log': ["O castelo te espera..."], 'enemy': None,
        'weapon': {"name": "Punhal Velho", "atk": 8, "type": "weapon", "value": 10, "rarity": "comum"},
        'armor': {"name": "Trapos", "def": 2, "type": "armor", "value": 5},
        'floor': 1, 'kills': 0, 'inventory': [], 'state': 'playing',
        'market_stock': [] 
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
    with st.expander("📖 GUIA E ATUALIZAÇÕES", expanded=True):
        st.write("- **Berserker**: +90% ATK quando HP < 30%.")
        st.write("- **Assassino**: 30% chance de esquiva e chance de causar Stun.")
        st.write("- **Mago**: Magia causa +70% dano com armas RARAS.")
        st.write("- **Exploração**: Chance de baús aumentada em +20%.")
    
    st.subheader("Selecione sua Classe:")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🛡️ GUERREIRO"): start_game("Guerreiro")
    if c2.button("🔮 MAGO"): start_game("Mago")
    if c3.button("🪓 BERSERKER"): start_game("Berserker")
    if c4.button("🗡️ ASSASSINO"): start_game("Assassino")

# --- LÓGICA DE JOGO ATIVO ---
elif st.session_state.state == 'playing':
    # HUD Corrigido (Evita erros das imagens 1 e 7)
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
            if c1.button("⚔️ ATACAR"):
                base_atk = st.session_state.weapon['atk']
                if is_berserk: base_atk *= 1.9 
                
                dmg = int(base_atk + random.randint(5, 15))
                stunned = False
                
                if st.session_state.hero_class == "Assassino" and random.random() < 0.25:
                    stunned = True
                    add_log("⚡ STUN! O inimigo está atordoado!")

                en['hp'] -= dmg
                add_log(f"Causou {dmg} de dano!")
                
                if en['hp'] <= 0:
                    st.session_state.gold += 40
                    st.session_state.kills += 1
                    st.session_state.enemy = None
                    if st.session_state.kills >= FLOOR_GOALS.get(st.session_state.floor, 3):
                        st.session_state.floor += 1; st.session_state.kills = 0
                    st.rerun()
                else:
                    if stunned: add_log("Inimigo atordoado não atacou.")
                    elif st.session_state.hero_class == "Assassino" and random.random() < 0.30:
                        add_log("💨 ESQUIVA! Você desviou do ataque!")
                    else:
                        edmg = max(2, en['atk'] - st.session_state.armor.get('def', 0))
                        st.session_state.hp -= edmg
                        if st.session_state.hp <= 0: st.session_state.state = 'player_dead'
                    st.rerun()

            if st.session_state.hero_class == "Mago" and c2.button("🔥 MAGIA"):
                mag_dmg = st.session_state.weapon['atk'] + 20
                if st.session_state.weapon.get('rarity') == 'raro':
                    mag_dmg *= 1.7
                    add_log("✨ MAGIA POTENCIALIZADA!")
                en['hp'] -= int(mag_dmg)
                add_log(f"Magia causou {int(mag_dmg)} de dano!")
                st.session_state.hp -= max(5, en['atk'] - 5)
                if en['hp'] <= 0: st.session_state.enemy = None; st.session_state.kills += 1
                st.rerun()
        else:
            if st.button("👣 EXPLORAR"):
                if random.random() < 0.50: # Chance de baú +20%
                    st.session_state.gold += 50
                    add_log("🎁 Baú encontrado! +50G")
                else:
                    st.session_state.enemy = {"name": "Monstro", "hp": 70, "max_hp": 70, "atk": 18}
                st.rerun()

    with tab_i:
        st.subheader("Mochila")
        if not st.session_state.inventory: st.write("Vazia.")
        for idx, item in enumerate(st.session_state.inventory):
            col1, col2, col3 = st.columns([2, 1, 1])
            col1.write(f"{item['name']} (+{item.get('atk', 0)} ATK)")
            if col2.button("Equipar", key=f"e_{idx}"):
                old = st.session_state['weapon']
                st.session_state['weapon'] = item
                st.session_state.inventory[idx] = old
                st.rerun()
            if col3.button("Vender", key=f"v_{idx}"):
                st.session_state.gold += item.get('value', 20)
                st.session_state.inventory.pop(idx)
                st.rerun()

    with tab_s:
        # Reposição de Estoque e Itens Raros (Corrigindo imagem 7)
        if not st.session_state.get('market_stock'):
            pool = [
                {"name": "Espada de Aço", "atk": 30, "price": 100, "type": "weapon", "rarity": "comum", "value": 50},
                {"name": "Cajado Arcano", "atk": 28, "price": 110, "type": "weapon", "rarity": "comum", "value": 55}
            ]
            if random.random() < 0.02: # 2% Chance Rara
                pool.append({"name": "LÂMINA INFINITA", "atk": 150, "price": 500, "type": "weapon", "rarity": "raro", "value": 250})
            st.session_state.market_stock = random.sample(pool, min(len(pool), 2))

        for idx, it in enumerate(st.session_state.market_stock):
            rarity_prefix = "⭐ " if it['rarity'] == 'raro' else ""
            if st.button(f"Comprar {rarity_prefix}{it['name']} ({it['price']}G)", key=f"shop_{idx}"):
                if st.session_state.gold >= it['price']:
                    st.session_state.gold -= it['price']
                    st.session_state.inventory.append(it)
                    st.session_state.market_stock.pop(idx)
                    st.rerun()
        
        if st.button("🔄 Renovar Estoque (20G)"):
            if st.session_state.gold >= 20:
                st.session_state.gold -= 20
                st.session_state.market_stock = []
                st.rerun()

    st.divider()
    for line in st.session_state.log[:3]: st.write(f"`{line}`") # Corrigindo imagem 3

elif st.session_state.state == 'player_dead':
    st.error("VOCÊ CAIU EM COMBATE!")
    if st.button("RECOMEÇAR"): st.session_state.clear(); st.rerun()
