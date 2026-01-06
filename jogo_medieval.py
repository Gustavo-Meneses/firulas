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
    .item-stat { color: #ffcc00; font-weight: bold; }
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
        'inventory': []
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

# --- GERENCIAMENTO DE ITENS E VENDAS ---
def handle_item(item_idx, action):
    item = st.session_state.inventory[item_idx]
    if action == "descartar":
        st.session_state.inventory.pop(item_idx)
        add_log(f"🗑️ Descartou: {item['name']}")
    elif action == "usar" and "Poção" in item['name']:
        st.session_state.hp = min(st.session_state.max_hp, st.session_state.hp + 40)
        st.session_state.inventory.pop(item_idx)
        add_log("🧪 Bebeu poção (+40 HP)!")
    elif action == "equipar":
        target = 'weapon' if item['type'] == "weapon" else 'armor'
        old_item = st.session_state[target]
        st.session_state[target] = item
        st.session_state.inventory[item_idx] = old_item
        add_log(f"⚔️ Equipou {item['name']}!")

def sell_item(item_idx):
    item = st.session_state.inventory.pop(item_idx)
    st.session_state.gold += 20
    add_log(f"💰 Vendeu {item['name']} por 20G")

# --- UI PRINCIPAL ---

if not st.session_state.game_active:
    st.title("🏰 DARK CASTLE: ASCENSÃO")
    with st.expander("📖 GUIA DO AVENTUREIRO", expanded=True):
        st.write("""
        - **Objetivo:** Chegue ao 5º andar e derrote o Lorde das Sombras.
        - **Combate:** Use ataques físicos ou magia (consome mana).
        - **Bolsa:** Clique em '🎒 BOLSA' para equipar armas ou tomar poções.
        - **Mercado:** Venda itens achados em baús para comprar equipamentos melhores.
        """)
    st.subheader("Escolha sua classe:")
    c1, c2 = st.columns(2)
    if c1.button("🛡️ GUERREIRO"): start_game("Guerreiro"); st.rerun()
    if c2.button("🔮 MAGO"): start_game("Mago"); st.rerun()

else:
    # HUD DE VIDA E OURO
    hp_p = (st.session_state.hp / st.session_state.max_hp) * 100
    st.markdown(f"""
    <div class="char-hud">
        ❤️ VIDA: {st.session_state.hp}/{st.session_state.max_hp} | 💰 <span class="gold-count">{st.session_state.gold}G</span>
        <div style="background: #333; width: 100%; height: 12px; border: 1px solid #4af626; margin-top:5px;">
            <div style="background: #4af626; width: {hp_p}%; height: 100%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # INVENTÁRIO INTERATIVO COM STATUS
    with st.expander("🎒 BOLSA DE ITENS (ABRIR)", expanded=False):
        if not st.session_state.inventory:
            st.write("Sua bolsa está vazia.")
        for idx, item in enumerate(st.session_state.inventory):
            col_n, col_a = st.columns([2.5, 1.5])
            
            # Formatação do nome com o status
            stat_info = ""
            if item['type'] == "weapon":
                stat_info = f" <span class='item-stat'>(+{item['atk']} ATK)</span>"
            elif item['type'] == "armor":
                stat_info = f" <span class='item-stat'>(+{item['def']} DEF)</span>"
            
            col_n.markdown(f"• {item['name']}{stat_info}", unsafe_allow_html=True)
            
            with col_a:
                ca, cb = st.columns(2)
                if item['type'] in ["weapon", "armor"]:
                    if ca.button("Equipar", key=f"eq_{idx}"): handle_item(idx, "equipar"); st.rerun()
                elif "Poção" in item['name']:
                    if ca.button("Beber", key=f"us_{idx}"): handle_item(idx, "usar"); st.rerun()
                if cb.button("Lixo", key=f"del_{idx}"): handle_item(idx, "descartar"); st.rerun()

    st.divider()

    # LOGICA DE ESTADOS
    if st.session_state.hp <= 0:
        st.error("💀 VOCÊ MORREU")
        if st.button("RECOMEÇAR"): st.session_state.clear(); st.rerun()

    elif st.session_state.in_shop:
        st.title("🛒 MERCADOR")
        t_buy, t_sell = st.tabs(["Comprar", "Vender"])
        with t_buy:
            if st.button("🗡️ ESPADA LONGA - 30 ATK (120G)"):
                if st.session_state.gold >= 120:
                    st.session_state.gold -= 120
                    st.session_state.inventory.append({"name": "Espada Longa", "atk": 30, "type": "weapon"})
                    add_log("🛒 Comprou Espada Longa!")
                else: add_log("❌ Ouro insuficiente!")
            if st.button("🧪 POÇÃO DE VIDA (40G)"):
                if st.session_state.gold >= 40:
                    st.session_state.gold -= 40
                    st.session_state.inventory.append({"name": "Poção de Vida", "type": "consumable"})
                    add_log("🛒 Comprou Poção!")
                else: add_log("❌ Ouro insuficiente!")
        with t_sell:
            for idx, item in enumerate(st.session_state.inventory):
                if st.button(f"Vender {item['name']} (+20G)", key=f"sl_{idx}"):
                    sell_item(idx); st.rerun()
        if st.button("🔙 VOLTAR"): st.session_state.in_shop = False; st.rerun()

    elif st.session_state.enemy:
        enemy = st.session_state.enemy
        st.subheader(f"👹 COMBATE: {enemy['name']}")
        e_hp_p = max(0, enemy['hp'])
        st.warning(f"HP DO INIMIGO: {e_hp_p}")
        st.progress(min(1.0, e_hp_p / 100) if enemy['name'] != "LORDE DAS SOMBRAS" else min(1.0, e_hp_p / 500))
        
        c1, c2 = st.columns(2)
        if c1.button("⚔️ ATACAR"):
            dmg = st.session_state.weapon['atk'] + random.randint(5, 10)
            enemy['hp'] -= dmg
            add_log(f"💥 Você causou {dmg} de dano!")
            if enemy['hp'] <= 0:
                st.session_state.gold += 40; st.session_state.enemy = None; add_log("🏆 Inimigo derrotado!")
            else:
                edmg = max(2, 18 - st.session_state.armor['def'])
                st.session_state.hp -= edmg; add_log(f"🩸 Inimigo revidou: {edmg}")
            st.rerun()
        if c2.button("🔥 MAGIA (25 MP)"):
            if st.session_state.mana >= 25:
                st.session_state.mana -= 25
                dmg = 50 + (st.session_state.level * 5)
                enemy['hp'] -= dmg
                add_log(f"🔮 Magia causou {dmg}!")
                if enemy['hp'] <= 0:
                    st.session_state.gold += 40; st.session_state.enemy = None; add_log("🏆 Vitória Arcana!")
                else:
                    st.session_state.hp -= 10; add_log("🩸 Sofreu contra-ataque!")
            else: add_log("❌ Sem Mana!")
            st.rerun()

    elif st.session_state.chest_found:
        st.title("🎁 BAÚ ENCONTRADO!")
        if st.button("🔓 ABRIR"):
            if random.random() < 0.7:
                item = random.choice([
                    {"name": "Poção de Vida", "type": "consumable"},
                    {"name": "Escudo de Madeira", "def": 6, "type": "armor"},
                    {"name": "Lança Curta", "atk": 22, "type": "weapon"}
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
            if st.session_state.floor == 5 and st.session_state.progress_floor >= 2:
                st.session_state.enemy = {"name": "LORDE DAS SOMBRAS", "hp": 500, "atk": 30}
            elif roll < 0.5: 
                st.session_state.enemy = {"name": "Esqueleto", "hp": 60 + (st.session_state.floor * 10)}
            elif roll < 0.8: 
                st.session_state.chest_found = True
            else: 
                add_log("👣 O corredor está silencioso...")
                st.session_state.progress_floor += 0.5 # Corredores vazios dão meio progresso
            st.rerun()
        if c2.button("🛒 MERCADOR"): st.session_state.in_shop = True; st.rerun()

    # HISTÓRICO
    st.divider()
    for line in st.session_state.log[:3]: st.write(f"`{line}`")
