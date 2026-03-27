import streamlit as st
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
# CSS — VISUAL 3D / DARK FANTASY
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900&family=Cinzel:wght@400;600;700&family=UnifrakturMaguntia&display=swap');

/* ── BASE ── */
:root {
  --gold:    #c9a84c;
  --gold-lt: #f0d080;
  --red:     #c0392b;
  --red-lt:  #e74c3c;
  --blue:    #2980b9;
  --cyan:    #00e5ff;
  --green:   #00ff88;
  --bg:      #0a0608;
  --bg2:     #120d10;
  --bg3:     #1c1520;
  --border:  #3a2a30;
  --text:    #d4b896;
  --text-lt: #f0e0c8;
  --shadow:  rgba(0,0,0,0.8);
}

html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--bg) !important;
  color: var(--text);
  font-family: 'Cinzel', serif;
}

[data-testid="stAppViewContainer"] {
  background-image:
    radial-gradient(ellipse 80% 60% at 50% 0%, rgba(100,20,20,0.18) 0%, transparent 70%),
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(255,255,255,0.012) 2px,
      rgba(255,255,255,0.012) 4px
    );
}

/* hide Streamlit chrome */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }
[data-testid="block-container"] { padding: 1.5rem 1rem 3rem; max-width: 820px; margin: auto; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: var(--bg2); border-radius: 8px; padding: 4px; }
.stTabs [data-baseweb="tab"] {
  font-family: 'Cinzel', serif; font-size: 0.78rem; letter-spacing: .08em;
  color: var(--text); background: transparent; border-radius: 6px; padding: 8px 14px;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, #3a1a1a, #2a1020) !important;
  color: var(--gold) !important;
  box-shadow: inset 0 1px 0 rgba(201,168,76,.3), 0 0 12px rgba(201,168,76,.15);
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1rem; }

div[data-testid="stButton"] > button {
  font-family: 'Cinzel', serif !important;
  font-weight: 700 !important;
  letter-spacing: .08em !important;
  text-transform: uppercase;
  font-size: 0.72rem !important;
  width: 100% !important;
  padding: 10px 8px !important;
  border-radius: 6px !important;
  transition: all .2s ease !important;
}

/* divider */
hr { border-color: var(--border) !important; margin: 12px 0 !important; }

/* progress bar (enemy HP) */
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, #8b0000, #c0392b, #e74c3c) !important;
  box-shadow: 0 0 8px rgba(231,76,60,.6);
}
.stProgress > div > div { background: rgba(255,255,255,0.07) !important; border-radius: 4px; }

/* warnings */
.stWarning { background: rgba(201,168,76,.1) !important; border-color: var(--gold) !important; }

