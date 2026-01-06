import streamlit as st
import random

# --- ESTÉTICA E UI ---
st.set_page_config(page_title="Dark Castle: RPG Manager", page_icon="🎒", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    .stApp { background-color: #050505; font-family: 'VT323', monospace; color: #4af626; font-size: 20px; }
    .char-hud { background: rgba(0, 255, 0, 0.1); border: 2px solid #4af626; padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center; }
    .gold-count { color: #ffd700; font-size: 24px; font-weight: bold; }
    .stButton>button { background-color: #111; color: #4af626; border: 1px solid #4af626; border-radius: 0px; font-family: 'VT323', monospace; margin-top: 5px; }
    .stButton>button:hover { background-color: #4af626; color: #000; }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO ---
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False, 'hero_class': "Viajante", 'level': 1, 'hp': 100, 'max_hp': 100, 
        'mana': 50, 'gold': 0, 'log': ["Sua jornada começa..."], 'enemy': None,
        'weapon': {"name": "Adaga Velha", "atk": 8, "type": "weapon"},
        'armor': {"name": "Trapos", "def": 2, "type": "armor"},
        'floor': 1, 'progress_floor': 0, 'in_shop': False, 'chest_found': False,
        'inventory': [] # Lista de dicionários de itens
    })

def add_log(msg):
    st.session_state.log.insert(0, msg)

def start_game(role):
    st.session_state.game_active = True
    st.session_state.hero_class = role
    if role == "Guerreiro":
        st.session_state.hp = st.session_state.max_hp = 150
        st.session_state.weapon = {"name": "Machado de Ferro", "atk": 15, "type": "weapon"}
    else:
        st.session_state.hp = st.session_state.max_hp = 90
        st.session_state.mana = 120
        st.session_state.weapon = {"name": "Cajado Rúnico", "atk": 10, "type": "weapon"}

# --- GERENCIAMENTO DE ITENS ---
def handle_item(item_idx, action):
    item = st.session_state.inventory[item_idx]
    
    if action == "descartar":
        st.session_state.inventory.pop(item_idx)
        add_log(f"🗑️ Você jogou fora: {item['name']}")
    
    elif action == "usar":
        if "Poção" in item['name']:
            st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + 40)
            st.session_state.inventory.pop(item_idx)
            add_log("🧪 Você bebeu a poção e recuperou 40 HP!")
    
    elif action == "equipar":
        if item['type'] == "weapon":
            old_weapon = st.session_state.weapon
            st.session_state.weapon = item
            st.session_state.inventory[item_idx] = old_weapon
            add_log(f"⚔️ Equipou {item['name']}. {old_weapon['name']} voltou para a bolsa.")
        elif item['type'] == "armor":
            old_armor = st.session_state.armor
            st.session_state.armor = item
            st.session_state.inventory[item_idx] = old_armor
            add_log(f"🛡️ Equipou {item['name']}. {old_armor['name']} voltou para a bolsa.")

def sell_item(item_idx):
    item = st.session_state.inventory.pop(item_idx)
    price = 20 # Preço fixo de revenda para simplificar
    st.session_state.gold += price
    add_log(f"💰 Vendeu {item['name']} por {price}G")

# --- UI PRINCIPAL ---
if not st.session_state.game_active:
    st.title("🏰 DARK CASTLE: RPG MANAGER")
    c1, c2 = st.columns(2)
    if c1.button("🛡️ GUERREIRO"): start_game("Guerreiro"); st.rerun()
    if c2.button("🔮 MAGO"): start_game("Mago"); st.rerun()
else:
    # HUD
    hp_p = (st.session_state.hp / st.session_state.max_hp) * 100
    st.markdown(f"""
    <div class="char-hud">
        ❤️ HP: {st.session_state.hp}/{st.session_state.max_hp} | 💰 <span class="gold-count">{st.session_state.gold}G</span>
        <div style="background: #333; width: 100%; height: 10px; border: 1px solid #4af626; margin-top:5px;">
            <div style="background: #4af626; width: {hp_p}%; height: 100%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # INVENTÁRIO INTERATIVO
    with st.expander("🎒 BOLSA DE ITENS", expanded=False):
        if not st.session_state.inventory:
            st.write("Vazia...")
        for idx, item in enumerate(st.session_state.inventory):
            col_name, col_act = st.columns([2, 2])
            col_name.write(f"• **{item['name']}**")
            
            with col_act:
                c1, c2 = st.columns(2)
                if item['type'] in ["weapon", "armor"]:
                    if c1.button("Equipar", key=f"eq_{idx}"): handle_item(idx, "equipar"); st.rerun()
                elif "Poção" in item['name']:
                    if c1.button("Beber", key=f"use_{idx}"): handle_item(idx, "usar"); st.rerun()
                
                if c2.button("Lixo", key=f"del_{idx}"): handle_item(idx, "descartar"); st.rerun()

    st.divider()

    # ESTADOS DE JOGO
    if st.session_state.hp <= 0:
        st.error("💀 FIM DA LINHA")
        if st.button("RECOMEÇAR"): st.session_state.clear(); st.rerun()

    elif st.session_state.in_shop:
        st.title("🛒 MERCADOR")
        tab_buy, tab_sell = st.tabs(["Comprar", "Vender"])
        
        with tab_buy:
            c1, c2 = st.columns(2)
            if c1.button("🗡️ ESPADA (100G)"):
                if st.session_state.gold >= 100:
                    st.session_state.gold -= 100
                    st.session_state.inventory.append({"name": "Espada", "atk": 25, "type": "weapon"})
                    add_log("🛒 Espada comprada!")
                else: add_log("❌ Sem ouro!")
            if c2.button("🧪 POÇÃO (40G)"):
                if st.session_state.gold >= 40:
                    st.session_state.gold -= 40
                    st.session_state.inventory.append({"name": "Poção de Vida", "type": "consumable"})
                    add_log("🛒 Poção comprada!")
                else: add_log("❌ Sem ouro!")
        
        with tab_sell:
            if not st.session_state.inventory: st.write("Nada para vender.")
            for idx, item in enumerate(st.session_state.inventory):
                if st.button(f"Vender {item['name']} (20G)", key=f"sell_{idx}"):
                    sell_item(idx); st.rerun()
        
        if st.button("🔙 SAIR"): st.session_state.in_shop = False; st.rerun()

    elif st.session_state.enemy:
        st.subheader(f"👹 COMBATE: {st.session_state.enemy['name']}")
        if st.button("⚔️ ATACAR"):
            dmg = st.session_state.weapon['atk'] + random.randint(5, 10)
            st.session_state.enemy['hp'] -= dmg
            add_log(f"💥 Causou {dmg} de dano!")
            if st.session_state.enemy['hp'] <= 0:
                st.session_state.gold += 30; st.session_state.enemy = None; add_log("🏆 Vitória!")
            else:
                edmg = max(1, 15 - st.session_state.armor['def'])
                st.session_state.hp -= edmg; add_log(f"🩸 Recebeu {edmg} de dano!")
            st.rerun()

    elif st.session_state.chest_found:
        st.title("🎁 BAÚ!")
        if st.button("🔓 ABRIR"):
            roll = random.random()
            if roll < 0.7:
                item = random.choice([
                    {"name": "Poção de Vida", "type": "consumable"},
                    {"name": "Escudo Velho", "def": 5, "type": "armor"},
                    {"name": "Punhal Rápido", "atk": 18, "type": "weapon"}
                ])
                st.session_state.inventory.append(item)
                add_log(f"🎁 Achou: {item['name']}!")
            else: add_log("💨 Estava vazio...")
            st.session_state.chest_found = False; st.rerun()
        if st.button("🏃 IGNORAR"): st.session_state.chest_found = False; st.rerun()

    else:
        st.title(f"🏰 ANDAR {st.session_state.floor}")
        c1, c2 = st.columns(2)
        if c1.button("👣 EXPLORAR"):
            roll = random.random()
            if roll < 0.5: st.session_state.enemy = {"name": "Esqueleto", "hp": 50}
            elif roll < 0.8: st.session_state.chest_found = True
            else: add_log("👣 Nada aqui...")
            st.rerun()
        if c2.button("🛒 MERCADOR"): st.session_state.in_shop = True; st.rerun()

    st.divider()
    for line in st.session_state.log[:3]: st.write(f"`{line}`")
