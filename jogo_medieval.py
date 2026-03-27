import streamlit as st
import streamlit.components.v1 as components
import random
import time

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Dark Castle: Ascensão",
    page_icon="🏰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS — VISUAL 3D / DARK FANTASY + ANIMAÇÕES DE COMBATE
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900&family=Cinzel:wght@400;600;700&family=UnifrakturMaguntia&display=swap');

:root {
  --gold:#c9a84c; --gold-lt:#f0d080; --red:#c0392b; --red-lt:#e74c3c;
  --blue:#2980b9; --cyan:#00e5ff; --green:#00ff88;
  --bg:#0a0608; --bg2:#120d10; --bg3:#1c1520; --border:#3a2a30;
  --text:#d4b896; --text-lt:#f0e0c8; --shadow:rgba(0,0,0,0.8);
}

html,body,[data-testid="stAppViewContainer"] {
    background-color: var(--bg);
    color: var(--text);
    font-family: 'Cinzel', serif;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }

/* Headers */
.castle-title {
    font-family: 'UnifrakturMaguntia', cursive;
    font-size: 4.2rem;
    text-align: center;
    color: var(--gold);
    text-shadow: 0 0 25px rgba(201,168,76,0.4), 3px 3px 2px #000;
    margin-bottom: -10px;
}
.castle-subtitle {
    font-family: 'Cinzel Decorative', serif;
    font-size: 1.1rem;
    text-align: center;
    color: #8a7040;
    letter-spacing: 0.4em;
    margin-bottom: 30px;
}

