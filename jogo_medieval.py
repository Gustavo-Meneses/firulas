import streamlit as st
import random
import time

### ============================================================
### CONFIGURAÇÃO DA PÁGINA E CSS
### ============================================================
st.set_page_config(page_title="Dark Castle: Ascensão", page_icon="🏰", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    /* Estilos Dark Fantasy e animações aqui */
    .bar-wrap { width: 100%; background: #222; border: 1px solid #444; height: 10px; margin-bottom: 5px; }
    .bar-fill-hp { background: #e53935; height: 100%; transition: width 0.3s; }
    .dmg-number { position: absolute; font-weight: bold; font-size: 1.5rem; color: #ff5252; animation: fadeUp 1s forwards; }
    @keyframes fadeUp { 0% { opacity: 1; transform: translateY(0); } 100% { opacity: 0; transform: translateY(-20px); } }
</style>
""", unsafe_allow_html=True)

### ============================================================
### CONSTANTES
### ============================================================
CLASSES = {
    "Guerreiro": { "icon": "🛡️", "hp": 180, "mana": 30, "atk": 14, "def_val": 9, "weapon": {"name": "Espada Curta", "atk": 14, "type": "weapon", "rarity": "comum"}, "armor": {"name": "Cota de Ferro", "def": 9, "type": "armor", "rarity": "comum"}, "stats": {"força": 4, "agilidade": 2, "magia": 1} },
    "Mago": { "icon": "🔮", "hp": 90, "mana": 140, "atk": 10, "def_val": 3, "weapon": {"name": "Cajado Aprendiz", "atk": 10, "type": "weapon", "rarity": "comum"}, "armor": {"name": "Manto de Linho", "def": 3, "type": "armor", "rarity": "comum"}, "stats": {"força": 1, "agilidade": 2, "magia": 5} },
    "Berserker": { "icon": "🪓", "hp": 220, "mana": 20, "atk": 12, "def_val": 4, "weapon": {"name": "Machado Gasto", "atk": 12, "type": "weapon", "rarity": "comum"}, "armor": {"name": "Pelagem Grossa", "def": 4, "type": "armor", "rarity": "comum"}, "stats": {"força": 5, "agilidade": 3, "magia": 0} },
    "Assassino": { "icon": "🗡️", "hp": 115, "mana": 55, "atk": 18, "def_val": 2, "weapon": {"name": "Adagas Duplas", "atk": 18, "type": "weapon", "rarity": "comum"}, "armor": {"name": "Couro Negro", "def": 2, "type": "armor", "rarity": "comum"}, "stats": {"força": 3, "agilidade": 5, "magia": 2} }
}

ENEMIES = {
    1: [("Rato Gigante", 40, 8, "🐀"), ("Esqueleto Torto", 50, 10, "💀")],
    2: [("Gárgula de Pedra", 80, 18, "🗿"), ("Espectro Faminto", 70, 22, "👻")],
    3: [("Cavaleiro Corrompido", 130, 28, "⚔️")],
    4: [("Dragão Menor", 180, 38, "🐉")],
    5: [("Lorde das Sombras", 250, 50, "👁️")]
}

MARKET_POOL = {
    "weapon": [{"name": "Espada Longa", "atk": 36, "price": 140, "rarity": "comum"}],
    "armor": [{"name": "Cota de Malha", "def": 18, "price": 120, "rarity": "comum"}]
}

ANIM_NONE = ""
ANIM_HERO_DEATH = "anim-hero-death"

### ============================================================
### HELPERS E ESTADO
### ============================================================
def log(msg: str, kind: str = ""):
    ts = time.strftime('%H:%M')
    st.session_state.log.insert(0, {"t": ts, "msg": msg, "kind": kind})
    if len(st.session_state.log) > 30: st.session_state.log.pop()

def spawn_enemy(floor: int):
    tier = min(floor, 5)
    pool = ENEMIES[tier]
    name, base_hp, base_atk, icon = random.choice(pool)
    scale = 1 + (floor - 1) * 0.22
    hp = int(base_hp * scale)
    return {"name": f"{icon} {name}", "hp": hp, "max_hp": hp, "atk": int(base_atk * scale), "stunned": False, "sprite": icon}

def init_state():
    defaults = {
        'game_active': False, 'hero_class': None, 'hp': 100, 'max_hp': 100, 'mana': 50, 'max_mana': 50,
        'gold': 120, 'log': [{"t": "??:??", "msg": "O castelo aguarda...", "kind": ""}],
        'enemy': None, 'weapon': None, 'armor': None, 'floor': 1, 'kills': 0, 'state': 'menu',
        'arena_anim': ANIM_NONE, 'arena_dmg_hero': None, 'arena_dmg_enemy': None, 'arena_dmg_kind': '',
        'total_kills': 0, 'gold_earned': 0
    }
    for k, v in defaults.items():
        if k not in st.session_state: st.session_state[k] = v

init_state()

### ============================================================
### LÓGICA DE RENDERIZAÇÃO DA ARENA (CORREÇÃO DO ERRO AQUI)
### ============================================================
def render_arena(enemy=None):
    ss = st.session_state
    display_enemy = enemy if enemy else ss.get("enemy")
    
    # --- AJUSTE: Recuperando as variáveis do session_state para evitar NameError ---
    dmg_hero = ss.get('arena_dmg_hero')
    dmg_enemy = ss.get('arena_dmg_enemy')
    dmg_kind = ss.get('arena_dmg_kind', '')
    anim_cls = ss.get('arena_anim', ANIM_NONE)
    # ------------------------------------------------------------------------------

    dmg_html = ""
    # Agora dmg_enemy está definido no escopo
    if dmg_enemy is not None:
        dmg_html += f'<div class="dmg-number {dmg_kind}" style="right:22%;bottom:105px">-{dmg_enemy}</div>'
    
    if dmg_hero is not None:
        dmg_html += f'<div class="dmg-number dmg-hero" style="left:22%;bottom:105px">-{dmg_hero}</div>'

    st.markdown(f"""
    <div class="arena-frame {anim_cls}">
        {dmg_html}
        <div class="hero-sprite">🛡️</div>
        <div class="enemy-sprite">{'👹' if not display_enemy else display_enemy.get('sprite')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Limpa o estado de animação após renderizar
    ss.arena_anim = ANIM_NONE
    ss.arena_dmg_hero = None
    ss.arena_dmg_enemy = None
    ss.arena_dmg_kind = ""

### ============================================================
### TELAS DO JOGO
### ============================================================
def start_game(role: str):
    c = CLASSES[role]
    st.session_state.update({
        'game_active': True, 'hero_class': role, 'hp': c['hp'], 'max_hp': c['hp'],
        'mana': c['mana'], 'max_mana': c['mana'], 'weapon': dict(c['weapon']),
        'armor': dict(c['armor']), 'state': 'playing', 'floor': 1, 'enemy': spawn_enemy(1)
    })
    st.rerun()

def render_menu():
    st.markdown("<div class='castle-title'>Dark Castle</div>", unsafe_allow_html=True)
    for name, data in CLASSES.items():
        if st.button(f"Jogar como {name} {data['icon']}"):
            start_game(name)

def render_game():
    ss = st.session_state
    st.subheader(f"⚔️ ANDAR {ss.floor}")
    render_arena()
    if st.button("Atacar"):
        # Lógica de ataque simplificada para exemplo
        ss.arena_dmg_enemy = random.randint(10, 20)
        st.rerun()

# Roteador Principal [3]
state = st.session_state.state
if state == 'menu':
    render_menu()
elif state == 'playing':
    render_game()