/* ── 3D TITLE ── */
.castle-title {
  font-family: 'UnifrakturMaguntia', cursive;
  font-size: clamp(2.6rem, 8vw, 4.8rem);
  text-align: center;
  line-height: 1.1;
  margin: 0 0 4px;
  background: linear-gradient(180deg, #f0d080 0%, #c9a84c 40%, #7a5a20 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 2px 6px rgba(201,168,76,.5)) drop-shadow(0 4px 18px rgba(0,0,0,.9));
  text-shadow: none;
  letter-spacing: .04em;
}
.castle-subtitle {
  font-family: 'Cinzel', serif;
  font-size: .82rem; letter-spacing: .35em; text-transform: uppercase;
  color: #7a6040; text-align: center; margin-bottom: 28px;
}

/* ── 3D FLOOR BADGE ── */
.floor-3d {
  display: inline-block;
  font-family: 'Cinzel Decorative', serif;
  font-size: 1.05rem; font-weight: 900;
  letter-spacing: .12em; text-transform: uppercase;
  color: #0a0608;
  background: linear-gradient(180deg, #f0d080 0%, #c9a84c 50%, #7a5a20 100%);
  padding: 8px 28px;
  border-radius: 40px;
  box-shadow:
    0 2px 0 #3a2a00,
    0 4px 0 #2a1a00,
    0 6px 0 #1a0a00,
    0 8px 0 rgba(0,0,0,.5),
    0 12px 24px rgba(0,0,0,.7),
    inset 0 1px 0 rgba(255,255,240,.5);
  transform: perspective(200px) rotateX(8deg);
  text-shadow: 0 1px 2px rgba(255,255,200,.4);
}
.floor-wrapper { text-align: center; margin-bottom: 20px; }

/* ── 3D HERO PANEL ── */
.hero-3d {
  background:
    linear-gradient(135deg, rgba(60,20,20,.95) 0%, rgba(25,12,18,.95) 100%);
  border: 1px solid rgba(201,168,76,.3);
  border-radius: 12px;
  padding: 18px 20px;
  margin-bottom: 16px;
  position: relative;
  overflow: hidden;
  box-shadow:
    0 1px 0 rgba(201,168,76,.2) inset,
    0 -1px 0 rgba(0,0,0,.6) inset,
    6px 6px 20px rgba(0,0,0,.7),
    -1px -1px 0 rgba(201,168,76,.1);
}
.hero-3d::before {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(201,168,76,.06) 0%, transparent 60%);
  pointer-events: none;
}
.hero-3d::after {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(201,168,76,.5), transparent);
}
.hero-name {
  font-family: 'Cinzel Decorative', serif;
  font-size: .95rem; font-weight: 700; letter-spacing: .1em;
  color: var(--gold-lt);
  text-shadow: 0 0 12px rgba(201,168,76,.5);
}
.hero-gold {
  font-family: 'Cinzel', serif; font-weight: 700;
  color: var(--gold-lt); font-size: .95rem;
}
.stat-row { display: flex; align-items: center; gap: 10px; margin: 6px 0; }
.stat-label { font-size: .72rem; letter-spacing: .1em; color: #8a7060; min-width: 50px; }
.bar-wrap {
  flex: 1; height: 12px; background: rgba(255,255,255,.07);
  border-radius: 6px; overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0,0,0,.6), 0 1px 0 rgba(255,255,255,.05);
}
.bar-fill-hp {
  height: 100%; border-radius: 6px;
  background: linear-gradient(90deg, #7b0000, #c0392b 60%, #ff6b6b);
  box-shadow: 0 0 8px rgba(192,57,43,.7);
  transition: width .4s ease;
}
.bar-fill-mp {
  height: 100%; border-radius: 6px;
  background: linear-gradient(90deg, #003070, #2980b9 60%, #5dade2);
  box-shadow: 0 0 8px rgba(41,128,185,.7);
  transition: width .4s ease;
}
.stat-val { font-size: .76rem; color: var(--text); min-width: 60px; text-align: right; }
.equip-row {
  margin-top: 12px; padding-top: 10px;
  border-top: 1px solid rgba(201,168,76,.15);
  display: flex; gap: 16px; font-size: .72rem; color: #8a7060;
}
.equip-val { color: var(--text); font-weight: 600; }
.equip-val.rare { color: var(--cyan); text-shadow: 0 0 8px rgba(0,229,255,.5); }
.fury-badge {
  display: inline-block;
  background: linear-gradient(135deg, #8b0000, #c0392b);
  color: #fff; font-size: .62rem; font-weight: 700; letter-spacing: .12em;
  padding: 2px 8px; border-radius: 10px;
  box-shadow: 0 0 10px rgba(192,57,43,.8);
  animation: pulse-red 1s ease-in-out infinite;
}
@keyframes pulse-red {
  0%,100% { box-shadow: 0 0 8px rgba(192,57,43,.8); }
  50%      { box-shadow: 0 0 18px rgba(255,80,80,1); }
}

/* ── 3D ENEMY CARD ── */
.enemy-3d {
  background: linear-gradient(135deg, rgba(40,10,10,.97), rgba(20,8,12,.97));
  border: 1px solid rgba(192,57,43,.35);
  border-radius: 12px; padding: 18px 20px; margin-bottom: 14px;
  position: relative; overflow: hidden;
  box-shadow:
    inset 0 1px 0 rgba(231,76,60,.15),
    8px 8px 24px rgba(0,0,0,.8),
    0 0 40px rgba(192,57,43,.08);
}
.enemy-3d::after {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(231,76,60,.4), transparent);
}
.enemy-name {
  font-family: 'Cinzel Decorative', serif;
  font-size: 1rem; font-weight: 700; color: #e74c3c;
  text-shadow: 0 0 14px rgba(231,76,60,.6);
  margin-bottom: 6px;
}
.enemy-hp-wrap {
  height: 14px; background: rgba(255,255,255,.06); border-radius: 7px;
  overflow: hidden; margin-bottom: 6px;
  box-shadow: inset 0 2px 4px rgba(0,0,0,.7);
}
.enemy-hp-fill {
  height: 100%; border-radius: 7px;
  background: linear-gradient(90deg, #6b0000, #c0392b 50%, #ff4444);
  box-shadow: 0 0 10px rgba(255,68,68,.6);
  transition: width .4s ease;
}
.enemy-stats { font-size: .72rem; color: #8a5050; margin-top: 4px; }

/* ── 3D BUTTONS ── */
.btn-attack div[data-testid="stButton"] > button {
  background: linear-gradient(180deg, #6b1a1a 0%, #3d0e0e 50%, #2a0808 100%) !important;
  color: #ff9999 !important; border: 1px solid rgba(192,57,43,.5) !important;
  box-shadow: 0 4px 0 #1a0404, 0 5px 8px rgba(0,0,0,.6),
              inset 0 1px 0 rgba(255,100,100,.2) !important;
}
.btn-attack div[data-testid="stButton"] > button:hover {
  transform: translateY(1px) !important;
  box-shadow: 0 3px 0 #1a0404, 0 4px 6px rgba(0,0,0,.6) !important;
}
.btn-magic div[data-testid="stButton"] > button {
  background: linear-gradient(180deg, #0d2a4a 0%, #071a30 50%, #040f1c 100%) !important;
  color: #5dade2 !important; border: 1px solid rgba(41,128,185,.4) !important;
  box-shadow: 0 4px 0 #020810, 0 5px 8px rgba(0,0,0,.6),
              inset 0 1px 0 rgba(100,180,255,.15) !important;
}
.btn-explore div[data-testid="stButton"] > button {
  background: linear-gradient(180deg, #1a3a1a 0%, #0d200d 50%, #071407 100%) !important;
  color: #00ff88 !important; border: 1px solid rgba(0,200,100,.3) !important;
  box-shadow: 0 4px 0 #030a03, 0 5px 8px rgba(0,0,0,.6),
              inset 0 1px 0 rgba(0,255,100,.1) !important;
  font-size: .8rem !important; padding: 14px 8px !important;
}
.btn-gold div[data-testid="stButton"] > button {
  background: linear-gradient(180deg, #3a2a08 0%, #241a05 50%, #160f03 100%) !important;
  color: var(--gold-lt) !important; border: 1px solid rgba(201,168,76,.3) !important;
  box-shadow: 0 4px 0 #0a0601, 0 5px 8px rgba(0,0,0,.6),
              inset 0 1px 0 rgba(201,168,76,.2) !important;
}
.btn-danger div[data-testid="stButton"] > button {
  background: linear-gradient(180deg, #4a0a0a 0%, #2a0505 100%) !important;
  color: #ff6b6b !important; border: 1px solid rgba(192,57,43,.4) !important;
}

/* ── CLASS CARDS ── */
.class-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 16px 0; }
.class-card {
  background: linear-gradient(135deg, rgba(40,20,20,.9), rgba(20,10,15,.9));
  border: 1px solid rgba(201,168,76,.2); border-radius: 12px; padding: 18px 16px;
  position: relative; overflow: hidden;
  box-shadow: 4px 4px 16px rgba(0,0,0,.7), inset 0 1px 0 rgba(201,168,76,.1);
  transition: all .25s ease; cursor: pointer;
}
.class-card::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(circle at 30% 30%, rgba(201,168,76,.06), transparent 60%);
}
.class-icon { font-size: 2.2rem; margin-bottom: 8px; display: block; }
.class-name {
  font-family: 'Cinzel Decorative', serif; font-size: .82rem;
  color: var(--gold-lt); font-weight: 700; letter-spacing: .08em;
  margin-bottom: 6px;
}
.class-desc { font-size: .68rem; color: #8a7060; line-height: 1.5; }
.class-stat { display: flex; align-items: center; gap: 6px; margin-top: 8px; }
.cs-bar { flex: 1; height: 4px; background: rgba(255,255,255,.08); border-radius: 2px; overflow: hidden; }
.cs-fill { height: 100%; border-radius: 2px; }

/* ── LORE CARD ── */
.lore-card {
  background: linear-gradient(135deg, rgba(20,12,8,.95), rgba(12,8,10,.95));
  border: 1px solid rgba(201,168,76,.15);
  border-radius: 10px; padding: 20px 22px; margin: 16px 0;
  font-size: .78rem; color: #8a7060; line-height: 1.75;
  box-shadow: inset 0 0 60px rgba(0,0,0,.4);
  font-style: italic;
}
.lore-title {
  font-family: 'Cinzel Decorative', serif; font-size: .82rem;
  color: var(--gold); font-style: normal; letter-spacing: .1em;
  margin-bottom: 10px; display: block;
}

/* ── INVENTORY ITEM ── */
.inv-item {
  background: rgba(30,18,22,.8);
  border: 1px solid rgba(201,168,76,.15); border-radius: 8px;
  padding: 10px 14px; margin-bottom: 8px;
  display: flex; align-items: center; gap: 10px;
  box-shadow: 2px 2px 8px rgba(0,0,0,.5);
}
.inv-item.rare { border-color: rgba(0,229,255,.35); box-shadow: 0 0 12px rgba(0,229,255,.1), 2px 2px 8px rgba(0,0,0,.5); }
.inv-name { flex: 1; font-size: .78rem; color: var(--text-lt); }
.inv-name.rare { color: var(--cyan); text-shadow: 0 0 8px rgba(0,229,255,.4); }
.inv-attr { font-size: .7rem; color: #8a7060; }
.inv-val { font-size: .7rem; color: var(--gold); }

/* ── MARKET ITEM ── */
.mkt-item {
  background: rgba(25,15,18,.9);
  border: 1px solid rgba(201,168,76,.18); border-radius: 8px;
  padding: 12px 14px; margin-bottom: 10px;
  box-shadow: 3px 3px 10px rgba(0,0,0,.6);
  position: relative; overflow: hidden;
}
.mkt-item.rare {
  border-color: rgba(0,229,255,.4);
  box-shadow: 0 0 16px rgba(0,229,255,.12), 3px 3px 10px rgba(0,0,0,.6);
}
.mkt-item::after {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(201,168,76,.3), transparent);
}
.mkt-name { font-size: .82rem; color: var(--text-lt); font-weight: 600; margin-bottom: 4px; }
.mkt-name.rare { color: var(--cyan); text-shadow: 0 0 8px rgba(0,229,255,.5); }
.mkt-sub { font-size: .7rem; color: #7a6050; margin-bottom: 8px; }
.price-tag {
  display: inline-block; background: linear-gradient(135deg, #3a2a08, #1a1203);
  border: 1px solid rgba(201,168,76,.3); border-radius: 12px;
  padding: 2px 10px; font-size: .72rem; color: var(--gold-lt);
  margin-bottom: 8px;
}

/* ── LOG ── */
.log-wrap {
  background: rgba(10,6,8,.9);
  border: 1px solid rgba(201,168,76,.1); border-radius: 8px;
  padding: 12px 14px; margin-top: 14px;
  max-height: 120px; overflow-y: auto;
}
.log-line {
  font-size: .72rem; color: #7a6858; line-height: 1.8;
  border-bottom: 1px solid rgba(255,255,255,.04); padding-bottom: 2px;
}
.log-line:first-child { color: var(--text); }
.log-line.crit { color: #e74c3c; }
.log-line.loot { color: var(--gold); }
.log-line.level { color: var(--green); }
.log-line.magic { color: #5dade2; }

/* ── GAME OVER ── */
.gameover-wrap { text-align: center; padding: 40px 20px; }
.gameover-title {
  font-family: 'UnifrakturMaguntia', cursive;
  font-size: 4rem; color: #c0392b;
  text-shadow: 0 0 30px rgba(192,57,43,.8), 0 0 60px rgba(192,57,43,.4);
  animation: flicker 2s ease-in-out infinite;
}
@keyframes flicker {
  0%,100% { opacity: 1; } 45% { opacity: .9; } 50% { opacity: .6; } 55% { opacity: .9; }
}
.gameover-stats {
  background: rgba(20,10,12,.9); border: 1px solid rgba(192,57,43,.3);
  border-radius: 10px; padding: 20px; margin: 20px auto; max-width: 320px;
  font-size: .82rem; line-height: 2;
}

/* ── CHEST ANIMATION ── */
.chest-reveal {
  text-align: center; padding: 20px;
  font-family: 'Cinzel Decorative', serif;
  font-size: 1rem; color: var(--gold-lt);
  text-shadow: 0 0 20px rgba(201,168,76,.7);
}

/* ── SECTION HEADER ── */
.section-hdr {
  font-family: 'Cinzel Decorative', serif;
  font-size: .72rem; letter-spacing: .2em; text-transform: uppercase;
  color: #5a4030; margin-bottom: 10px; margin-top: 4px;
  border-bottom: 1px solid rgba(201,168,76,.1); padding-bottom: 6px;
}

/* ── POTION ROW ── */
.pot-row { display: flex; gap: 8px; margin-bottom: 12px; }
.pot-row > div { flex: 1; }

/* scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(201,168,76,.3); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# CONSTANTES E DADOS
# ============================================================

CLASSES = {
    "Guerreiro": {
        "icon": "🛡️",
        "hp": 180, "mana": 30, "atk": 14, "def_val": 9,
        "weapon": {"name": "Espada Curta", "atk": 14, "type": "weapon", "rarity": "comum", "value": 30},
        "armor":  {"name": "Cota de Ferro", "def": 9, "type": "armor",  "rarity": "comum", "value": 25},
        "desc": "Resistência incomparável. Bloqueia 20% de todo dano recebido.",
        "special": "block",
        "stats": {"força": 4, "agilidade": 2, "magia": 1},
        "lore": "Forjado nas guerras do norte, suportou o que nenhum outro sobreviveu."
    },
    "Mago": {
        "icon": "🔮",
        "hp": 90, "mana": 140, "atk": 10, "def_val": 3,
        "weapon": {"name": "Cajado Aprendiz", "atk": 10, "type": "weapon", "rarity": "comum", "value": 30},
        "armor":  {"name": "Manto de Linho",  "def": 3,  "type": "armor",  "rarity": "comum", "value": 20},
        "desc": "Devastação arcana. Itens RAROS amplificam magias em +70%.",
        "special": "magic",
        "stats": {"força": 1, "agilidade": 2, "magia": 5},
        "lore": "Banido da Academia Arcana por estudar feitiços proibidos."
    },
    "Berserker": {
        "icon": "🪓",
        "hp": 220, "mana": 20, "atk": 12, "def_val": 4,
        "weapon": {"name": "Machado Gasto", "atk": 12, "type": "weapon", "rarity": "comum", "value": 30},
        "armor":  {"name": "Pelagem Grossa", "def": 4,  "type": "armor",  "rarity": "comum", "value": 20},
        "desc": "Fúria incontrolável. Abaixo de 20% de vida: +90% de dano.",
        "special": "fury",
        "stats": {"força": 5, "agilidade": 3, "magia": 0},
        "lore": "Enlouqueceu ao ver sua aldeia queimar. A dor virou poder."
    },
    "Assassino": {
        "icon": "🗡️",
        "hp": 115, "mana": 55, "atk": 18, "def_val": 2,
        "weapon": {"name": "Adagas Duplas", "atk": 18, "type": "weapon", "rarity": "comum", "value": 30},
        "armor":  {"name": "Couro Negro",   "def": 2,  "type": "armor",  "rarity": "comum", "value": 20},
        "desc": "Letal e evasivo. 30% esquiva, 25% atordoamento (stun).",
        "special": "stun",
        "stats": {"força": 3, "agilidade": 5, "magia": 2},
        "lore": "Ninguém sabe seu nome real. Deixa apenas silêncio e sangue."
    },
}

ENEMIES = {
    1: [("Rato Gigante", 40, 8, "🐀"), ("Esqueleto Torto", 50, 10, "💀"), ("Goblin Bêbado", 45, 9, "👺")],
    2: [("Gárgula de Pedra", 80, 18, "🗿"), ("Espectro Faminto", 70, 22, "👻"), ("Verme Sombrio", 90, 16, "🪱")],
    3: [("Cavaleiro Corrompido", 130, 28, "⚔️"), ("Bruxa do Pântano", 110, 32, "🧙"), ("Golem de Lama", 150, 24, "🪨")],
    4: [("Dragão Menor", 180, 38, "🐉"), ("Lich Antigo", 160, 42, "☠️"), ("Senhor Vampiro", 170, 36, "🧛")],
    5: [("Lorde das Sombras", 250, 50, "👁️"), ("Arcanista Caído", 220, 55, "🌑"), ("O Devorador", 280, 45, "💀")],
}

MARKET_POOL = {
    "weapon": [
        {"name": "Espada Longa",    "atk": 36, "price": 140, "type": "weapon", "rarity": "comum", "value": 65},
        {"name": "Machado de Guerra","atk": 42,"price": 160, "type": "weapon", "rarity": "comum", "value": 75},
        {"name": "Glaive Sombrio",  "atk": 52, "price": 200, "type": "weapon", "rarity": "incomum","value": 95},
        {"name": "Lâmina da Ruína", "atk": 75, "price": 320, "type": "weapon", "rarity": "raro",  "value": 160},
        {"name": "DESTRUIDORA",     "atk": 130,"price": 550, "type": "weapon", "rarity": "lendário","value": 270},
    ],
    "armor": [
        {"name": "Cota de Malha",   "def": 18, "price": 120, "type": "armor",  "rarity": "comum", "value": 55},
        {"name": "Escudo Cruzado",  "def": 25, "price": 160, "type": "armor",  "rarity": "comum", "value": 70},
        {"name": "Armadura das Trevas","def":35,"price": 220,"type": "armor",  "rarity": "incomum","value": 100},
        {"name": "Égide Arcana",    "def": 50, "price": 350, "type": "armor",  "rarity": "raro",  "value": 175},
    ],
}

LORE_PER_FLOOR = {
    1: "O portão rangeu ao fechar atrás de você. O cheiro de podridão e pedra úmida preencheu seus pulmões.",
    2: "As tochas piscam. Nas paredes, marcas de garras — muitas. Alguém tentou escapar.",
    3: "Uma inscrição na pedra: 'Os que chegaram até aqui já não eram humanos por inteiro.'",
    4: "O calor aumenta. O chão vibra. Algo antigo desperta nas profundezas.",
    5: "Você chegou ao topo. O trono vazio pulsa com energia escura. O castelo é você agora.",
}

RARITY_COLORS = {
    "comum":    "#d4b896",
    "incomum":  "#00e676",
    "raro":     "#00e5ff",
    "lendário": "#ff9100",
}


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
    hp = int(base_hp * scale)
    atk = int(base_atk * scale)
    return {"name": f"{icon} {name}", "hp": hp, "max_hp": hp, "atk": atk, "stunned": False}

def generate_market():
    weapons = MARKET_POOL["weapon"]
    armors  = MARKET_POOL["armor"]
    floor = st.session_state.floor

    # Rarity weights scale with floor
    w_weights = [40, 30, 20, 7, 3] if floor >= 3 else [60, 30, 10, 0, 0]
    a_weights = [50, 30, 15, 5]    if floor >= 3 else [70, 25, 5, 0]

    def pick(pool, weights):
        total = sum(weights[:len(pool)])
        r = random.randint(1, total)
        cum = 0
        for item, w in zip(pool, weights):
            cum += w
            if r <= cum:
                return dict(item)
        return dict(pool[-1])

    return [pick(weapons, w_weights), pick(armors, a_weights)]

def render_bar(pct, kind="hp"):
    pct = max(0.0, min(1.0, pct))
    cls = f"bar-fill-{kind}"
    color_stop = "#ff6b6b" if kind == "hp" else "#5dade2"
    return f'<div class="bar-wrap"><div class="{cls}" style="width:{pct*100:.1f}%"></div></div>'

def rarity_color(r):
    return RARITY_COLORS.get(r, "#d4b896")

def item_label(item):
    attr = f"+{item['atk']} ATK" if item["type"] == "weapon" else f"+{item['def']} DEF"
    r = item.get("rarity", "comum")
    col = rarity_color(r)
    return f'<span style="color:{col}">{item["name"]}</span> <span style="color:#5a4030;font-size:.7rem">({attr})</span>'


# ============================================================
# INIT STATE
# ============================================================
def init_state():
    defaults = {
        'game_active': False,
        'hero_class': None,
        'hp': 100, 'max_hp': 100,
        'mana': 50, 'max_mana': 50,
        'gold': 120,
        'log': [{"t": "??:??", "msg": "O castelo aguarda...", "kind": ""}],
        'enemy': None,
        'weapon': None,
        'armor': None,
        'floor': 1,
        'kills': 0,
        'kills_needed': 3,
        'inventory': [],
        'state': 'menu',
        'market_stock': [],
        'total_kills': 0,
        'gold_earned': 0,
        'blocked_last': False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ============================================================
# START GAME
# ============================================================
def start_game(role: str):
    c = CLASSES[role]
    st.session_state.update({
        'game_active': True,
        'hero_class': role,
        'hp': c['hp'], 'max_hp': c['hp'],
        'mana': c['mana'], 'max_mana': c['mana'],
        'gold': 120,
        'weapon': dict(c['weapon']),
        'armor':  dict(c['armor']),
        'state': 'playing',
        'floor': 1,
        'kills': 0,
        'kills_needed': 3,
        'inventory': [],
        'market_stock': [],
        'total_kills': 0,
        'gold_earned': 120,
        'enemy': None,
        'log': [{"t": time.strftime('%H:%M'), "msg": f"⚔️ {role} entra no castelo maldito...", "kind": "level"}],
        'blocked_last': False,
    })
    st.rerun()


# ============================================================
# COMBAT LOGIC
# ============================================================
def player_attack(magic: bool = False):
    ss = st.session_state
    en = ss.enemy
    if not en:
        return

    # ── Player hits enemy ──
    base_atk = ss.weapon['atk']
    hp_pct   = ss.hp / ss.max_hp
    is_fury  = ss.hero_class == "Berserker" and hp_pct < 0.2
    is_rare  = ss.weapon.get('rarity') in ('raro', 'lendário')

    if magic:
        if ss.mana < 15:
            st.warning("Mana insuficiente!")
            return
        ss.mana -= 15
        dmg = base_atk + 28 + random.randint(5, 15)
        if is_rare:
            dmg = int(dmg * 1.7)
            log("✨ Magia potencializada pelo item raro!", "magic")
        else:
            log("🔥 Feitiço lançado!", "magic")
    else:
        dmg = base_atk + random.randint(4, 14)
        if is_fury:
            dmg = int(dmg * 1.9)
            log("🔥 FÚRIA! Dano devastador!", "crit")

    stun = False
    if ss.hero_class == "Assassino" and not magic and random.random() < 0.25:
        stun = True
        en['stunned'] = True
        log("⚡ STUN! Inimigo paralisado!", "crit")

    en['hp'] -= dmg
    log(f"⚔️ Você causou {dmg} de dano em {en['name']}!", "")

    # ── Enemy dies ──
    if en['hp'] <= 0:
        gold_gain = 45 + ss.floor * 12 + random.randint(0, 20)
        ss.gold += gold_gain
        ss.gold_earned += gold_gain
        ss.kills += 1
        ss.total_kills += 1
        ss.enemy = None
        log(f"💀 {en['name']} foi derrotado! +{gold_gain}G", "loot")

        # drop chance
        if random.random() < 0.20 + ss.floor * 0.03:
            dropped = random.choice(generate_market())
            dropped["price"] = 0
            ss.inventory.append(dropped)
            log(f"🎁 Item largado: {dropped['name']}!", "loot")

        # advance floor
        if ss.kills >= ss.kills_needed:
            ss.floor += 1
            ss.kills = 0
            ss.kills_needed = 3 + (ss.floor // 2)
            ss.market_stock = []
            log(f"🌟 ANDAR {ss.floor} desbloqueado!", "level")
            if ss.floor > 5:
                ss.state = 'victory'
        st.rerun()
        return

    # ── Enemy retaliates ──
    if en.get('stunned'):
        en['stunned'] = False
        log("😵 Inimigo ainda atordoado — sem contra-ataque.", "")
    else:
        if ss.hero_class == "Assassino" and random.random() < 0.30:
            log("💨 Você esquivou do ataque!", "")
        else:
            reduction = ss.armor['def']
            # Guerreiro passive block
            block_bonus = 0
            if ss.hero_class == "Guerreiro" and random.random() < 0.20:
                block_bonus = en['atk'] // 2
                ss.blocked_last = True
                log("🛡️ Bloqueio! Dano reduzido!", "")
            else:
                ss.blocked_last = False
            edmg = max(2, en['atk'] - reduction - block_bonus)
            ss.hp -= edmg
            log(f"👹 {en['name']} causou {edmg} de dano!", "crit")
            if ss.hp <= 0:
                ss.hp = 0
                ss.state = 'player_dead'

    st.rerun()


# ============================================================
# ████████  RENDER MENU  ████████
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
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-hdr'>Escolha sua linhagem</div>", unsafe_allow_html=True)

    cols = st.columns(2)
    class_list = list(CLASSES.items())
    for idx, (name, data) in enumerate(class_list):
        col = cols[idx % 2]
        with col:
            stats = data["stats"]
            bars_html = ""
            for stat_name, val in stats.items():
                icons = {"força": "⚔️", "agilidade": "💨", "magia": "🔮"}
                fill_pct = val / 5 * 100
                bars_html += f"""
                <div class="class-stat">
                  <span style="font-size:.65rem;color:#5a4030;min-width:54px">{icons.get(stat_name,'')} {stat_name}</span>
                  <div class="cs-bar"><div class="cs-fill" style="width:{fill_pct}%;background:linear-gradient(90deg,#c9a84c,#f0d080)"></div></div>
                </div>"""

            st.markdown(f"""
            <div class="class-card">
              <span class="class-icon">{data['icon']}</span>
              <div class="class-name">{name}</div>
              <div class="class-desc">{data['desc']}</div>
              {bars_html}
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"{data['icon']} Jogar como {name}", key=f"start_{name}"):
                start_game(name)


# ============================================================
# ████████  RENDER HERO PANEL  ████████
# ============================================================
def render_hero_panel():
    ss = st.session_state
    hp_pct   = ss.hp / ss.max_hp
    mp_pct   = ss.mana / ss.max_mana
    is_fury  = ss.hero_class == "Berserker" and hp_pct < 0.2
    w_rarity = ss.weapon.get('rarity', 'comum')
    a_rarity = ss.armor.get('rarity', 'comum')
    w_col    = rarity_color(w_rarity)
    a_col    = rarity_color(a_rarity)

    fury_badge = '<span class="fury-badge">⚡ FÚRIA</span>' if is_fury else ""

    st.markdown(f"""
    <div class="hero-3d">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
        <span class="hero-name">{CLASSES[ss.hero_class]['icon']} {ss.hero_class.upper()} {fury_badge}</span>
        <span class="hero-gold">💰 {ss.gold}G</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">❤️ VIDA</span>
        {render_bar(hp_pct, 'hp')}
        <span class="stat-val">{ss.hp}/{ss.max_hp}</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">🔮 MANA</span>
        {render_bar(mp_pct, 'mp')}
        <span class="stat-val">{ss.mana}/{ss.max_mana}</span>
      </div>
      <div class="equip-row">
        <span>⚔️ <span class="equip-val" style="color:{w_col}">{ss.weapon['name']} +{ss.weapon['atk']}</span></span>
        <span>🛡️ <span class="equip-val" style="color:{a_col}">{ss.armor['name']} +{ss.armor['def']}</span></span>
        <span style="margin-left:auto;color:#5a4030;font-size:.68rem">🏆 {ss.total_kills} abatidos</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# ████████  RENDER COMBAT TAB  ████████
# ============================================================
def render_combat():
    ss = st.session_state

    # Floor lore
    lore = LORE_PER_FLOOR.get(ss.floor, "")
    if lore:
        st.markdown(f"""
        <div style="font-style:italic;font-size:.72rem;color:#5a4030;
          border-left:2px solid rgba(201,168,76,.2);padding-left:10px;margin-bottom:14px">
          {lore}
        </div>""", unsafe_allow_html=True)

    # Kill progress
    progress_pct = ss.kills / ss.kills_needed
    st.markdown(f"""
    <div style="margin-bottom:12px">
      <div style="font-size:.68rem;color:#5a4030;letter-spacing:.1em;margin-bottom:4px">
        PROGRESSO DO ANDAR — {ss.kills}/{ss.kills_needed} abates
      </div>
      <div style="height:6px;background:rgba(255,255,255,.06);border-radius:3px;overflow:hidden">
        <div style="width:{progress_pct*100:.0f}%;height:100%;background:linear-gradient(90deg,#3a7a3a,#00ff88);
          box-shadow:0 0 8px rgba(0,255,136,.5);border-radius:3px;transition:width .4s"></div>
      </div>
    </div>""", unsafe_allow_html=True)

    if ss.enemy:
        en = ss.enemy
        hp_pct = max(0, en['hp'] / en['max_hp'])
        stun_txt = ' <span style="color:#ffcc00;font-size:.65rem">[ATORDOADO]</span>' if en.get('stunned') else ""

        st.markdown(f"""
        <div class="enemy-3d">
          <div class="enemy-name">{en['name']}{stun_txt}</div>
          <div class="enemy-hp-wrap">
            <div class="enemy-hp-fill" style="width:{hp_pct*100:.1f}%"></div>
          </div>
          <div class="enemy-stats">
            ❤️ {max(0,en['hp'])}/{en['max_hp']} HP &nbsp;|&nbsp; ⚔️ {en['atk']} ATK
          </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="btn-attack">', unsafe_allow_html=True)
            if st.button("⚔️ ATACAR", key="btn_attack"):
                player_attack(magic=False)
            st.markdown('</div>', unsafe_allow_html=True)

        if ss.hero_class == "Mago":
            with c2:
                st.markdown('<div class="btn-magic">', unsafe_allow_html=True)
                if st.button(f"🔥 MAGIA (15☁️)", key="btn_magic"):
                    player_attack(magic=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            with c2:
                # Flavour skill display
                skill_map = {
                    "Guerreiro":  "🛡️ BLOQUEIO (passivo 20%)",
                    "Berserker":  "🔥 FÚRIA (passivo <20% HP)",
                    "Assassino":  "💨 ESQUIVA (passivo 30%)",
                }
                st.markdown(f"""
                <div style="background:rgba(255,255,255,.03);border:1px solid rgba(201,168,76,.1);
                  border-radius:8px;padding:10px;text-align:center;font-size:.68rem;color:#5a4030">
                  {skill_map.get(ss.hero_class,"")}
                </div>""", unsafe_allow_html=True)

    else:
        st.markdown('<div class="btn-explore">', unsafe_allow_html=True)
        if st.button("👣 EXPLORAR A SALA", key="btn_explore"):
            roll = random.random()
            if roll < 0.50:
                gain = 35 + ss.floor * 12 + random.randint(0, 18)
                ss.gold += gain
                ss.gold_earned += gain
                log(f"🎁 Baú encontrado! +{gain}G", "loot")
                # small chance of item in chest
                if random.random() < 0.15:
                    item = random.choice(generate_market())
                    item["price"] = 0
                    ss.inventory.append(item)
                    log(f"✨ Item no baú: {item['name']}!", "loot")
            else:
                ss.enemy = spawn_enemy(ss.floor)
                log(f"⚠️ {ss.enemy['name']} aparece das sombras!", "crit")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


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
      <div>
        <div class="inv-name" style="color:{w_col}">{ss.weapon['name']}</div>
        <div class="inv-attr">+{ss.weapon['atk']} ATK · {ss.weapon.get('rarity','comum').upper()}</div>
      </div>
    </div>
    <div class="inv-item">
      <span style="font-size:1.2rem">🛡️</span>
      <div>
        <div class="inv-name" style="color:{a_col}">{ss.armor['name']}</div>
        <div class="inv-attr">+{ss.armor['def']} DEF · {ss.armor.get('rarity','comum').upper()}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-hdr' style='margin-top:14px'>Mochila</div>", unsafe_allow_html=True)

    if not ss.inventory:
        st.markdown('<div style="color:#5a4030;font-size:.78rem;padding:10px 0">— Mochila vazia —</div>', unsafe_allow_html=True)
        return

    for i, item in enumerate(ss.inventory):
        r = item.get('rarity', 'comum')
        col = rarity_color(r)
        attr = f"+{item['atk']} ATK" if item['type'] == 'weapon' else f"+{item['def']} DEF"
        icon = "⚔️" if item['type'] == 'weapon' else "🛡️"
        rare_cls = "rare" if r in ('raro','lendário') else ""

        st.markdown(f"""
        <div class="inv-item {rare_cls}">
          <span style="font-size:1.1rem">{icon}</span>
          <div style="flex:1">
            <div class="inv-name {rare_cls}" style="color:{col}">{item['name']}</div>
            <div class="inv-attr">{attr} · {r.upper()}</div>
          </div>
          <div class="inv-val">⚖️ {item.get('value',0)}G</div>
        </div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
            if st.button(f"Equipar", key=f"equip_{i}"):
                slot = item['type']
                old = ss[slot]
                ss[slot] = item
                ss.inventory[i] = old
                log(f"🔄 Equipou: {item['name']}!", "")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            sell_val = item.get('value', 10)
            if st.button(f"Vender +{sell_val}G", key=f"sell_inv_{i}"):
                ss.gold += sell_val
                ss.inventory.pop(i)
                log(f"💰 Vendeu {item['name']} por {sell_val}G", "loot")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# ████████  RENDER MARKET TAB  ████████
# ============================================================
def render_market():
    ss = st.session_state

    if not ss.market_stock:
        ss.market_stock = generate_market()

    # Potions
    st.markdown("<div class='section-hdr'>Poções</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button("❤️ Vida +50 HP\n(40G)", key="pot_hp"):
            if ss.gold >= 40:
                ss.gold -= 40
                healed = min(ss.max_hp, ss.hp + 50) - ss.hp
                ss.hp += healed
                log(f"❤️ Poção de vida: +{healed} HP", "loot")
                st.rerun()
            else:
                st.warning("Ouro insuficiente!")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="btn-magic">', unsafe_allow_html=True)
        if st.button("🔮 Mana +40\n(40G)", key="pot_mp"):
            if ss.gold >= 40:
                ss.gold -= 40
                restored = min(ss.max_mana, ss.mana + 40) - ss.mana
                ss.mana += restored
                log(f"🔮 Poção de mana: +{restored} Mana", "magic")
                st.rerun()
            else:
                st.warning("Ouro insuficiente!")
        st.markdown('</div>', unsafe_allow_html=True)

    # Equipment
    st.markdown("<div class='section-hdr' style='margin-top:14px'>Equipamentos</div>", unsafe_allow_html=True)

    for i, item in enumerate(ss.market_stock):
        r = item.get('rarity', 'comum')
        col = rarity_color(r)
        attr = f"+{item['atk']} ATK" if item['type'] == 'weapon' else f"+{item['def']} DEF"
        icon = "⚔️" if item['type'] == 'weapon' else "🛡️"
        rare_cls = "rare" if r in ('raro','lendário') else ""
        badge = f'<span style="background:{col};color:#000;font-size:.6rem;padding:1px 6px;border-radius:8px;font-weight:700">{r.upper()}</span>' if r != "comum" else ""

        st.markdown(f"""
        <div class="mkt-item {rare_cls}">
          <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div class="mkt-name {rare_cls}" style="color:{col}">{icon} {item['name']} {badge}</div>
            <div class="price-tag">💰 {item['price']}G</div>
          </div>
          <div class="mkt-sub">{attr}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button(f"Comprar {item['name']}", key=f"buy_{i}"):
            if ss.gold >= item['price']:
                ss.gold -= item['price']
                bought = dict(item)
                ss.inventory.append(bought)
                ss.market_stock.pop(i)
                log(f"🛒 Comprou: {item['name']}!", "loot")
                if not ss.market_stock:
                    ss.market_stock = generate_market()
                st.rerun()
            else:
                st.warning("Ouro insuficiente!")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='section-hdr' style='margin-top:14px'>Vender Inventário</div>", unsafe_allow_html=True)
    if not ss.inventory:
        st.markdown('<div style="color:#5a4030;font-size:.78rem">— Nada para vender —</div>', unsafe_allow_html=True)
    else:
        for i, item in enumerate(ss.inventory):
            sell_val = item.get('value', 10)
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            if st.button(f"Vender {item['name']} (+{sell_val}G)", key=f"sell_mkt_{i}"):
                ss.gold += sell_val
                ss.inventory.pop(i)
                log(f"💰 Vendeu {item['name']} por {sell_val}G", "loot")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# ████████  RENDER LOG  ████████
# ============================================================
def render_log():
    ss = st.session_state
    lines = ss.log[:6]
    items_html = ""
    for entry in lines:
        cls = entry.get("kind", "")
        items_html += f'<div class="log-line {cls}">[{entry["t"]}] {entry["msg"]}</div>'
    st.markdown(f'<div class="log-wrap">{items_html}</div>', unsafe_allow_html=True)


# ============================================================
# ████████  MAIN GAME SCREEN  ████████
# ============================================================
def render_game():
    ss = st.session_state

    # Floor badge
    st.markdown(f"""
    <div class="floor-wrapper">
      <span class="floor-3d">⚔️ ANDAR {ss.floor} ⚔️</span>
    </div>""", unsafe_allow_html=True)

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

    st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
    if st.button("🔄 RECOMEÇAR A JORNADA"):
        reset_state()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# ████████  VICTORY  ████████
# ============================================================
def render_victory():
    ss = st.session_state
    st.markdown(f"""
    <div class="gameover-wrap">
      <div style="font-family:'UnifrakturMaguntia',cursive;font-size:3.6rem;
        color:#c9a84c;text-shadow:0 0 30px rgba(201,168,76,.8)">
        Vitória!
      </div>
      <div style="font-family:'Cinzel',serif;color:#8a7040;font-size:.82rem;margin:8px 0 20px">
        O trono do Rei Eterno é seu. O castelo inclina sua coroa.
      </div>
      <div class="gameover-stats">
        <div>⚔️ Inimigos abatidos: <b style="color:var(--gold)">{ss.total_kills}</b></div>
        <div>💰 Ouro acumulado: <b style="color:var(--gold)">{ss.gold_earned}G</b></div>
        <div>🧙 Classe: <b style="color:var(--gold)">{ss.hero_class}</b></div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
    if st.button("🏆 JOGAR NOVAMENTE"):
        reset_state()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# ████████  ROUTER  ████████
# ============================================================
state = st.session_state.state

if state == 'menu':
    render_menu()
elif state == 'playing':
    render_game()
elif state == 'player_dead':
    render_gameover()
elif state == 'victory':
    render_victory()