/* Cards */
.lore-card {
    background: linear-gradient(135deg, #1a1215 0%, #0d090a 100%);
    border: 1px solid var(--border);
    padding: 20px;
    border-radius: 4px;
    font-style: italic;
    font-size: 0.88rem;
    line-height: 1.6;
    color: #a08070;
    margin-bottom: 25px;
    position: relative;
    box-shadow: 0 10px 30px var(--shadow);
}
.lore-title {
    display: block;
    font-family: 'Cinzel Decorative', serif;
    font-size: 0.75rem;
    color: var(--gold);
    margin-bottom: 8px;
    letter-spacing: 0.1em;
}

.class-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    padding: 16px;
    border-radius: 8px;
    transition: 0.3s;
    text-align: center;
    height: 100%;
}
.class-card:hover { border-color: var(--gold); background: var(--bg3); }
.class-icon { font-size: 2.2rem; display: block; margin-bottom: 10px; }
.class-name { font-family: 'Cinzel Decorative', serif; color: var(--gold); font-size: 1.1rem; }
.class-desc { font-size: 0.72rem; color: #8a7060; margin: 10px 0; min-height: 40px; }

/* Stats Bars */
.cs-stat-row { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.cs-stat-label { font-size: 0.65rem; color: #6a5040; width: 65px; text-align: left; }
.cs-stat-bar-bg { flex: 1; height: 4px; background: rgba(0,0,0,0.4); border-radius: 2px; overflow: hidden; }
.cs-stat-bar-fill { height: 100%; background: var(--gold); border-radius: 2px; }

/* UI Elements */
.section-hdr {
    font-family: 'Cinzel Decorative', serif;
    font-size: 0.8rem;
    color: var(--gold);
    border-bottom: 1px solid var(--border);
    padding-bottom: 5px;
    margin: 25px 0 15px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.hero-3d {
    background: linear-gradient(180deg, #1c1518 0%, #0a0608 100%);
    border: 1px solid var(--border);
    border-top: 2px solid var(--gold);
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 15px 35px var(--shadow);
    margin-bottom: 20px;
}
.hero-name { font-family: 'Cinzel Decorative', serif; color: var(--gold); font-size: 1.1rem; }
.hero-gold { color: var(--gold-lt); font-weight: 700; font-size: 0.9rem; }

.stat-row { display: flex; align-items: center; gap: 12px; margin-top: 8px; }
.stat-label { font-size: 0.7rem; font-weight: 700; color: #8a7060; width: 45px; }
.bar-wrap { flex: 1; height: 10px; background: #1a1012; border-radius: 5px; border: 1px solid #302025; overflow: hidden; position: relative; }
.bar-fill-hp { height: 100%; background: linear-gradient(90deg, #7b0000, var(--red)); transition: 0.5s; }
.bar-fill-mp { height: 100%; background: linear-gradient(90deg, #004e7b, var(--blue)); transition: 0.5s; }
.stat-val { font-size: 0.75rem; color: var(--text-lt); min-width: 50px; text-align: right; }

.equip-row { display: flex; gap: 15px; margin-top: 15px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.05); }
.equip-val { font-size: 0.72rem; color: #a08070; }

/* Battle Progress */
.floor-wrapper { text-align: center; margin: 10px 0 25px; }
.floor-3d {
    font-family: 'Cinzel Decorative', serif;
    font-size: 1.4rem;
    color: var(--gold);
    background: rgba(201,168,76,0.05);
    padding: 5px 30px;
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 20px;
}

/* Log Style */
.log-wrap {
    background: rgba(0,0,0,0.3);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 12px;
    height: 140px;
    overflow-y: auto;
    font-size: 0.75rem;
}
.log-line { margin-bottom: 4px; border-bottom: 1px solid rgba(255,255,255,0.02); padding-bottom: 2px; }
.log-line.crit { color: var(--red-lt); font-weight: 700; }
.log-line.magic { color: var(--cyan); }
.log-line.loot { color: var(--gold); }

/* Buttons */
.stButton>button {
    width: 100%;
    background: linear-gradient(180deg, #2a1a1f 0%, #1a0f12 100%);
    color: var(--text);
    border: 1px solid var(--border);
    font-family: 'Cinzel', serif;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    transition: 0.2s;
}
.stButton>button:hover {
    border-color: var(--gold);
    color: var(--gold);
    box-shadow: 0 0 15px rgba(201,168,76,0.2);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 10px; background: transparent; }
.stTabs [data-baseweb="tab"] {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 4px 4px 0 0;
    padding: 10px 20px;
    color: #6a5040;
}
.stTabs [aria-selected="true"] {
    background: var(--bg3) !important;
    border-color: var(--gold) !important;
    color: var(--gold) !important;
}

/* Arena & Combat Visuals */
.enemy-stats-bar {
    display: flex; justify-content: space-between;
    background: rgba(0,0,0,0.5); border: 1px solid rgba(192,57,43,0.3);
    padding: 8px 15px; border-radius: 6px; margin-bottom: 15px;
    font-size: 0.8rem; color: var(--red-lt);
}
.stun-tag { color: #ffcc00; font-weight: 700; text-shadow: 0 0 8px rgba(255,204,0,0.5); }

/* Inventory/Market Items */
.inv-item, .mkt-item {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    padding: 10px; border-radius: 6px; margin-bottom: 8px;
    display: flex; align-items: center; gap: 12px;
}
.inv-item.rare, .mkt-item.rare { border-color: rgba(201,168,76,0.3); background: rgba(201,168,76,0.03); }
.inv-name, .mkt-name { font-family: 'Cinzel Decorative', serif; font-size: 0.85rem; }
.inv-attr, .mkt-sub { font-size: 0.68rem; color: #8a7060; }
.price-tag { font-family: 'Cinzel', serif; color: var(--gold); font-weight: 700; }

/* Game Over Screen */
.gameover-wrap { text-align: center; padding: 40px 20px; }
.gameover-title { font-family: 'UnifrakturMaguntia', cursive; font-size: 5rem; color: var(--red); text-shadow: 0 0 30px rgba(192,57,43,0.6); }
.gameover-stats { background: rgba(0,0,0,0.4); border: 1px solid var(--border); border-radius: 8px; padding: 20px; display: inline-block; margin-top: 20px; font-size: 0.9rem; }

.fury-badge {
    background: var(--red); color: white; font-size: 0.6rem; padding: 1px 5px;
    border-radius: 4px; margin-left: 8px; vertical-align: middle;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CONSTANTES & DATABASE
# ============================================================
ANIM_NONE = ""
ANIM_HERO_ATTACK = "anim-hero-attack"
ANIM_HERO_MAGIC = "anim-hero-magic"
ANIM_HERO_HIT = "anim-hero-hit"
ANIM_HERO_BLOCK = "anim-hero-block"
ANIM_HERO_DODGE = "anim-hero-dodge"
ANIM_HERO_DEATH = "anim-hero-death"
ANIM_HERO_FURY = "anim-hero-fury"
ANIM_ENEMY_HIT = "anim-enemy-hit"
ANIM_ENEMY_STUN = "anim-enemy-stun"
ANIM_ENEMY_DEATH = "anim-enemy-death"

CLASSES = {
    "Guerreiro": {
        "icon": "🛡️", "desc": "Mestre em defesa. Pode bloquear ataques.",
        "hp": 120, "mana": 30, "atk": 12, "def": 8,
        "stats": {"força": 4, "agilidade": 2, "magia": 1}
    },
    "Mago": {
        "icon": "🧙", "desc": "Poder destrutivo arcano. Usa mana para atacar.",
        "hp": 80, "mana": 100, "atk": 8, "def": 4,
        "stats": {"força": 1, "agilidade": 2, "magia": 5}
    },
    "Assassino": {
        "icon": "🗡️", "desc": "Rápido e letal. Alta chance de esquiva.",
        "hp": 90, "mana": 40, "atk": 15, "def": 3,
        "stats": {"força": 2, "agilidade": 5, "magia": 1}
    },
    "Berserker": {
        "icon": "🪓", "desc": "Fica mais forte quanto menos HP possui.",
        "hp": 150, "mana": 20, "atk": 14, "def": 5,
        "stats": {"força": 5, "agilidade": 1, "magia": 1}
    }
}

ENEMIES = {
    1: [("Rato de Esgoto", 40, 6, "🐀"), ("Esqueleto", 55, 9, "💀"), ("Slime", 45, 7, "🧪")],
    2: [("Zumbi", 80, 12, "🧟"), ("Aranha Gigante", 70, 15, "🕷️"), ("Gárgula", 95, 10, "🗿")],
    3: [("Cavaleiro Caído", 130, 18, "⚔️"), ("Súcubo", 110, 22, "😈"), ("Espectro", 100, 25, "👻")],
    4: [("Golem de Pedra", 220, 25, "🧱"), ("Lich", 160, 35, "💀🧙"), ("Vampiro", 180, 30, "🧛")],
    5: [("Dragão de Ossos", 500, 50, "🐉"), ("Rei Eterno", 700, 65, "👑")]
}

MARKET_POOL = {
    "weapon": [
        {"name": "Adaga Enferrujada", "atk": 3, "price": 25, "type": "weapon", "rarity": "comum"},
        {"name": "Espada Curta", "atk": 7, "price": 60, "type": "weapon", "rarity": "comum"},
        {"name": "Machado de Batalha", "atk": 12, "price": 120, "type": "weapon", "rarity": "raro", "value": 50},
        {"name": "Cajado Arcano", "atk": 15, "price": 200, "type": "weapon", "rarity": "raro", "value": 80},
        {"name": "Excalibur", "atk": 35, "price": 500, "type": "weapon", "rarity": "lendário", "value": 250},
    ],
    "armor": [
        {"name": "Trapos Velhos", "def": 2, "price": 20, "type": "armor", "rarity": "comum"},
        {"name": "Couro Batido", "def": 6, "price": 55, "type": "armor", "rarity": "comum"},
        {"name": "Cota de Malha", "def": 12, "price": 110, "type": "armor", "rarity": "raro", "value": 45},
        {"name": "Armadura de Placas", "def": 22, "price": 250, "type": "armor", "rarity": "raro", "value": 100},
        {"name": "Égide de Ouro", "def": 45, "price": 600, "type": "armor", "rarity": "lendário", "value": 300},
    ]
}

RARITY_COLORS = {"comum": "#d4b896", "raro": "#2980b9", "lendário": "#c9a84c"}

LORE_PER_FLOOR = {
    1: "O ar é úmido e cheira a mofo. Os primeiros degraus do castelo rangem sob seus pés.",
    2: "As tochas nas paredes queimam com uma chama azulada. O silêncio é interrompido por sussurros.",
    3: "O mármore negro do chão reflete sua angústia. O poder do Rei Eterno começa a pesar.",
    4: "Sangue escorre pelas fendas das paredes. Você ouve o bater de asas de horrores antigos.",
    5: "O Salão do Trono. A realidade se dobra. O fim da jornada está diante de você."
}

# Sons 8-bit Medievais
SOUNDS = {
    "start":   "https://cdn.pixabay.com/audio/2021/08/04/audio_0625c15139.mp3", # Game Start
    "attack":  "https://cdn.pixabay.com/audio/2022/03/15/audio_8b326c4a17.mp3", # 8-bit Sword
    "magic":   "https://cdn.pixabay.com/audio/2021/08/04/audio_12b0c7443c.mp3", # 8-bit Magic
    "loot":    "https://cdn.pixabay.com/audio/2021/08/04/audio_32cd7a2942.mp3", # 8-bit Coin
    "death":   "https://cdn.pixabay.com/audio/2021/08/04/audio_c40006960d.mp3", # 8-bit Death
    "victory": "https://cdn.pixabay.com/audio/2021/08/04/audio_7f61fd0296.mp3", # 8-bit Victory
    "bgm":     "https://cdn.pixabay.com/audio/2022/01/18/audio_d0a13f69d2.mp3", # Somber 8-bit Theme
    "click":   "https://cdn.pixabay.com/audio/2021/08/04/audio_1480909694.mp3", # UI Click
}

def play_sfx(key):
    if key in SOUNDS:
        st.session_state.sfx_trigger = key

def render_audio():
    ss = st.session_state
    # SFX Trigger - Um componente por gatilho para garantir execução
    if ss.get('sfx_trigger'):
        sfx_url = SOUNDS.get(ss.sfx_trigger)
        components.html(f"""
            <audio autoplay><source src="{sfx_url}" type="audio/mpeg"></audio>
        """, height=0, key=f"sfx_{time.time()}") # Key única para forçar render do som
        ss.sfx_trigger = None
    
    # BGM - Renderizada sempre que o jogo está ativo para não sumir do DOM
    if ss.get('game_active'):
        bgm_url = SOUNDS['bgm']
        components.html(f"""
            <audio id="bgm" autoplay loop><source src="{bgm_url}" type="audio/mpeg"></audio>
            <script>
                var audio = document.getElementById('bgm');
                audio.volume = 0.2;
            </script>
        """, height=0, key="bgm_component")
    else:
        ss.bgm_playing = False

# ============================================================
# HELPERS
# ============================================================
def log(msg: str, kind: str = ""):
    ts = time.strftime('%H:%M')
    st.session_state.log.insert(0, {"t": ts, "msg": msg, "kind": kind})
    if len(st.session_state.log) > 30:
        st.session_state.log.pop()

def reset_state():
    st.session_state.clear()

def spawn_enemy(floor: int):
    tier = min(floor, 5)
    pool = ENEMIES[tier]
    name, base_hp, base_atk, icon = random.choice(pool)
    scale = 1 + (floor - 1) * 0.22
    hp  = int(base_hp  * scale)
    atk = int(base_atk * scale)
    return {"name": f"{icon} {name}", "hp": hp, "max_hp": hp,
            "atk": atk, "stunned": False, "sprite": icon}

def generate_market():
    weapons = MARKET_POOL["weapon"]
    armors  = MARKET_POOL["armor"]
    floor   = st.session_state.floor
    w_w = [40, 30, 20, 7, 3] if floor >= 3 else [60, 30, 10, 0, 0]
    a_w = [50, 30, 15, 5]    if floor >= 3 else [70, 25, 5, 0]

    def pick(pool, weights):
        total = sum(weights[:len(pool)])
        r = random.randint(1, total); cum = 0
        for item, w in zip(pool, weights):
            cum += w
            if r <= cum:
                return dict(item)
        return dict(pool[-1])

    return [pick(weapons, w_w), pick(armors, a_w)]

def render_bar(pct, kind="hp"):
    pct = max(0.0, min(1.0, pct))
    return (f'<div class="bar-wrap">'
            f'<div class="bar-fill-{kind}" style="width:{pct*100:.1f}%"></div>'
            f'</div>')

def rarity_color(r):
    return RARITY_COLORS.get(r, "#d4b896")

def build_stat_bars(stats: dict) -> str:
    """Return HTML string for class stat bars — fully self-contained."""
    icons = {"força": "⚔️", "agilidade": "💨", "magia": "🔮"}
    html = ""
    for stat_name, val in stats.items():
        pct = int(val / 5 * 100)
        html += (
            f'<div class="cs-stat-row">'
            f'<span class="cs-stat-label">{icons.get(stat_name,"")} {stat_name}</span>'
            f'<div class="cs-stat-bar-bg">'
            f'<div class="cs-stat-bar-fill" style="width:{pct}%"></div>'
            f'</div></div>'
        )
    return html


# ============================================================
# INIT STATE
# ============================================================
def init_state():
    defaults = {
        'game_active': False, 'hero_class': None,
        'hp': 100, 'max_hp': 100, 'mana': 50, 'max_mana': 50, 'gold': 120,
        'log': [{"t": "??:??", "msg": "O castelo aguarda...", "kind": ""}],
        'enemy': None, 'weapon': None, 'armor': None,
        'floor': 1, 'kills': 0, 'kills_needed': 3,
        'inventory': [], 'state': 'menu', 'market_stock': [],
        'total_kills': 0, 'gold_earned': 0, 'blocked_last': False,
        'arena_anim': ANIM_NONE,
        'arena_dmg_hero': None,
        'arena_dmg_enemy': None,
        'arena_dmg_kind': '',
        'dying_enemy': None,
        'sfx_trigger': None,
        'bgm_playing': False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ============================================================
# SPRITE SYSTEM (CSS SHADOW PIXELS)
# ============================================================
def _hero_sprite_px(cls):
    if cls == "Guerreiro": return [[0,1,0],[1,1,1],[1,0,1]] # Dummy 3x3
    if cls == "Mago":      return [[0,1,1],[0,1,0],[1,1,1]]
    if cls == "Assassino": return [[1,0,1],[1,1,1],[0,1,0]]
    return [[1,1,1],[1,0,1],[1,1,1]] # Berserker

def _enemy_sprite_px(name):
    if "Dragão" in name: return [[1,1,1],[1,1,0],[1,0,0]]
    return [[0,1,0],[1,1,1],[0,1,0]]

def _px_to_shadow(px_map, size=3):
    shadows = []
    for y, row in enumerate(px_map):
        for x, val in enumerate(row):
            if val: shadows.append(f"{x*size}px {y*size}px 0 currentColor")
    return ",".join(shadows)

# ============================================================
# ARENA ENGINE (SVG/HTML ANIMATIONS)
# ============================================================
def render_arena(enemy):
    ss        = st.session_state
    anim_cls  = ss.get('arena_anim', ANIM_NONE)
    dmg_hero  = ss.get('arena_dmg_hero')
    dmg_enemy = ss.get('arena_dmg_enemy')
    dmg_kind  = ss.get('arena_dmg_kind', '')

    display_enemy = enemy or ss.get('dying_enemy')
    hero_hp_pct   = ss.hp / ss.max_hp
    enemy_hp_pct  = (max(0, display_enemy['hp']) / display_enemy['max_hp']) if display_enemy else 0

    SCALE = 3
    hero_shadow  = _px_to_shadow(_hero_sprite_px(ss.hero_class), SCALE)
    enemy_shadow = _px_to_shadow(_enemy_sprite_px(display_enemy['name'] if display_enemy else ""), SCALE) if display_enemy else ""

    enemy_name_clean = ""
    if display_enemy:
        parts = display_enemy['name'].split(' ', 1)
        enemy_name_clean = parts[1] if len(parts) > 1 else parts[0]

    dmg_html = ""
    if dmg_enemy is not None:
        color = "#00e5ff" if "magic" in dmg_kind else "#ff9944"
        dmg_html += f'<div class="dmg-num" style="right:20%;bottom:110px;color:{color}">-{dmg_enemy}</div>'
    if dmg_hero is not None:
        dmg_html += f'<div class="dmg-num" style="left:20%;bottom:110px;color:#ff4444">-{dmg_hero}</div>'

    stun_html = ""
    if display_enemy and display_enemy.get('stunned'):
        stun_html = '<div class="stun-pop" style="right:16%;bottom:155px">STUN!</div>'

    enemy_block = ""
    if display_enemy:
        ep = enemy_hp_pct * 100
        ehp_cur = max(0, display_enemy['hp'])
        ehp_max = display_enemy['max_hp']
        enemy_block = f"""
        <div class="hp-row">
          <span class="hp-lbl" style="color:#8a5050;text-align:right">{enemy_name_clean}</span>
          <div class="hp-track"><div class="hp-fill enemy-fill" style="width:{ep:.1f}%"></div></div>
          <span class="hp-val">{ehp_cur}/{ehp_max}</span>
        </div>
        <div class="sprite-wrap enemy-wrap">
          <div class="px-sprite sprite-enemy" style="box-shadow:{enemy_shadow}"></div>
          <div class="sprite-lbl" style="color:#e74c3c">{enemy_name_clean}</div>
        </div>"""

    hhp = hero_hp_pct * 100

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Cinzel:wght@600&display=swap');
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{background:transparent;overflow:hidden;}}
.arena{{
  position:relative;
  background:linear-gradient(180deg,#0d0508 0%,#1a0a10 60%,#0a0305 100%);
  border:1px solid rgba(192,57,43,.3);border-radius:14px;
  padding:14px 16px 0;overflow:hidden;height:230px;
  box-shadow:0 0 40px rgba(0,0,0,.9),inset 0 0 60px rgba(100,0,0,.1);
  font-family:'Cinzel',serif;
}}
.arena::before{{content:'';position:absolute;bottom:60px;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,rgba(201,168,76,.12),rgba(201,168,76,.22),rgba(201,168,76,.12),transparent);}}
.arena::after{{content:'';position:absolute;bottom:0;left:0;right:0;height:60px;
  background:linear-gradient(0deg,rgba(10,3,8,.95),transparent);pointer-events:none;z-index:2;}}
.hp-row{{display:flex;align-items:center;gap:8px;margin-bottom:5px;z-index:5;position:relative;}}
.hp-lbl{{font-size:10px;letter-spacing:.05em;color:#8a7060;min-width:80px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.hp-track{{flex:1;height:9px;background:rgba(255,255,255,.07);border-radius:5px;overflow:hidden;
  box-shadow:inset 0 2px 3px rgba(0,0,0,.6);}}
.hp-fill{{height:100%;border-radius:5px;transition:width .5s ease;}}
.hero-fill{{background:linear-gradient(90deg,#7b0000,#c0392b 60%,#e74c3c);box-shadow:0 0 6px rgba(192,57,43,.7);}}
.enemy-fill{{background:linear-gradient(90deg,#5a0000,#8b0000 60%,#b00000);box-shadow:0 0 6px rgba(139,0,0,.7);}}
.hp-val{{font-size:9px;color:#d4b896;min-width:52px;text-align:right;}}
.vs{{position:absolute;top:48%;left:50%;transform:translate(-50%,-50%);
  font-family:'Cinzel Decorative',serif;font-size:11px;color:rgba(201,168,76,.2);
  letter-spacing:.18em;z-index:1;}}
.px-sprite{{width:{SCALE}px;height:{SCALE}px;position:relative;image-rendering:pixelated;}}
.sprite-wrap{{position:absolute;bottom:60px;display:flex;flex-direction:column;align-items:center;gap:6px;z-index:3;}}
.hero-wrap{{left:13%;}}
.enemy-wrap{{right:13%;}}
.sprite-lbl{{font-family:'Cinzel Decorative',serif;font-size:9px;letter-spacing:.07em;
  white-space:nowrap;text-shadow:0 0 8px currentColor;}}
.hero-wrap .sprite-lbl{{color:#c9a84c;}}
.dmg-num{{position:absolute;font-family:'Cinzel Decorative',serif;font-weight:900;font-size:18px;
  pointer-events:none;z-index:20;animation:dmg-float 1s ease forwards;text-shadow:0 0 8px currentColor;}}
@keyframes dmg-float{{
  0%  {{opacity:1;transform:translateY(0) scale(1.2);}}
  40% {{opacity:1;transform:translateY(-22px) scale(1);}}
  80% {{opacity:.6;transform:translateY(-36px) scale(.85);}}
  100%{{opacity:0;transform:translateY(-48px) scale(.7);}}
}}
.stun-pop{{position:absolute;font-family:'Cinzel Decorative',serif;font-size:11px;
  color:#ffcc00;text-shadow:0 0 10px rgba(255,200,0,.8);
  animation:stun-float .8s ease forwards;z-index:20;}}
@keyframes stun-float{{0%{{opacity:1;transform:translateY(0) scale(1.1);}}100%{{opacity:0;transform:translateY(-28px) scale(.8);}}}}

/* ── HERO ANIMS ── */
.anim-hero-attack .sprite-hero{{animation:hero-slash .55s ease forwards;}}
@keyframes hero-slash{{0%{{transform:translateX(0) scaleX(1);}}25%{{transform:translateX(6px) scaleX(1.1);}}50%{{transform:translateX(55px) scaleX(1.15);}}70%{{transform:translateX(46px) scaleX(1.05);}}100%{{transform:translateX(0) scaleX(1);}}}}
.anim-hero-magic .sprite-hero{{animation:hero-cast .65s ease forwards;}}
@keyframes hero-cast{{0%{{transform:translateY(0) scale(1);filter:brightness(1);}}35%{{transform:translateY(-12px) scale(1.15);filter:brightness(2) hue-rotate(200deg);}}65%{{transform:translateY(-7px) scale(1.1);filter:brightness(1.7) hue-rotate(180deg);}}100%{{transform:translateY(0) scale(1);filter:brightness(1);}}}}
.anim-hero-fury .sprite-hero{{animation:fury-aura .5s ease forwards;}}
@keyframes fury-aura{{0%,100%{{filter:brightness(1);transform:scale(1);}}30%{{filter:brightness(2.5) sepia(1) hue-rotate(-20deg);transform:scale(1.18);}}60%{{filter:brightness(1.8) sepia(.8) hue-rotate(-10deg);transform:scale(1.1);}}}}
.anim-hero-hit .sprite-hero{{animation:hero-hurt .45s ease forwards;}}
@keyframes hero-hurt{{0%,100%{{transform:translateX(0);filter:brightness(1);}}15%{{transform:translateX(-10px);filter:brightness(3) sepia(1) hue-rotate(-30deg);}}35%{{transform:translateX(7px);}}55%{{transform:translateX(-5px);}}75%{{transform:translateX(3px);}}}}
.anim-hero-block .sprite-hero{{animation:hero-block .5s ease forwards;}}
@keyframes hero-block{{0%,100%{{transform:translateX(0);filter:brightness(1);}}30%{{transform:translateX(10px);filter:brightness(2) sepia(1) saturate(2);}}60%{{transform:translateX(5px);filter:brightness(1.4);}}}}
.anim-hero-dodge .sprite-hero{{animation:hero-dodge .5s ease forwards;}}
@keyframes hero-dodge{{0%{{transform:translate(0,0) rotate(0deg);}}30%{{transform:translate(-20px,-16px) rotate(-10deg);}}60%{{transform:translate(-13px,-8px) rotate(-5deg);}}100%{{transform:translate(0,0) rotate(0deg);}}}}
.anim-hero-death .sprite-hero{{animation:hero-die 1.1s ease forwards;}}
@keyframes hero-die{{0%{{transform:translate(0,0) rotate(0deg) scale(1);opacity:1;filter:brightness(1);}}20%{{transform:translate(0,-12px) rotate(-8deg) scale(1.06);filter:brightness(3) sepia(1) hue-rotate(-30deg);}}55%{{transform:translate(2px,5px) rotate(-25deg) scale(.9);opacity:.8;}}80%{{transform:translate(4px,15px) rotate(-55deg) scale(.65);opacity:.35;}}100%{{transform:translate(4px,22px) rotate(-90deg) scale(.25);opacity:0;}}}}

/* ── ENEMY ANIMS ── */
.anim-enemy-hit .sprite-enemy{{animation:enemy-hurt .45s ease forwards;}}
@keyframes enemy-hurt{{0%,100%{{transform:scaleX(-1);filter:brightness(1);}}15%{{transform:scaleX(-1) translateX(-8px);filter:brightness(3) sepia(1) hue-rotate(-30deg);}}35%{{transform:scaleX(-1) translateX(5px);}}55%{{transform:scaleX(-1) translateX(-4px);}}75%{{transform:scaleX(-1) translateX(2px);}}}}
.anim-enemy-stun .sprite-enemy{{animation:enemy-stun .65s ease forwards;}}
@keyframes enemy-stun{{0%,100%{{transform:scaleX(-1) rotate(0deg);}}20%{{transform:scaleX(-1) rotate(12deg) translateY(-5px);}}40%{{transform:scaleX(-1) rotate(-10deg) translateY(2px);}}60%{{transform:scaleX(-1) rotate(7deg);}}80%{{transform:scaleX(-1) rotate(-4deg);}}}}
.anim-enemy-death .sprite-enemy{{animation:enemy-die .9s ease forwards;}}
@keyframes enemy-die{{0%{{transform:scaleX(-1) scale(1) translateY(0);opacity:1;filter:brightness(1);}}20%{{transform:scaleX(-1) scale(1.18) translateY(-10px);filter:brightness(4) sepia(1) hue-rotate(-10deg);opacity:1;}}55%{{transform:scaleX(-1) scale(.8) translateY(5px) rotate(18deg);opacity:.7;}}80%{{transform:scaleX(-1) scale(.35) translateY(20px) rotate(45deg);opacity:.2;}}100%{{transform:scaleX(-1) scale(0) translateY(26px) rotate(65deg);opacity:0;}}}}

/* ── FLASH ── */
.flash{{position:absolute;inset:0;border-radius:14px;pointer-events:none;z-index:10;}}
.anim-hero-attack .flash,.anim-hero-fury .flash{{animation:fl-red .55s ease forwards;}}
.anim-hero-magic .flash{{animation:fl-blue .65s ease forwards;}}
.anim-hero-hit .flash,.anim-hero-death .flash{{animation:fl-dmg .5s ease forwards;}}
.anim-enemy-death .flash{{animation:fl-gold .9s ease forwards;}}
@keyframes fl-red{{0%,100%{{background:transparent;}}40%{{background:rgba(192,57,43,.15);}}}}
@keyframes fl-blue{{0%,100%{{background:transparent;}}40%{{background:rgba(0,229,255,.18);}}}}
@keyframes fl-dmg{{0%,100%{{background:transparent;}}30%{{background:rgba(220,20,20,.2);}}}}
@keyframes fl-gold{{0%,100%{{background:transparent;}}30%{{background:rgba(255,60,60,.2);}}50%{{background:rgba(201,168,76,.14);}}}}

/* magic bolt */
.magic-bolt{{display:none;position:absolute;bottom:78px;left:28%;
  width:8px;height:8px;border-radius:50%;background:#00e5ff;
  box-shadow:0 0 12px 4px rgba(0,229,255,.8);z-index:5;}}
.anim-hero-magic .magic-bolt{{display:block;animation:bolt .55s ease forwards;}}
@keyframes bolt{{0%{{transform:translateX(0) scale(.5);opacity:1;}}60%{{transform:translateX(150px) scale(1.4);opacity:1;}}100%{{transform:translateX(220px) scale(.2);opacity:0;}}}}
</style>
</head>
<body>
<div class="arena {anim_cls}">
  <div class="hp-row">
    <span class="hp-lbl">{ss.hero_class}</span>
    <div class="hp-track"><div class="hp-fill hero-fill" style="width:{hhp:.1f}%"></div></div>
    <span class="hp-val">{ss.hp}/{ss.max_hp}</span>
  </div>
  {enemy_block}
  <div class="vs">VS</div>
  <div class="sprite-wrap hero-wrap">
    <div class="px-sprite sprite-hero" style="box-shadow:{hero_shadow}"></div>
    <div class="sprite-lbl" style="color:#c9a84c">{ss.hero_class}</div>
  </div>
  <div class="magic-bolt"></div>
  <div class="flash"></div>
  {dmg_html}
  {stun_html}
</div>
</body></html>"""

    components.html(html, height=240, scrolling=False)

    ss.arena_anim      = ANIM_NONE
    ss.arena_dmg_hero  = None
    ss.arena_dmg_enemy = None
    ss.arena_dmg_kind  = ''
    ss.dying_enemy     = None

# ============================================================
# GAME LOGIC
# ============================================================
def start_game(cls_name):
    ss = st.session_state
    reset_state()
    init_state()
    ss.game_active = True
    ss.hero_class  = cls_name
    ss.hp          = CLASSES[cls_name]["hp"]
    ss.max_hp      = CLASSES[cls_name]["hp"]
    ss.mana        = CLASSES[cls_name]["mana"]
    ss.max_mana    = CLASSES[cls_name]["mana"]
    ss.weapon      = MARKET_POOL["weapon"][0]
    ss.armor       = MARKET_POOL["armor"][0]
    ss.state       = 'game'
    ss.market_stock = generate_market()
    log(f"⚔️ A jornada de {cls_name} começa!", "loot")
    play_sfx("start")

def player_attack(magic=False):
    ss = st.session_state
    en = ss.enemy
    if not en: return

    # Hero damage
    dmg = ss.weapon['atk'] + CLASSES[ss.hero_class]['atk']
    kind = 'physical'
    
    if magic:
        if ss.mana >= 15:
            ss.mana -= 15
            dmg += (CLASSES[ss.hero_class]['stats']['magia'] * 4)
            kind = 'magic'
            ss.arena_anim = ANIM_HERO_MAGIC
            play_sfx("magic")
        else:
            st.warning("Mana insuficiente!")
            return
    else:
        ss.arena_anim = ANIM_HERO_ATTACK
        play_sfx("attack")

    # Critical / Special Class Logic
    if ss.hero_class == "Berserker" and (ss.hp / ss.max_hp) < 0.2:
        dmg *= 2
        ss.arena_anim = ANIM_HERO_FURY
        log("🔥 FÚRIA ATIVADA!", "crit")

    # Apply damage
    en['hp'] -= dmg
    ss.arena_dmg_enemy = dmg
    ss.arena_dmg_kind  = kind
    log(f"💥 Você causou {dmg} de dano!", "magic" if magic else "")

    if en['hp'] <= 0:
        ss.arena_anim = ANIM_ENEMY_DEATH
        enemy_death()
    else:
        enemy_turn()

def enemy_turn():
    ss = st.session_state
    en = ss.enemy
    if not en or en.get('stunned'):
        if en.get('stunned'):
            en['stunned'] = False
            log(f"💫 {en['name']} está atordoado!", "magic")
        return

    # Enemy damage
    dmg = max(1, en['atk'] - (ss.armor['def'] + CLASSES[ss.hero_class]['def']))
    
    # Class Defenses
    blocked = False
    if ss.hero_class == "Guerreiro" and random.random() < 0.20:
        dmg = 0; blocked = True; ss.arena_anim = ANIM_HERO_BLOCK
        log("🛡️ BLOQUEADO!", "loot")
    elif ss.hero_class == "Assassino" and random.random() < 0.30:
        dmg = 0; blocked = True; ss.arena_anim = ANIM_HERO_DODGE
        log("💨 ESQUIVOU!", "loot")
    
    if not blocked:
        ss.hp -= dmg
        ss.arena_dmg_hero = dmg
        ss.arena_anim = ANIM_HERO_HIT
        log(f"🩸 {en['name']} atacou! -{dmg} HP", "crit")

    if ss.hp <= 0:
        ss.hp = 0
        ss.state = 'gameover'

def enemy_death():
    ss = st.session_state
    en = ss.enemy
    gold = 15 + (ss.floor * 10) + random.randint(0, 15)
    ss.gold += gold
    ss.gold_earned += gold
    ss.kills += 1
    ss.total_kills += 1
    ss.dying_enemy = en
    ss.enemy = None
    log(f"💀 {en['name']} derrotado! +{gold}G", "loot")
    play_sfx("victory")

    if ss.kills >= ss.kills_needed:
        ss.floor += 1
        ss.kills = 0
        ss.kills_needed = 3 + (ss.floor // 2)
        log(f"🏰 ANDAR {ss.floor} ALCANÇADO!", "loot")
        if ss.floor > 5:
            ss.state = 'victory'

# ============================================================
# ████████  RENDER MENU SCREEN  ████████
# ============================================================
def render_menu():
    st.markdown("<div class='castle-title'>Dark Castle</div>", unsafe_allow_html=True)
    st.markdown("<div class='castle-subtitle'>✦ Ascensão ✦</div>", unsafe_allow_html=True)
    st.markdown("""
<div class="lore-card">
  <span class="lore-title">📜 A Profecia</span>
  O Castelo das Sombras ergueu-se sobre os ossos de mil guerreiros.
  Cinco andares. Cinco horrores. No topo, o trono do Rei Eterno aguarda
  aquele que sobreviver. Nenhum sobreviveu. Ainda.
</div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-hdr'>Escolha sua linhagem</div>", unsafe_allow_html=True)

    cols = st.columns(2)
    for idx, (name, data) in enumerate(CLASSES.items()):
        with cols[idx % 2]:
            bars_html = build_stat_bars(data["stats"])
            # Single st.markdown call — no nested columns, no Streamlit parsing issues
            st.markdown(
                f'<div class="class-card">'
                f'<span class="class-icon">{data["icon"]}</span>'
                f'<div class="class-name">{name}</div>'
                f'<div class="class-desc">{data["desc"]}</div>'
                f'{bars_html}'
                f'</div>',
                unsafe_allow_html=True
            )
            if st.button(f"{data['icon']} Jogar como {name}", key=f"start_{name}"):
                start_game(name)


# ============================================================
# ████████  RENDER HERO PANEL  ████████
# ============================================================
def render_hero_panel():
    ss     = st.session_state
    hp_pct = ss.hp / ss.max_hp
    mp_pct = ss.mana / ss.max_mana
    is_fury = ss.hero_class == "Berserker" and hp_pct < 0.2
    w_col  = rarity_color(ss.weapon.get('rarity', 'comum'))
    a_col  = rarity_color(ss.armor.get('rarity', 'comum'))
    fury   = '<span class="fury-badge">⚡ FÚRIA</span>' if is_fury else ""

    st.markdown(f"""
<div class="hero-3d">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
    <span class="hero-name">{CLASSES[ss.hero_class]['icon']} {ss.hero_class.upper()} {fury}</span>
    <span class="hero-gold">💰 {ss.gold}G</span>
  </div>
  <div class="stat-row">
    <span class="stat-label">❤️ VIDA</span>
    {render_bar(hp_pct,'hp')}
    <span class="stat-val">{ss.hp}/{ss.max_hp}</span>
  </div>
  <div class="stat-row">
    <span class="stat-label">🔮 MANA</span>
    {render_bar(mp_pct,'mp')}
    <span class="stat-val">{ss.mana}/{ss.max_mana}</span>
  </div>
  <div class="equip-row">
    <span>⚔️ <span class="equip-val" style="color:{w_col}">{ss.weapon['name']} +{ss.weapon['atk']}</span></span>
    <span>🛡️ <span class="equip-val" style="color:{a_col}">{ss.armor['name']} +{ss.armor['def']}</span></span>
    <span style="margin-left:auto;color:#5a4030;font-size:.68rem">🏆 {ss.total_kills} abatidos</span>
  </div>
</div>""", unsafe_allow_html=True)


# ============================================================
# ████████  RENDER COMBAT TAB  ████████
# ============================================================
def render_combat():
    ss = st.session_state

    lore = LORE_PER_FLOOR.get(ss.floor, "")
    if lore:
        st.markdown(f"""<div style="font-style:italic;font-size:.72rem;color:#5a4030;
          border-left:2px solid rgba(201,168,76,.2);padding-left:10px;margin-bottom:14px">
          {lore}</div>""", unsafe_allow_html=True)

    prog = ss.kills / ss.kills_needed
    st.markdown(f"""
<div style="margin-bottom:12px">
  <div style="font-size:.68rem;color:#5a4030;letter-spacing:.1em;margin-bottom:4px">
    PROGRESSO DO ANDAR — {ss.kills}/{ss.kills_needed} abates
  </div>
  <div style="height:6px;background:rgba(255,255,255,.06);border-radius:3px;overflow:hidden">
    <div style="width:{prog*100:.0f}%;height:100%;
      background:linear-gradient(90deg,#3a7a3a,#00ff88);
      box-shadow:0 0 8px rgba(0,255,136,.5);border-radius:3px;transition:width .4s"></div>
  </div>
</div>""", unsafe_allow_html=True)

    if ss.enemy:
        en = ss.enemy
        render_arena(en)

        stun_tag = '<span class="stun-tag">⭐ ATORDOADO</span>' if en.get('stunned') else ""
        st.markdown(f"""<div class="enemy-stats-bar">
<span>{en['name']}</span>
<span>❤️ {max(0,en['hp'])}/{en['max_hp']}</span>
<span>⚔️ {en['atk']} ATK</span>
{stun_tag}
</div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("⚔️ ATACAR", key="btn_attack"):
                player_attack(magic=False)

        if ss.hero_class == "Mago":
            with c2:
                if st.button("🔥 MAGIA  (15 Mana)", key="btn_magic"):
                    player_attack(magic=True)
        else:
            skill_map = {
                "Guerreiro": "🛡️ BLOQUEIO  passivo 20%",
                "Berserker": "🔥 FÚRIA  passivo < 20% HP",
                "Assassino": "💨 ESQUIVA  passivo 30%",
            }
            with c2:
                st.markdown(f"""<div style="background:rgba(255,255,255,.03);border:1px solid rgba(201,168,76,.1);
border-radius:8px;padding:10px;text-align:center;font-size:.65rem;color:#5a4030">
{skill_map.get(ss.hero_class,'')}</div>""", unsafe_allow_html=True)
    else:
        render_arena(None)
        if st.button("👣 EXPLORAR A SALA", key="btn_explore"):
            if random.random() < 0.50:
                gain = 35 + ss.floor * 12 + random.randint(0, 18)
                ss.gold += gain; ss.gold_earned += gain
                log(f"🎁 Baú encontrado! +{gain}G", "loot")
                play_sfx("loot")
                if random.random() < 0.15:
                    item = random.choice(generate_market())
                    item["price"] = 0
                    ss.inventory.append(item)
                    log(f"✨ Item no baú: {item['name']}!", "loot")
            else:
                ss.enemy = spawn_enemy(ss.floor)
                log(f"⚠️ {ss.enemy['name']} aparece das sombras!", "crit")
                play_sfx("start")
            st.rerun()


# ============================================================
# ████████  RENDER INVENTORY TAB  ████████
# ============================================================
def render_inventory():
    ss = st.session_state
    st.markdown("<div class='section-hdr'>Itens Equipados</div>", unsafe_allow_html=True)
    w_col = rarity_color(ss.weapon.get('rarity','comum'))
    a_col = rarity_color(ss.armor.get('rarity','comum'))
    st.markdown(f"""
<div class="inv-item">
  <span style="font-size:1.2rem">⚔️</span>
  <div><div class="inv-name" style="color:{w_col}">{ss.weapon['name']}</div>
    <div class="inv-attr">+{ss.weapon['atk']} ATK · {ss.weapon.get('rarity','comum').upper()}</div></div>
</div>
<div class="inv-item">
  <span style="font-size:1.2rem">🛡️</span>
  <div><div class="inv-name" style="color:{a_col}">{ss.armor['name']}</div>
    <div class="inv-attr">+{ss.armor['def']} DEF · {ss.armor.get('rarity','comum').upper()}</div></div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-hdr' style='margin-top:14px'>Mochila</div>", unsafe_allow_html=True)
    if not ss.inventory:
        st.markdown('<div style="color:#5a4030;font-size:.78rem;padding:10px 0">— Mochila vazia —</div>', unsafe_allow_html=True)
        return

    for i, item in enumerate(ss.inventory):
        r       = item.get('rarity','comum')
        col     = rarity_color(r)
        attr    = f"+{item['atk']} ATK" if item['type']=='weapon' else f"+{item['def']} DEF"
        icon    = "⚔️" if item['type']=='weapon' else "🛡️"
        rare_c  = "rare" if r in ('raro','lendário') else ""
        st.markdown(f"""
<div class="inv-item {rare_c}">
  <span style="font-size:1.1rem">{icon}</span>
  <div style="flex:1"><div class="inv-name" style="color:{col}">{item['name']}</div>
    <div class="inv-attr">{attr} · {r.upper()}</div></div>
  <div class="inv-val">⚖️ {item.get('value',0)}G</div>
</div>""", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Equipar", key=f"equip_{i}"):
                old = ss[item['type']]
                ss[item['type']] = item
                ss.inventory[i] = old
                log(f"🔄 Equipou: {item['name']}!", "")
                play_sfx("click")
                st.rerun()
        with c2:
            sv = item.get('value', 10)
            if st.button(f"Vender +{sv}G", key=f"sell_inv_{i}"):
                ss.gold += sv
                ss.inventory.pop(i)
                log(f"💰 Vendeu {item['name']} por {sv}G", "loot")
                st.rerun()


# ============================================================
# ████████  RENDER MARKET TAB  ████████
# ============================================================
def render_market():
    ss = st.session_state
    if not ss.market_stock:
        ss.market_stock = generate_market()

    st.markdown("<div class='section-hdr'>Poções</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("❤️ Vida +50 HP\n(40G)", key="pot_hp"):
            if ss.gold >= 40:
                ss.gold -= 40
                healed = min(ss.max_hp, ss.hp+50)-ss.hp
                ss.hp += healed
                log(f"❤️ Poção de vida: +{healed} HP", "loot")
                st.rerun()
            else:
                st.warning("Ouro insuficiente!")
    with c2:
        if st.button("🔮 Mana +40\n(40G)", key="pot_mp"):
            if ss.gold >= 40:
                ss.gold -= 40
                restored = min(ss.max_mana, ss.mana+40)-ss.mana
                ss.mana += restored
                log(f"🔮 Poção de mana: +{restored} Mana", "magic")
                st.rerun()
            else:
                st.warning("Ouro insuficiente!")

    st.markdown("<div class='section-hdr' style='margin-top:14px'>Equipamentos</div>", unsafe_allow_html=True)
    for i, item in enumerate(ss.market_stock):
        r       = item.get('rarity','comum')
        col     = rarity_color(r)
        attr    = f"+{item['atk']} ATK" if item['type']=='weapon' else f"+{item['def']} DEF"
        icon    = "⚔️" if item['type']=='weapon' else "🛡️"
        rare_c  = "rare" if r in ('raro','lendário') else ""
        badge   = (f'<span style="background:{col};color:#000;font-size:.6rem;'
                   f'padding:1px 6px;border-radius:8px;font-weight:700">{r.upper()}</span>'
                   if r != "comum" else "")
        st.markdown(f"""
<div class="mkt-item {rare_c}">
  <div style="display:flex;justify-content:space-between;align-items:flex-start">
    <div class="mkt-name" style="color:{col}">{icon} {item['name']} {badge}</div>
    <div class="price-tag">💰 {item['price']}G</div>
  </div>
  <div class="mkt-sub">{attr}</div>
</div>""", unsafe_allow_html=True)
        if st.button(f"Comprar {item['name']}", key=f"buy_{i}"):
            if ss.gold >= item['price']:
                ss.gold -= item['price']
                ss.inventory.append(dict(item))
                ss.market_stock.pop(i)
                log(f"🛒 Comprou: {item['name']}!", "loot")
                play_sfx("loot")
                if not ss.market_stock:
                    ss.market_stock = generate_market()
                st.rerun()
            else:
                st.warning("Ouro insuficiente!")

    st.markdown("<div class='section-hdr' style='margin-top:14px'>Vender Inventário</div>", unsafe_allow_html=True)
    if not ss.inventory:
        st.markdown('<div style="color:#5a4030;font-size:.78rem">— Nada para vender —</div>', unsafe_allow_html=True)
    else:
        for i, item in enumerate(ss.inventory):
            sv = item.get('value', 10)
            if st.button(f"Vender {item['name']} (+{sv}G)", key=f"sell_mkt_{i}"):
                ss.gold += sv
                ss.inventory.pop(i)
                log(f"💰 Vendeu {item['name']} por {sv}G", "loot")
                st.rerun()


# ============================================================
# ████████  RENDER LOG  ████████
# ============================================================
def render_log():
    lines = st.session_state.log[:6]
    items = "".join(
        f'<div class="log-line {e.get("kind","")}">[{e["t"]}] {e["msg"]}</div>'
        for e in lines
    )
    st.markdown(f'<div class="log-wrap">{items}</div>', unsafe_allow_html=True)


# ============================================================
# ████████  MAIN GAME SCREEN  ████████
# ============================================================
def render_game():
    ss = st.session_state
    st.markdown(f'<div class="floor-wrapper"><span class="floor-3d">⚔️ ANDAR {ss.floor} ⚔️</span></div>',
                unsafe_allow_html=True)
    render_hero_panel()
    tab_c, tab_i, tab_m = st.tabs(["⚔️  COMBATE", "🎒  MOCHILA", "🛒  MERCADO"])
    with tab_c: render_combat()
    with tab_i: render_inventory()
    with tab_m: render_market()
    render_log()


# ============================================================
# ████████  GAME OVER  ████████
# ============================================================
def render_gameover():
    ss = st.session_state
    # Show death arena with hero dying animation
    ss.arena_anim = ANIM_HERO_DEATH
    render_arena(None)
    play_sfx("death")

    st.markdown(f"""
<div class="gameover-wrap">
  <div class="gameover-title">Game Over</div>
  <div style="font-family:'Cinzel',serif;color:#7a4040;font-size:.82rem;margin:8px 0 20px">
    O castelo devorou mais uma alma.
  </div>
  <div class="gameover-stats">
    <div>🏰 Andar alcançado: <b style="color:var(--gold)">{ss.floor}</b></div>
    <div>⚔️ Inimigos abatidos: <b style="color:var(--gold)">{ss.total_kills}</b></div>
    <div>💰 Ouro acumulado: <b style="color:var(--gold)">{ss.gold_earned}G</b></div>
    <div>🧙 Classe: <b style="color:var(--gold)">{ss.hero_class}</b></div>
  </div>
</div>""", unsafe_allow_html=True)

    if st.button("🔄 RECOMEÇAR A JORNADA"):
        reset_state(); st.rerun()


# ============================================================
# ████████  VICTORY  ████████
# ============================================================
def render_victory():
    ss = st.session_state
    play_sfx("victory")
    st.markdown(f"""
<div class="gameover-wrap">
  <div style="font-family:'UnifrakturMaguntia',cursive;font-size:3.6rem;
    color:#c9a84c;text-shadow:0 0 30px rgba(201,168,76,.8)">Vitória!</div>
  <div style="font-family:'Cinzel',serif;color:#8a7040;font-size:.82rem;margin:8px 0 20px">
    O trono do Rei Eterno é seu. O castelo inclina sua coroa.
  </div>
  <div class="gameover-stats">
    <div>⚔️ Inimigos abatidos: <b style="color:var(--gold)">{ss.total_kills}</b></div>
    <div>💰 Ouro acumulado: <b style="color:var(--gold)">{ss.gold_earned}G</b></div>
    <div>🧙 Classe: <b style="color:var(--gold)">{ss.hero_class}</b></div>
  </div>
</div>""", unsafe_allow_html=True)

    if st.button("🏆 JOGAR NOVAMENTE"):
        reset_state(); st.rerun()


# ============================================================
# MAIN LOOP
# ============================================================
if st.session_state.state == 'menu':
    render_menu()
elif st.session_state.state == 'game':
    render_game()
elif st.session_state.state == 'gameover':
    render_gameover()
elif st.session_state.state == 'victory':
    render_victory()

# Audio Engine Call
render_audio()
