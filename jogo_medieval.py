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
  background-color:var(--bg) !important; color:var(--text); font-family:'Cinzel',serif;
}
[data-testid="stAppViewContainer"] {
  background-image:
    radial-gradient(ellipse 80% 60% at 50% 0%,rgba(100,20,20,.18) 0%,transparent 70%),
    repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(255,255,255,.012) 2px,rgba(255,255,255,.012) 4px);
}
#MainMenu,footer,header,[data-testid="stToolbar"],
[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none !important;}
[data-testid="block-container"]{padding:1.5rem 1rem 3rem;max-width:820px;margin:auto;}

.stTabs [data-baseweb="tab-list"]{gap:4px;background:var(--bg2);border-radius:8px;padding:4px;}
.stTabs [data-baseweb="tab"]{font-family:'Cinzel',serif;font-size:.78rem;letter-spacing:.08em;
  color:var(--text);background:transparent;border-radius:6px;padding:8px 14px;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#3a1a1a,#2a1020) !important;
  color:var(--gold) !important;box-shadow:inset 0 1px 0 rgba(201,168,76,.3),0 0 12px rgba(201,168,76,.15);}
.stTabs [data-baseweb="tab-panel"]{padding-top:1rem;}

div[data-testid="stButton"]>button{font-family:'Cinzel',serif !important;font-weight:700 !important;
  letter-spacing:.08em !important;text-transform:uppercase;font-size:.72rem !important;
  width:100% !important;padding:10px 8px !important;border-radius:6px !important;transition:all .15s ease !important;}
hr{border-color:var(--border) !important;margin:12px 0 !important;}
.stProgress>div>div>div>div{background:linear-gradient(90deg,#8b0000,#c0392b,#e74c3c) !important;box-shadow:0 0 8px rgba(231,76,60,.6);}
.stProgress>div>div{background:rgba(255,255,255,.07) !important;border-radius:4px;}

/* ── TITLE ── */
.castle-title{font-family:'UnifrakturMaguntia',cursive;font-size:clamp(2.6rem,8vw,4.8rem);
  text-align:center;line-height:1.1;margin:0 0 4px;
  background:linear-gradient(180deg,#f0d080 0%,#c9a84c 40%,#7a5a20 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  filter:drop-shadow(0 2px 6px rgba(201,168,76,.5)) drop-shadow(0 4px 18px rgba(0,0,0,.9));letter-spacing:.04em;}
.castle-subtitle{font-family:'Cinzel',serif;font-size:.82rem;letter-spacing:.35em;
  text-transform:uppercase;color:#7a6040;text-align:center;margin-bottom:28px;}

/* ── FLOOR 3D ── */
.floor-3d{display:inline-block;font-family:'Cinzel Decorative',serif;font-size:1.05rem;
  font-weight:900;letter-spacing:.12em;text-transform:uppercase;color:#0a0608;
  background:linear-gradient(180deg,#f0d080 0%,#c9a84c 50%,#7a5a20 100%);
  padding:8px 28px;border-radius:40px;
  box-shadow:0 2px 0 #3a2a00,0 4px 0 #2a1a00,0 6px 0 #1a0a00,0 8px 0 rgba(0,0,0,.5),
             0 12px 24px rgba(0,0,0,.7),inset 0 1px 0 rgba(255,255,240,.5);
  transform:perspective(200px) rotateX(8deg);text-shadow:0 1px 2px rgba(255,255,200,.4);}
.floor-wrapper{text-align:center;margin-bottom:20px;}

/* ── HERO PANEL ── */
.hero-3d{background:linear-gradient(135deg,rgba(60,20,20,.95) 0%,rgba(25,12,18,.95) 100%);
  border:1px solid rgba(201,168,76,.3);border-radius:12px;padding:18px 20px;
  margin-bottom:16px;position:relative;overflow:hidden;
  box-shadow:0 1px 0 rgba(201,168,76,.2) inset,0 -1px 0 rgba(0,0,0,.6) inset,
             6px 6px 20px rgba(0,0,0,.7),-1px -1px 0 rgba(201,168,76,.1);}
.hero-3d::before{content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(201,168,76,.06) 0%,transparent 60%);pointer-events:none;}
.hero-3d::after{content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(201,168,76,.5),transparent);}
.hero-name{font-family:'Cinzel Decorative',serif;font-size:.95rem;font-weight:700;
  letter-spacing:.1em;color:var(--gold-lt);text-shadow:0 0 12px rgba(201,168,76,.5);}
.hero-gold{font-family:'Cinzel',serif;font-weight:700;color:var(--gold-lt);font-size:.95rem;}
.stat-row{display:flex;align-items:center;gap:10px;margin:6px 0;}
.stat-label{font-size:.72rem;letter-spacing:.1em;color:#8a7060;min-width:50px;}
.bar-wrap{flex:1;height:12px;background:rgba(255,255,255,.07);border-radius:6px;overflow:hidden;
  box-shadow:inset 0 2px 4px rgba(0,0,0,.6),0 1px 0 rgba(255,255,255,.05);}
.bar-fill-hp{height:100%;border-radius:6px;
  background:linear-gradient(90deg,#7b0000,#c0392b 60%,#ff6b6b);
  box-shadow:0 0 8px rgba(192,57,43,.7);transition:width .4s ease;}
.bar-fill-mp{height:100%;border-radius:6px;
  background:linear-gradient(90deg,#003070,#2980b9 60%,#5dade2);
  box-shadow:0 0 8px rgba(41,128,185,.7);transition:width .4s ease;}
.stat-val{font-size:.76rem;color:var(--text);min-width:60px;text-align:right;}
.equip-row{margin-top:12px;padding-top:10px;border-top:1px solid rgba(201,168,76,.15);
  display:flex;gap:16px;font-size:.72rem;color:#8a7060;}
.equip-val{color:var(--text);font-weight:600;}
.fury-badge{display:inline-block;background:linear-gradient(135deg,#8b0000,#c0392b);
  color:#fff;font-size:.62rem;font-weight:700;letter-spacing:.12em;
  padding:2px 8px;border-radius:10px;box-shadow:0 0 10px rgba(192,57,43,.8);
  animation:pulse-red 1s ease-in-out infinite;}
@keyframes pulse-red{0%,100%{box-shadow:0 0 8px rgba(192,57,43,.8);}50%{box-shadow:0 0 18px rgba(255,80,80,1);}}

/* ══════════════════════════════════════════
   ARENA ANIMADA
══════════════════════════════════════════ */
.arena-wrap{
  position:relative;
  background:linear-gradient(180deg,#0d0508 0%,#1a0a10 60%,#0a0305 100%);
  border:1px solid rgba(192,57,43,.25);border-radius:14px;
  padding:20px 16px 16px;margin-bottom:14px;overflow:hidden;
  box-shadow:0 0 40px rgba(0,0,0,.8),inset 0 0 60px rgba(100,0,0,.08);
  min-height:200px;
}
.arena-wrap::before{content:'';position:absolute;bottom:56px;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,rgba(201,168,76,.15),rgba(201,168,76,.25),rgba(201,168,76,.15),transparent);}
.arena-wrap::after{content:'';position:absolute;bottom:0;left:0;right:0;height:54px;
  background:linear-gradient(0deg,rgba(10,3,8,.9),transparent);pointer-events:none;}

.sprite{font-size:3.4rem;display:inline-block;line-height:1;
  filter:drop-shadow(0 4px 8px rgba(0,0,0,.8));transform-origin:bottom center;}

.hero-sprite-wrap{position:absolute;bottom:56px;left:12%;
  display:flex;flex-direction:column;align-items:center;gap:4px;}
.hero-sprite-label{font-family:'Cinzel Decorative',serif;font-size:.6rem;color:var(--gold);
  letter-spacing:.08em;text-shadow:0 0 8px rgba(201,168,76,.5);}

.enemy-sprite-wrap{position:absolute;bottom:56px;right:12%;
  display:flex;flex-direction:column;align-items:center;gap:4px;}
.enemy-sprite-label{font-family:'Cinzel',serif;font-size:.6rem;color:#e74c3c;
  letter-spacing:.06em;text-shadow:0 0 8px rgba(231,76,60,.5);}

.arena-hp-row{display:flex;gap:10px;margin-bottom:14px;align-items:center;}
.ahp-label{font-size:.68rem;color:#8a7060;min-width:44px;}
.ahp-bar{flex:1;height:10px;background:rgba(255,255,255,.07);border-radius:5px;
  overflow:hidden;box-shadow:inset 0 2px 3px rgba(0,0,0,.6);}
.ahp-fill-hero{height:100%;border-radius:5px;
  background:linear-gradient(90deg,#7b0000,#c0392b 60%,#e74c3c);
  box-shadow:0 0 6px rgba(192,57,43,.6);transition:width .5s ease;}
.ahp-fill-enemy{height:100%;border-radius:5px;
  background:linear-gradient(90deg,#5a0000,#8b0000 60%,#b00000);
  box-shadow:0 0 6px rgba(139,0,0,.6);transition:width .5s ease;}
.ahp-val{font-size:.64rem;color:var(--text);min-width:56px;text-align:right;}
.vs-badge{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  font-family:'Cinzel Decorative',serif;font-size:.75rem;color:rgba(201,168,76,.2);
  letter-spacing:.15em;pointer-events:none;}
.event-flash{position:absolute;inset:0;border-radius:14px;pointer-events:none;z-index:10;}

/* ── HERO ATTACK ── */
.anim-hero-attack .sprite-hero{animation:hero-slash .55s ease forwards;}
@keyframes hero-slash{
  0%  {transform:translateX(0) scaleX(1) rotate(0deg);}
  20% {transform:translateX(4px) scaleX(1.08) rotate(-8deg);}
  45% {transform:translateX(58px) scaleX(1.15) rotate(-15deg);}
  60% {transform:translateX(52px) scaleX(1) rotate(-5deg);}
  100%{transform:translateX(0) scaleX(1) rotate(0deg);}
}
.anim-hero-attack .event-flash{animation:flash-red .55s ease forwards;}
@keyframes flash-red{0%,100%{background:transparent;}40%{background:rgba(192,57,43,.18);}50%{background:rgba(255,80,60,.08);}}

/* ── HERO MAGIC ── */
.anim-hero-magic .sprite-hero{animation:hero-cast .65s ease forwards;}
@keyframes hero-cast{
  0%  {transform:translateY(0) scale(1);filter:drop-shadow(0 4px 8px rgba(0,0,0,.8));}
  30% {transform:translateY(-10px) scale(1.12);filter:drop-shadow(0 0 20px rgba(41,128,185,.9)) drop-shadow(0 4px 8px rgba(0,0,0,.8));}
  60% {transform:translateY(-6px) scale(1.08);filter:drop-shadow(0 0 30px rgba(0,229,255,1)) drop-shadow(0 4px 8px rgba(0,0,0,.8));}
  100%{transform:translateY(0) scale(1);filter:drop-shadow(0 4px 8px rgba(0,0,0,.8));}
}
.anim-hero-magic .event-flash{animation:flash-blue .65s ease forwards;}
@keyframes flash-blue{0%,100%{background:transparent;}40%{background:rgba(41,128,185,.2);}55%{background:rgba(0,229,255,.1);}}
.anim-hero-magic::after{content:'✨';position:absolute;bottom:74px;left:28%;font-size:1.6rem;
  animation:magic-bolt .55s ease forwards;z-index:5;}
@keyframes magic-bolt{
  0%  {transform:translateX(0) scale(.5);opacity:1;}
  60% {transform:translateX(140px) scale(1.2);opacity:1;}
  100%{transform:translateX(200px) scale(.3);opacity:0;}
}

/* ── ENEMY HIT ── */
.anim-enemy-hit .sprite-enemy{animation:enemy-hurt .45s ease forwards;}
@keyframes enemy-hurt{
  0%,100%{transform:scaleX(-1);filter:drop-shadow(0 4px 8px rgba(0,0,0,.8));}
  15%    {transform:scaleX(-1) translateX(-6px);filter:drop-shadow(0 0 14px rgba(255,60,60,1)) drop-shadow(0 4px 8px rgba(0,0,0,.8));}
  30%    {transform:scaleX(-1) translateX(5px);}
  50%    {transform:scaleX(-1) translateX(-4px);}
  70%    {transform:scaleX(-1) translateX(3px);}
}

/* ── HERO HIT ── */
.anim-hero-hit .sprite-hero{animation:hero-hurt .45s ease forwards;}
@keyframes hero-hurt{
  0%,100%{transform:translateX(0);filter:drop-shadow(0 4px 8px rgba(0,0,0,.8));}
  15%    {transform:translateX(-8px);filter:drop-shadow(0 0 12px rgba(255,80,60,.9)) drop-shadow(0 4px 8px rgba(0,0,0,.8));}
  30%    {transform:translateX(6px);}
  50%    {transform:translateX(-5px);}
  70%    {transform:translateX(3px);}
}

/* ── ENEMY DEATH ── */
.anim-enemy-death .sprite-enemy{animation:enemy-die .9s ease forwards;}
@keyframes enemy-die{
  0%  {transform:scaleX(-1) scale(1) translateY(0);opacity:1;filter:drop-shadow(0 4px 8px rgba(0,0,0,.8));}
  20% {transform:scaleX(-1) scale(1.15) translateY(-8px);filter:drop-shadow(0 0 20px rgba(255,60,60,1)) drop-shadow(0 4px 8px rgba(0,0,0,.8));opacity:1;}
  50% {transform:scaleX(-1) scale(.85) translateY(4px) rotate(15deg);opacity:.7;}
  80% {transform:scaleX(-1) scale(.4) translateY(18px) rotate(40deg);opacity:.2;}
  100%{transform:scaleX(-1) scale(0) translateY(24px) rotate(60deg);opacity:0;}
}
.anim-enemy-death .event-flash{animation:flash-gold-death .9s ease forwards;}
@keyframes flash-gold-death{0%,100%{background:transparent;}25%{background:rgba(255,60,60,.2);}50%{background:rgba(201,168,76,.15);}}

/* ── HERO DEATH ── */
.anim-hero-death .sprite-hero{animation:hero-die 1.1s ease forwards;}
@keyframes hero-die{
  0%  {transform:translateY(0) rotate(0deg) scale(1);opacity:1;}
  20% {transform:translateY(-10px) rotate(-5deg) scale(1.05);filter:drop-shadow(0 0 20px rgba(255,0,0,.8));}
  50% {transform:translateY(4px) rotate(-20deg) scale(.95);opacity:.8;}
  75% {transform:translateY(12px) rotate(-45deg) scale(.7);opacity:.4;}
  100%{transform:translateY(20px) rotate(-90deg) scale(.3);opacity:0;}
}
.anim-hero-death .event-flash{animation:flash-death 1.1s ease forwards;}
@keyframes flash-death{0%,100%{background:transparent;}30%{background:rgba(192,57,43,.3);}60%{background:rgba(100,0,0,.2);}}

/* ── DODGE ── */
.anim-hero-dodge .sprite-hero{animation:hero-dodge .5s ease forwards;}
@keyframes hero-dodge{
  0%  {transform:translateX(0) translateY(0);}
  30% {transform:translateX(-22px) translateY(-12px);}
  55% {transform:translateX(-16px) translateY(-6px);}
  100%{transform:translateX(0) translateY(0);}
}

/* ── BLOCK ── */
.anim-hero-block .sprite-hero{animation:hero-block .5s ease forwards;}
@keyframes hero-block{
  0%,100%{transform:translateX(0);filter:drop-shadow(0 4px 8px rgba(0,0,0,.8));}
  30%    {transform:translateX(8px);filter:drop-shadow(0 0 16px rgba(201,168,76,.9)) drop-shadow(0 4px 8px rgba(0,0,0,.8));}
  60%    {transform:translateX(4px);filter:drop-shadow(0 0 10px rgba(201,168,76,.5)) drop-shadow(0 4px 8px rgba(0,0,0,.8));}
}

/* ── STUN ── */
.anim-enemy-stun .sprite-enemy{animation:stun-wobble .6s ease forwards;}
@keyframes stun-wobble{
  0%,100%{transform:scaleX(-1) rotate(0deg);}
  20%    {transform:scaleX(-1) rotate(10deg) translateY(-4px);}
  40%    {transform:scaleX(-1) rotate(-8deg) translateY(2px);}
  60%    {transform:scaleX(-1) rotate(6deg);}
  80%    {transform:scaleX(-1) rotate(-4deg);}
}
.stun-stars{position:absolute;font-size:1rem;animation:stars-float .7s ease forwards;z-index:6;}
@keyframes stars-float{0%{opacity:1;transform:translateY(0) scale(1);}100%{opacity:0;transform:translateY(-28px) scale(.7);}}

/* ── FURY ── */
.anim-hero-fury .sprite-hero{animation:fury-aura .5s ease forwards;}
@keyframes fury-aura{
  0%,100%{filter:drop-shadow(0 4px 8px rgba(0,0,0,.8));transform:scale(1);}
  30%    {filter:drop-shadow(0 0 22px rgba(255,60,0,1)) drop-shadow(0 4px 8px rgba(0,0,0,.8));transform:scale(1.14);}
  60%    {filter:drop-shadow(0 0 16px rgba(255,120,0,.8)) drop-shadow(0 4px 8px rgba(0,0,0,.8));transform:scale(1.08);}
}

/* ── DAMAGE NUMBERS ── */
.dmg-number{position:absolute;font-family:'Cinzel Decorative',serif;font-weight:900;
  pointer-events:none;z-index:20;animation:dmg-float 1s ease forwards;}
@keyframes dmg-float{
  0%  {opacity:1;transform:translateY(0) scale(1.2);}
  30% {opacity:1;transform:translateY(-18px) scale(1);}
  70% {opacity:.8;transform:translateY(-30px) scale(.9);}
  100%{opacity:0;transform:translateY(-44px) scale(.7);}
}
.dmg-hero  {color:#ff4444;font-size:1.4rem;text-shadow:0 0 10px rgba(255,68,68,.8);}
.dmg-enemy {color:#ff9944;font-size:1.4rem;text-shadow:0 0 10px rgba(255,153,68,.8);}
.dmg-magic {color:#00e5ff;font-size:1.3rem;text-shadow:0 0 12px rgba(0,229,255,.9);}

/* ── ENEMY STATS BAR ── */
.enemy-stats-bar{background:rgba(20,8,12,.7);border:1px solid rgba(192,57,43,.2);
  border-radius:8px;padding:8px 14px;margin-bottom:14px;
  font-size:.72rem;color:#8a5050;display:flex;gap:14px;align-items:center;}
.stun-tag{color:#ffcc00;font-size:.65rem;margin-left:auto;}

/* ── BUTTON VARIANTS ── */
.btn-attack div[data-testid="stButton"]>button{
  background:linear-gradient(180deg,#6b1a1a 0%,#3d0e0e 50%,#2a0808 100%) !important;
  color:#ff9999 !important;border:1px solid rgba(192,57,43,.5) !important;
  box-shadow:0 4px 0 #1a0404,0 5px 8px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,100,100,.2) !important;}
.btn-attack div[data-testid="stButton"]>button:hover{transform:translateY(1px) !important;
  box-shadow:0 3px 0 #1a0404,0 4px 6px rgba(0,0,0,.6) !important;}
.btn-magic div[data-testid="stButton"]>button{
  background:linear-gradient(180deg,#0d2a4a 0%,#071a30 50%,#040f1c 100%) !important;
  color:#5dade2 !important;border:1px solid rgba(41,128,185,.4) !important;
  box-shadow:0 4px 0 #020810,0 5px 8px rgba(0,0,0,.6),inset 0 1px 0 rgba(100,180,255,.15) !important;}
.btn-explore div[data-testid="stButton"]>button{
  background:linear-gradient(180deg,#1a3a1a 0%,#0d200d 50%,#071407 100%) !important;
  color:#00ff88 !important;border:1px solid rgba(0,200,100,.3) !important;
  box-shadow:0 4px 0 #030a03,0 5px 8px rgba(0,0,0,.6),inset 0 1px 0 rgba(0,255,100,.1) !important;
  font-size:.8rem !important;padding:14px 8px !important;}
.btn-gold div[data-testid="stButton"]>button{
  background:linear-gradient(180deg,#3a2a08 0%,#241a05 50%,#160f03 100%) !important;
  color:var(--gold-lt) !important;border:1px solid rgba(201,168,76,.3) !important;
  box-shadow:0 4px 0 #0a0601,0 5px 8px rgba(0,0,0,.6),inset 0 1px 0 rgba(201,168,76,.2) !important;}
.btn-danger div[data-testid="stButton"]>button{
  background:linear-gradient(180deg,#4a0a0a 0%,#2a0505 100%) !important;
  color:#ff6b6b !important;border:1px solid rgba(192,57,43,.4) !important;}

/* ── CLASS CARDS ── */
.class-card{background:linear-gradient(135deg,rgba(40,20,20,.9),rgba(20,10,15,.9));
  border:1px solid rgba(201,168,76,.2);border-radius:12px;padding:18px 16px;
  position:relative;overflow:hidden;margin-bottom:10px;
  box-shadow:4px 4px 16px rgba(0,0,0,.7),inset 0 1px 0 rgba(201,168,76,.1);}
.class-card::before{content:'';position:absolute;inset:0;
  background:radial-gradient(circle at 30% 30%,rgba(201,168,76,.06),transparent 60%);}
.class-icon{font-size:2rem;margin-bottom:8px;display:block;}
.class-name{font-family:'Cinzel Decorative',serif;font-size:.82rem;color:var(--gold-lt);
  font-weight:700;letter-spacing:.08em;margin-bottom:6px;}
.class-desc{font-size:.68rem;color:#8a7060;line-height:1.5;margin-bottom:10px;}

/* ── STAT BARS INSIDE CLASS CARDS (pure inline CSS, no Streamlit nesting) ── */
.cs-stat-row{display:flex;align-items:center;gap:8px;margin-bottom:5px;}
.cs-stat-label{font-size:.62rem;color:#5a4030;min-width:60px;letter-spacing:.04em;}
.cs-stat-bar-bg{flex:1;height:5px;background:rgba(255,255,255,.08);border-radius:3px;overflow:hidden;}
.cs-stat-bar-fill{height:100%;border-radius:3px;
  background:linear-gradient(90deg,#c9a84c,#f0d080);box-shadow:0 0 6px rgba(201,168,76,.4);}

/* ── LORE ── */
.lore-card{background:linear-gradient(135deg,rgba(20,12,8,.95),rgba(12,8,10,.95));
  border:1px solid rgba(201,168,76,.15);border-radius:10px;padding:20px 22px;margin:16px 0;
  font-size:.78rem;color:#8a7060;line-height:1.75;box-shadow:inset 0 0 60px rgba(0,0,0,.4);font-style:italic;}
.lore-title{font-family:'Cinzel Decorative',serif;font-size:.82rem;color:var(--gold);
  font-style:normal;letter-spacing:.1em;margin-bottom:10px;display:block;}

/* ── INVENTORY / MARKET ── */
.inv-item{background:rgba(30,18,22,.8);border:1px solid rgba(201,168,76,.15);
  border-radius:8px;padding:10px 14px;margin-bottom:8px;display:flex;align-items:center;gap:10px;
  box-shadow:2px 2px 8px rgba(0,0,0,.5);}
.inv-item.rare{border-color:rgba(0,229,255,.35);box-shadow:0 0 12px rgba(0,229,255,.1),2px 2px 8px rgba(0,0,0,.5);}
.inv-name{flex:1;font-size:.78rem;color:var(--text-lt);}
.inv-attr{font-size:.7rem;color:#8a7060;}
.inv-val{font-size:.7rem;color:var(--gold);}
.mkt-item{background:rgba(25,15,18,.9);border:1px solid rgba(201,168,76,.18);
  border-radius:8px;padding:12px 14px;margin-bottom:10px;
  box-shadow:3px 3px 10px rgba(0,0,0,.6);position:relative;overflow:hidden;}
.mkt-item.rare{border-color:rgba(0,229,255,.4);box-shadow:0 0 16px rgba(0,229,255,.12),3px 3px 10px rgba(0,0,0,.6);}
.mkt-item::after{content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(201,168,76,.3),transparent);}
.mkt-name{font-size:.82rem;color:var(--text-lt);font-weight:600;margin-bottom:4px;}
.mkt-sub{font-size:.7rem;color:#7a6050;margin-bottom:8px;}
.price-tag{display:inline-block;background:linear-gradient(135deg,#3a2a08,#1a1203);
  border:1px solid rgba(201,168,76,.3);border-radius:12px;
  padding:2px 10px;font-size:.72rem;color:var(--gold-lt);margin-bottom:8px;}

/* ── LOG ── */
.log-wrap{background:rgba(10,6,8,.9);border:1px solid rgba(201,168,76,.1);
  border-radius:8px;padding:12px 14px;margin-top:14px;max-height:120px;overflow-y:auto;}
.log-line{font-size:.72rem;color:#7a6858;line-height:1.8;
  border-bottom:1px solid rgba(255,255,255,.04);padding-bottom:2px;}
.log-line:first-child{color:var(--text);}
.log-line.crit{color:#e74c3c;} .log-line.loot{color:var(--gold);}
.log-line.level{color:var(--green);} .log-line.magic{color:#5dade2;}

/* ── GAME OVER ── */
.gameover-wrap{text-align:center;padding:40px 20px;}
.gameover-title{font-family:'UnifrakturMaguntia',cursive;font-size:4rem;color:#c0392b;
  text-shadow:0 0 30px rgba(192,57,43,.8),0 0 60px rgba(192,57,43,.4);
  animation:flicker 2s ease-in-out infinite;}
@keyframes flicker{0%,100%{opacity:1;}45%{opacity:.9;}50%{opacity:.6;}55%{opacity:.9;}}
.gameover-stats{background:rgba(20,10,12,.9);border:1px solid rgba(192,57,43,.3);
  border-radius:10px;padding:20px;margin:20px auto;max-width:320px;font-size:.82rem;line-height:2;}

.section-hdr{font-family:'Cinzel Decorative',serif;font-size:.72rem;letter-spacing:.2em;
  text-transform:uppercase;color:#5a4030;margin-bottom:10px;margin-top:4px;
  border-bottom:1px solid rgba(201,168,76,.1);padding-bottom:6px;}

::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:rgba(201,168,76,.3);border-radius:2px;}
</style>
""", unsafe_allow_html=True)


# ============================================================
# CONSTANTES
# ============================================================
CLASSES = {
    "Guerreiro": {
        "icon": "🛡️", "sprite": "⚔️",
        "hp": 180, "mana": 30, "atk": 14, "def_val": 9,
        "weapon": {"name": "Espada Curta",  "atk": 14, "type": "weapon", "rarity": "comum", "value": 30},
        "armor":  {"name": "Cota de Ferro", "def": 9,  "type": "armor",  "rarity": "comum", "value": 25},
        "desc": "Resistência incomparável. Bloqueia 20% de todo dano recebido.",
        "special": "block",
        "stats": {"força": 4, "agilidade": 2, "magia": 1},
    },
    "Mago": {
        "icon": "🔮", "sprite": "🔮",
        "hp": 90, "mana": 140, "atk": 10, "def_val": 3,
        "weapon": {"name": "Cajado Aprendiz", "atk": 10, "type": "weapon", "rarity": "comum", "value": 30},
        "armor":  {"name": "Manto de Linho",  "def": 3,  "type": "armor",  "rarity": "comum", "value": 20},
        "desc": "Devastação arcana. Itens RAROS amplificam magias em +70%.",
        "special": "magic",
        "stats": {"força": 1, "agilidade": 2, "magia": 5},
    },
    "Berserker": {
        "icon": "🪓", "sprite": "🪓",
        "hp": 220, "mana": 20, "atk": 12, "def_val": 4,
        "weapon": {"name": "Machado Gasto", "atk": 12, "type": "weapon", "rarity": "comum", "value": 30},
        "armor":  {"name": "Pelagem Grossa", "def": 4, "type": "armor",  "rarity": "comum", "value": 20},
        "desc": "Fúria incontrolável. Abaixo de 20% de vida: +90% de dano.",
        "special": "fury",
        "stats": {"força": 5, "agilidade": 3, "magia": 0},
    },
    "Assassino": {
        "icon": "🗡️", "sprite": "🥷",
        "hp": 115, "mana": 55, "atk": 18, "def_val": 2,
        "weapon": {"name": "Adagas Duplas", "atk": 18, "type": "weapon", "rarity": "comum", "value": 30},
        "armor":  {"name": "Couro Negro",   "def": 2,  "type": "armor",  "rarity": "comum", "value": 20},
        "desc": "Letal e evasivo. 30% esquiva, 25% atordoamento (stun).",
        "special": "stun",
        "stats": {"força": 3, "agilidade": 5, "magia": 2},
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
        {"name": "Espada Longa",     "atk": 36, "price": 140, "type": "weapon", "rarity": "comum",    "value": 65},
        {"name": "Machado de Guerra","atk": 42,  "price": 160, "type": "weapon", "rarity": "comum",    "value": 75},
        {"name": "Glaive Sombrio",   "atk": 52,  "price": 200, "type": "weapon", "rarity": "incomum",  "value": 95},
        {"name": "Lâmina da Ruína",  "atk": 75,  "price": 320, "type": "weapon", "rarity": "raro",     "value": 160},
        {"name": "DESTRUIDORA",      "atk": 130, "price": 550, "type": "weapon", "rarity": "lendário", "value": 270},
    ],
    "armor": [
        {"name": "Cota de Malha",        "def": 18, "price": 120, "type": "armor", "rarity": "comum",   "value": 55},
        {"name": "Escudo Cruzado",        "def": 25, "price": 160, "type": "armor", "rarity": "comum",   "value": 70},
        {"name": "Armadura das Trevas",   "def": 35, "price": 220, "type": "armor", "rarity": "incomum", "value": 100},
        {"name": "Égide Arcana",          "def": 50, "price": 350, "type": "armor", "rarity": "raro",    "value": 175},
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

# Animation constants
ANIM_NONE         = ""
ANIM_HERO_ATTACK  = "anim-hero-attack"
ANIM_HERO_MAGIC   = "anim-hero-magic"
ANIM_HERO_HIT     = "anim-hero-hit"
ANIM_HERO_DODGE   = "anim-hero-dodge"
ANIM_HERO_BLOCK   = "anim-hero-block"
ANIM_HERO_FURY    = "anim-hero-fury"
ANIM_HERO_DEATH   = "anim-hero-death"
ANIM_ENEMY_HIT    = "anim-enemy-hit"
ANIM_ENEMY_STUN   = "anim-enemy-stun"
ANIM_ENEMY_DEATH  = "anim-enemy-death"


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
        'game_active': True, 'hero_class': role,
        'hp': c['hp'], 'max_hp': c['hp'],
        'mana': c['mana'], 'max_mana': c['mana'],
        'gold': 120, 'weapon': dict(c['weapon']), 'armor': dict(c['armor']),
        'state': 'playing', 'floor': 1, 'kills': 0, 'kills_needed': 3,
        'inventory': [], 'market_stock': [], 'total_kills': 0,
        'gold_earned': 120, 'enemy': None, 'blocked_last': False,
        'arena_anim': ANIM_NONE, 'arena_dmg_hero': None,
        'arena_dmg_enemy': None, 'arena_dmg_kind': '', 'dying_enemy': None,
        'log': [{"t": time.strftime('%H:%M'),
                 "msg": f"⚔️ {role} entra no castelo maldito...", "kind": "level"}],
    })
    st.rerun()


# ============================================================
# COMBAT LOGIC
# ============================================================
def player_attack(magic: bool = False):
    ss      = st.session_state
    en      = ss.enemy
    if not en:
        return

    base_atk = ss.weapon['atk']
    hp_pct   = ss.hp / ss.max_hp
    is_fury  = ss.hero_class == "Berserker" and hp_pct < 0.2
    is_rare  = ss.weapon.get('rarity') in ('raro', 'lendário')

    # ── Player hits enemy ──
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
        hero_anim = ANIM_HERO_MAGIC
        dmg_kind  = "dmg-magic"
    else:
        dmg = base_atk + random.randint(4, 14)
        if is_fury:
            dmg = int(dmg * 1.9)
            log("🔥 FÚRIA! Dano devastador!", "crit")
            hero_anim = ANIM_HERO_FURY
        else:
            hero_anim = ANIM_HERO_ATTACK
        dmg_kind = "dmg-enemy"

    # Stun
    stun = False
    if ss.hero_class == "Assassino" and not magic and random.random() < 0.25:
        stun = True
        en['stunned'] = True
        log("⚡ STUN! Inimigo paralisado!", "crit")
        enemy_anim = ANIM_ENEMY_STUN
    else:
        enemy_anim = ANIM_ENEMY_HIT

    en['hp'] -= dmg
    log(f"⚔️ Você causou {dmg} de dano em {en['name']}!", "")

    # ── Enemy dies ──
    if en['hp'] <= 0:
        gold_gain = 45 + ss.floor * 12 + random.randint(0, 20)
        ss.gold        += gold_gain
        ss.gold_earned += gold_gain
        ss.kills       += 1
        ss.total_kills += 1
        log(f"💀 {en['name']} foi derrotado! +{gold_gain}G", "loot")

        if random.random() < 0.20 + ss.floor * 0.03:
            dropped = random.choice(generate_market())
            dropped["price"] = 0
            ss.inventory.append(dropped)
            log(f"🎁 Item largado: {dropped['name']}!", "loot")

        ss.arena_anim      = ANIM_ENEMY_DEATH
        ss.arena_dmg_enemy = dmg
        ss.arena_dmg_kind  = dmg_kind
        ss.arena_dmg_hero  = None
        ss['dying_enemy']  = dict(en)
        ss.enemy           = None

        if ss.kills >= ss.kills_needed:
            ss.floor       += 1
            ss.kills        = 0
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
        ss.arena_anim      = hero_anim
        ss.arena_dmg_enemy = dmg
        ss.arena_dmg_hero  = None
        ss.arena_dmg_kind  = dmg_kind
    else:
        if ss.hero_class == "Assassino" and random.random() < 0.30:
            log("💨 Você esquivou do ataque!", "")
            ss.arena_anim      = ANIM_HERO_DODGE
            ss.arena_dmg_enemy = dmg
            ss.arena_dmg_hero  = None
            ss.arena_dmg_kind  = dmg_kind
        else:
            reduction   = ss.armor['def']
            block_bonus = 0
            if ss.hero_class == "Guerreiro" and random.random() < 0.20:
                block_bonus = en['atk'] // 2
                ss.blocked_last = True
                log("🛡️ Bloqueio! Dano reduzido!", "")
                used_hero_anim = ANIM_HERO_BLOCK
            else:
                ss.blocked_last = False
                used_hero_anim  = ANIM_HERO_HIT

            edmg      = max(2, en['atk'] - reduction - block_bonus)
            ss.hp    -= edmg
            log(f"👹 {en['name']} causou {edmg} de dano!", "crit")

            ss.arena_anim      = used_hero_anim
            ss.arena_dmg_enemy = dmg
            ss.arena_dmg_hero  = edmg
            ss.arena_dmg_kind  = dmg_kind

            if ss.hp <= 0:
                ss.hp         = 0
                ss.arena_anim = ANIM_HERO_DEATH
                ss.state      = 'player_dead'

    st.rerun()


# ============================================================
# PIXEL-ART SPRITE DEFINITIONS  (pure CSS box-shadow art)
# Each sprite = list of (col, row, hex_color), 1-indexed top-left.
# Rendered as a 1px div scaled via box-shadow — no images, no emojis.
# ============================================================
def _px_to_shadow(pixels, scale=3):
    return ", ".join(f"{c*scale}px {r*scale}px 0 {col}" for c, r, col in pixels)

WARRIOR_PX = [
    (6,1,"#a0a0c0"),(7,1,"#c0c0e0"),(8,1,"#c0c0e0"),(9,1,"#a0a0c0"),
    (5,2,"#8080a0"),(6,2,"#c0c0e0"),(7,2,"#e0e0ff"),(8,2,"#e0e0ff"),(9,2,"#c0c0e0"),(10,2,"#8080a0"),
    (5,3,"#8080a0"),(6,3,"#c9a84c"),(7,3,"#f0d080"),(8,3,"#f0d080"),(9,3,"#c9a84c"),(10,3,"#8080a0"),
    (6,4,"#a0a0c0"),(7,4,"#d4b896"),(8,4,"#d4b896"),(9,4,"#a0a0c0"),
    (5,5,"#6060a0"),(6,5,"#8080c0"),(7,5,"#a0a0e0"),(8,5,"#a0a0e0"),(9,5,"#8080c0"),(10,5,"#6060a0"),
    (4,6,"#404080"),(5,6,"#6060a0"),(6,6,"#c9a84c"),(7,6,"#8080c0"),(8,6,"#8080c0"),(9,6,"#c9a84c"),(10,6,"#6060a0"),(11,6,"#404080"),
    (4,7,"#404080"),(5,7,"#6060a0"),(6,7,"#8080c0"),(7,7,"#a0a0e0"),(8,7,"#a0a0e0"),(9,7,"#8080c0"),(10,7,"#6060a0"),(11,7,"#404080"),
    (5,8,"#303070"),(6,8,"#6060a0"),(7,8,"#8080c0"),(8,8,"#8080c0"),(9,8,"#6060a0"),(10,8,"#303070"),
    (11,3,"#e0e0e0"),(12,2,"#f0f0f0"),(13,1,"#ffffff"),
    (11,4,"#c0c0c0"),(10,4,"#c9a84c"),(11,5,"#c9a84c"),
    (5,9,"#303070"),(6,9,"#505090"),(7,9,"#303070"),(8,9,"#303070"),(9,9,"#505090"),(10,9,"#303070"),
    (5,10,"#202060"),(6,10,"#404080"),(7,10,"#202060"),(8,10,"#202060"),(9,10,"#404080"),(10,10,"#202060"),
    (5,11,"#181850"),(6,11,"#303070"),(9,11,"#303070"),(10,11,"#181850"),
    (5,12,"#101040"),(6,12,"#202060"),(9,12,"#202060"),(10,12,"#101040"),
]
MAGE_PX = [
    (7,1,"#4a0080"),(8,1,"#c9a84c"),
    (6,2,"#6000a0"),(7,2,"#8000d0"),(8,2,"#8000d0"),(9,2,"#6000a0"),
    (5,3,"#5000a0"),(6,3,"#7000c0"),(7,3,"#9000f0"),(8,3,"#9000f0"),(9,3,"#7000c0"),(10,3,"#5000a0"),
    (6,4,"#d4b896"),(7,4,"#e8cca8"),(8,4,"#e8cca8"),(9,4,"#d4b896"),
    (6,5,"#d4b896"),(7,5,"#20a0ff"),(8,5,"#20a0ff"),(9,5,"#d4b896"),
    (6,6,"#c4a886"),(7,6,"#d4b896"),(8,6,"#d4b896"),(9,6,"#c4a886"),
    (5,7,"#3000a0"),(6,7,"#5000c0"),(7,7,"#6000e0"),(8,7,"#6000e0"),(9,7,"#5000c0"),(10,7,"#3000a0"),
    (4,8,"#2000a0"),(5,8,"#4000c0"),(6,8,"#00e5ff"),(7,8,"#5000d0"),(8,8,"#5000d0"),(9,8,"#00e5ff"),(10,8,"#4000c0"),(11,8,"#2000a0"),
    (4,9,"#2000a0"),(5,9,"#4000c0"),(6,9,"#5000d0"),(7,9,"#6000e0"),(8,9,"#6000e0"),(9,9,"#5000d0"),(10,9,"#4000c0"),(11,9,"#2000a0"),
    (5,10,"#3000a0"),(6,10,"#4000c0"),(7,10,"#5000d0"),(8,10,"#5000d0"),(9,10,"#4000c0"),(10,10,"#3000a0"),
    (12,5,"#00e5ff"),(13,4,"#80f0ff"),(12,4,"#00e5ff"),(13,3,"#ffffff"),(12,3,"#80f0ff"),
    (11,6,"#4000c0"),(12,6,"#6000e0"),(11,7,"#3000a0"),
    (6,11,"#3000a0"),(7,11,"#2000a0"),(8,11,"#2000a0"),(9,11,"#3000a0"),
    (6,12,"#2000a0"),(9,12,"#2000a0"),
]
BERSERK_PX = [
    (4,1,"#8b0000"),(5,1,"#a00000"),(8,1,"#a00000"),(9,1,"#8b0000"),(11,1,"#8b0000"),
    (5,2,"#c00000"),(6,2,"#8b0000"),(7,2,"#8b0000"),(8,2,"#8b0000"),(9,2,"#c00000"),(10,2,"#8b0000"),
    (5,3,"#d4b896"),(6,3,"#d4b896"),(7,3,"#e8cca8"),(8,3,"#e8cca8"),(9,3,"#d4b896"),(10,3,"#d4b896"),
    (5,4,"#d4b896"),(6,4,"#ff4040"),(7,4,"#d4b896"),(8,4,"#d4b896"),(9,4,"#ff4040"),(10,4,"#d4b896"),
    (5,5,"#c4a886"),(6,5,"#d4b896"),(7,5,"#8b0000"),(8,5,"#8b0000"),(9,5,"#d4b896"),(10,5,"#c4a886"),
    (4,6,"#6b3a2a"),(5,6,"#8b4a3a"),(6,6,"#a05a4a"),(7,6,"#b06a5a"),(8,6,"#b06a5a"),(9,6,"#a05a4a"),(10,6,"#8b4a3a"),(11,6,"#6b3a2a"),
    (3,7,"#5b2a1a"),(4,7,"#7b3a2a"),(5,7,"#ff6a00"),(6,7,"#8b4a3a"),(7,7,"#a05a4a"),(8,7,"#a05a4a"),(9,7,"#8b4a3a"),(10,7,"#ff6a00"),(11,7,"#7b3a2a"),(12,7,"#5b2a1a"),
    (3,8,"#4b1a0a"),(4,8,"#6b2a1a"),(5,8,"#8b3a2a"),(6,8,"#a04a3a"),(7,8,"#b05a4a"),(8,8,"#b05a4a"),(9,8,"#a04a3a"),(10,8,"#8b3a2a"),(11,8,"#6b2a1a"),(12,8,"#4b1a0a"),
    (13,5,"#808080"),(14,4,"#a0a0a0"),(14,5,"#c0c0c0"),(14,6,"#a0a0a0"),(13,6,"#808080"),
    (12,6,"#c9a84c"),(12,7,"#c9a84c"),(12,8,"#c9a84c"),
    (5,9,"#5b2a1a"),(6,9,"#6b3a2a"),(7,9,"#4b1a0a"),(8,9,"#4b1a0a"),(9,9,"#6b3a2a"),(10,9,"#5b2a1a"),
    (5,10,"#4b1a0a"),(6,10,"#5b2a1a"),(9,10,"#5b2a1a"),(10,10,"#4b1a0a"),
    (5,11,"#3b0a00"),(6,11,"#4b1a0a"),(9,11,"#4b1a0a"),(10,11,"#3b0a00"),
]
ASSASSIN_PX = [
    (6,1,"#1a1a2e"),(7,1,"#2a2a3e"),(8,1,"#2a2a3e"),(9,1,"#1a1a2e"),
    (5,2,"#1a1a2e"),(6,2,"#2a2a3e"),(7,2,"#3a3a4e"),(8,2,"#3a3a4e"),(9,2,"#2a2a3e"),(10,2,"#1a1a2e"),
    (5,3,"#1a1a2e"),(6,3,"#2a2a3e"),(7,3,"#d4b896"),(8,3,"#d4b896"),(9,3,"#2a2a3e"),(10,3,"#1a1a2e"),
    (5,4,"#1a1a2e"),(6,4,"#d4b896"),(7,4,"#ff3333"),(8,4,"#ff3333"),(9,4,"#d4b896"),(10,4,"#1a1a2e"),
    (5,5,"#1a1a2e"),(6,5,"#2a2a3e"),(7,5,"#d4b896"),(8,5,"#d4b896"),(9,5,"#2a2a3e"),(10,5,"#1a1a2e"),
    (5,6,"#0a0a1a"),(6,6,"#1a1a2e"),(7,6,"#2a2a3e"),(8,6,"#2a2a3e"),(9,6,"#1a1a2e"),(10,6,"#0a0a1a"),
    (4,7,"#0a0a1a"),(5,7,"#1a1a2e"),(6,7,"#c9a84c"),(7,7,"#2a2a3e"),(8,7,"#2a2a3e"),(9,7,"#c9a84c"),(10,7,"#1a1a2e"),(11,7,"#0a0a1a"),
    (4,8,"#0a0a1a"),(5,8,"#1a1a2e"),(6,8,"#2a2a3e"),(7,8,"#3a3a4e"),(8,8,"#3a3a4e"),(9,8,"#2a2a3e"),(10,8,"#1a1a2e"),(11,8,"#0a0a1a"),
    (11,5,"#c0c0c0"),(12,4,"#e0e0e0"),(13,3,"#ffffff"),
    (3,5,"#c0c0c0"),(2,4,"#e0e0e0"),(1,3,"#ffffff"),
    (5,9,"#0a0a1a"),(6,9,"#1a1a2e"),(7,9,"#0a0a1a"),(8,9,"#0a0a1a"),(9,9,"#1a1a2e"),(10,9,"#0a0a1a"),
    (5,10,"#0a0a1a"),(6,10,"#1a1a2e"),(9,10,"#1a1a2e"),(10,10,"#0a0a1a"),
    (5,11,"#050510"),(6,11,"#0a0a1a"),(9,11,"#0a0a1a"),(10,11,"#050510"),
]
SKELETON_PX = [
    (7,1,"#e8e8e8"),(8,1,"#e8e8e8"),
    (6,2,"#d0d0d0"),(7,2,"#f0f0f0"),(8,2,"#f0f0f0"),(9,2,"#d0d0d0"),
    (6,3,"#d0d0d0"),(7,3,"#202020"),(8,3,"#202020"),(9,3,"#d0d0d0"),
    (6,4,"#c0c0c0"),(7,4,"#f0f0f0"),(8,4,"#f0f0f0"),(9,4,"#c0c0c0"),
    (6,5,"#d0d0d0"),(7,5,"#b0b0b0"),(8,5,"#b0b0b0"),(9,5,"#d0d0d0"),
    (5,6,"#c0c0c0"),(7,6,"#e0e0e0"),(8,6,"#e0e0e0"),(10,6,"#c0c0c0"),
    (5,7,"#b0b0b0"),(6,7,"#c0c0c0"),(7,7,"#d0d0d0"),(8,7,"#d0d0d0"),(9,7,"#c0c0c0"),(10,7,"#b0b0b0"),
    (5,8,"#c0c0c0"),(7,8,"#e0e0e0"),(8,8,"#e0e0e0"),(10,8,"#c0c0c0"),
    (5,9,"#b0b0b0"),(6,9,"#c0c0c0"),(9,9,"#c0c0c0"),(10,9,"#b0b0b0"),
    (6,10,"#c0c0c0"),(7,10,"#a0a0a0"),(8,10,"#a0a0a0"),(9,10,"#c0c0c0"),
    (6,11,"#b0b0b0"),(7,11,"#909090"),(8,11,"#909090"),(9,11,"#b0b0b0"),
    (6,12,"#808080"),(9,12,"#808080"),
    (11,4,"#d0d0d0"),(12,3,"#e8e8e8"),(13,2,"#ffffff"),
    (10,5,"#a0a0a0"),(11,5,"#b0b0b0"),
]
MONSTER_PX = [
    (5,1,"#8b0000"),(4,1,"#a00000"),(10,1,"#8b0000"),(11,1,"#a00000"),
    (5,2,"#2d5a1b"),(6,2,"#3d7a2b"),(7,2,"#4d8a3b"),(8,2,"#4d8a3b"),(9,2,"#3d7a2b"),(10,2,"#2d5a1b"),
    (4,3,"#2d5a1b"),(5,3,"#3d7a2b"),(6,3,"#ff4040"),(7,3,"#4d8a3b"),(8,3,"#4d8a3b"),(9,3,"#ff4040"),(10,3,"#3d7a2b"),(11,3,"#2d5a1b"),
    (4,4,"#2d5a1b"),(5,4,"#3d7a2b"),(6,4,"#4d8a3b"),(7,4,"#ff8800"),(8,4,"#ff8800"),(9,4,"#4d8a3b"),(10,4,"#3d7a2b"),(11,4,"#2d5a1b"),
    (4,5,"#1d4a0b"),(5,5,"#2d5a1b"),(6,5,"#ffffff"),(7,5,"#3d7a2b"),(8,5,"#3d7a2b"),(9,5,"#ffffff"),(10,5,"#2d5a1b"),(11,5,"#1d4a0b"),
    (4,6,"#1d4a0b"),(5,6,"#2d5a1b"),(6,6,"#3d7a2b"),(7,6,"#4d8a3b"),(8,6,"#4d8a3b"),(9,6,"#3d7a2b"),(10,6,"#2d5a1b"),(11,6,"#1d4a0b"),
    (3,7,"#1a3a08"),(4,7,"#2d5a1b"),(5,7,"#c0392b"),(6,7,"#3d7a2b"),(7,7,"#4d8a3b"),(8,7,"#4d8a3b"),(9,7,"#3d7a2b"),(10,7,"#c0392b"),(11,7,"#2d5a1b"),(12,7,"#1a3a08"),
    (3,8,"#1a3a08"),(4,8,"#2d5a1b"),(5,8,"#3d7a2b"),(6,8,"#4d8a3b"),(7,8,"#5d9a4b"),(8,8,"#5d9a4b"),(9,8,"#4d8a3b"),(10,8,"#3d7a2b"),(11,8,"#2d5a1b"),(12,8,"#1a3a08"),
    (3,9,"#8b0000"),(2,10,"#a00000"),(3,10,"#8b0000"),(12,9,"#8b0000"),(13,10,"#a00000"),(12,10,"#8b0000"),
    (5,9,"#1d4a0b"),(6,9,"#2d5a1b"),(7,9,"#1d4a0b"),(8,9,"#1d4a0b"),(9,9,"#2d5a1b"),(10,9,"#1d4a0b"),
    (5,10,"#1a3a08"),(6,10,"#2d5a1b"),(9,10,"#2d5a1b"),(10,10,"#1a3a08"),
    (5,11,"#101808"),(6,11,"#1a3a08"),(9,11,"#1a3a08"),(10,11,"#101808"),
]
DRAGON_PX = [
    (1,3,"#8b0000"),(2,2,"#a00000"),(2,3,"#8b0000"),(3,2,"#c00000"),(3,3,"#a00000"),(1,4,"#700000"),(2,4,"#8b0000"),(3,4,"#8b0000"),
    (13,3,"#8b0000"),(12,2,"#a00000"),(12,3,"#8b0000"),(11,2,"#c00000"),(11,3,"#a00000"),(13,4,"#700000"),(12,4,"#8b0000"),(11,4,"#8b0000"),
    (5,2,"#c0392b"),(6,2,"#e74c3c"),(7,2,"#ff5555"),(8,2,"#ff5555"),(9,2,"#e74c3c"),(10,2,"#c0392b"),
    (5,3,"#e74c3c"),(6,3,"#ff8800"),(7,3,"#e74c3c"),(8,3,"#e74c3c"),(9,3,"#ff8800"),(10,3,"#e74c3c"),
    (4,4,"#c0392b"),(5,4,"#e74c3c"),(6,4,"#ff8800"),(7,4,"#ffcc00"),(8,4,"#ffcc00"),(9,4,"#ff8800"),(10,4,"#e74c3c"),(11,4,"#c0392b"),
    (4,5,"#ff8800"),(3,5,"#ffcc00"),(2,5,"#ff4400"),(1,5,"#ff8800"),(3,6,"#ffcc00"),(2,6,"#ff8800"),
    (5,5,"#c0392b"),(6,5,"#e74c3c"),(7,5,"#ff5555"),(8,5,"#ff5555"),(9,5,"#e74c3c"),(10,5,"#c0392b"),
    (5,6,"#a0392b"),(6,6,"#c0392b"),(7,6,"#e74c3c"),(8,6,"#e74c3c"),(9,6,"#c0392b"),(10,6,"#a0392b"),
    (5,7,"#a0392b"),(6,7,"#c0392b"),(7,7,"#ffcc00"),(8,7,"#ffcc00"),(9,7,"#c0392b"),(10,7,"#a0392b"),
    (10,8,"#8b0000"),(11,8,"#a00000"),(12,9,"#8b0000"),(13,10,"#700000"),
    (5,8,"#8b2a1a"),(6,8,"#a0392b"),(9,8,"#a0392b"),(10,8,"#8b2a1a"),
    (5,9,"#701a0a"),(6,9,"#8b2a1a"),(9,9,"#8b2a1a"),(10,9,"#701a0a"),
]
GHOST_PX = [
    (7,1,"#aaaaee"),(8,1,"#aaaaee"),
    (6,2,"#bbbbff"),(7,2,"#ccccff"),(8,2,"#ccccff"),(9,2,"#bbbbff"),
    (5,3,"#aaaaee"),(6,3,"#00e5ff"),(7,3,"#ccccff"),(8,3,"#ccccff"),(9,3,"#00e5ff"),(10,3,"#aaaaee"),
    (5,4,"#aaaaee"),(6,4,"#bbbbff"),(7,4,"#ddddff"),(8,4,"#ddddff"),(9,4,"#bbbbff"),(10,4,"#aaaaee"),
    (5,5,"#9999dd"),(6,5,"#aaaaee"),(7,5,"#bbbbff"),(8,5,"#bbbbff"),(9,5,"#aaaaee"),(10,5,"#9999dd"),
    (5,6,"#9999dd"),(6,6,"#aaaaee"),(7,6,"#bbbbff"),(8,6,"#bbbbff"),(9,6,"#aaaaee"),(10,6,"#9999dd"),
    (5,7,"#8888cc"),(6,7,"#9999dd"),(7,7,"#aaaaee"),(8,7,"#aaaaee"),(9,7,"#9999dd"),(10,7,"#8888cc"),
    (5,8,"#7777bb"),(6,8,"#8888cc"),(7,8,"#7777bb"),(8,8,"#7777bb"),(9,8,"#8888cc"),(10,8,"#7777bb"),
    (5,9,"#6666aa"),(7,9,"#5555aa"),(8,9,"#5555aa"),(10,9,"#6666aa"),
    (6,10,"#5555aa"),(9,10,"#5555aa"),
]

def _enemy_sprite_px(enemy_name: str):
    n = enemy_name.lower()
    if any(k in n for k in ("esqueleto","torto","osso")):   return SKELETON_PX
    if any(k in n for k in ("dragão","dragao","dragon")):   return DRAGON_PX
    if any(k in n for k in ("espectro","fantasma","sombra","arcanista","lich","devorador")):
        return GHOST_PX
    return MONSTER_PX

def _hero_sprite_px(hero_class: str):
    return {"Guerreiro": WARRIOR_PX, "Mago": MAGE_PX,
            "Berserker": BERSERK_PX, "Assassino": ASSASSIN_PX}.get(hero_class, WARRIOR_PX)


# ============================================================
# ARENA RENDERER  — st.components.v1.html (zero Streamlit escaping)
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
    ss.arena_dmg_kind  = ""
    if not enemy:
        ss['dying_enemy'] = None


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
    </div>
    """, unsafe_allow_html=True)


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
            st.markdown('<div class="btn-attack">', unsafe_allow_html=True)
            if st.button("⚔️ ATACAR", key="btn_attack"):
                player_attack(magic=False)
            st.markdown('</div>', unsafe_allow_html=True)

        if ss.hero_class == "Mago":
            with c2:
                st.markdown('<div class="btn-magic">', unsafe_allow_html=True)
                if st.button("🔥 MAGIA  (15 Mana)", key="btn_magic"):
                    player_attack(magic=True)
                st.markdown('</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="btn-explore">', unsafe_allow_html=True)
        if st.button("👣 EXPLORAR A SALA", key="btn_explore"):
            if random.random() < 0.50:
                gain = 35 + ss.floor * 12 + random.randint(0, 18)
                ss.gold += gain; ss.gold_earned += gain
                log(f"🎁 Baú encontrado! +{gain}G", "loot")
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
            st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
            if st.button("Equipar", key=f"equip_{i}"):
                old = ss[item['type']]; ss[item['type']] = item; ss.inventory[i] = old
                log(f"🔄 Equipou: {item['name']}!", ""); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            sv = item.get('value', 10)
            if st.button(f"Vender +{sv}G", key=f"sell_inv_{i}"):
                ss.gold += sv; ss.inventory.pop(i)
                log(f"💰 Vendeu {item['name']} por {sv}G", "loot"); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


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
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button("❤️ Vida +50 HP\n(40G)", key="pot_hp"):
            if ss.gold >= 40:
                ss.gold -= 40; healed = min(ss.max_hp, ss.hp+50)-ss.hp; ss.hp += healed
                log(f"❤️ Poção de vida: +{healed} HP", "loot"); st.rerun()
            else: st.warning("Ouro insuficiente!")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="btn-magic">', unsafe_allow_html=True)
        if st.button("🔮 Mana +40\n(40G)", key="pot_mp"):
            if ss.gold >= 40:
                ss.gold -= 40; restored = min(ss.max_mana, ss.mana+40)-ss.mana; ss.mana += restored
                log(f"🔮 Poção de mana: +{restored} Mana", "magic"); st.rerun()
            else: st.warning("Ouro insuficiente!")
        st.markdown('</div>', unsafe_allow_html=True)

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
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button(f"Comprar {item['name']}", key=f"buy_{i}"):
            if ss.gold >= item['price']:
                ss.gold -= item['price']; ss.inventory.append(dict(item)); ss.market_stock.pop(i)
                log(f"🛒 Comprou: {item['name']}!", "loot")
                if not ss.market_stock: ss.market_stock = generate_market()
                st.rerun()
            else: st.warning("Ouro insuficiente!")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='section-hdr' style='margin-top:14px'>Vender Inventário</div>", unsafe_allow_html=True)
    if not ss.inventory:
        st.markdown('<div style="color:#5a4030;font-size:.78rem">— Nada para vender —</div>', unsafe_allow_html=True)
    else:
        for i, item in enumerate(ss.inventory):
            sv = item.get('value', 10)
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            if st.button(f"Vender {item['name']} (+{sv}G)", key=f"sell_mkt_{i}"):
                ss.gold += sv; ss.inventory.pop(i)
                log(f"💰 Vendeu {item['name']} por {sv}G", "loot"); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


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
        reset_state(); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# ████████  VICTORY  ████████
# ============================================================
def render_victory():
    ss = st.session_state
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

    st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
    if st.button("🏆 JOGAR NOVAMENTE"):
        reset_state(); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# ████████  ROUTER  ████████
# ============================================================
state = st.session_state.state

if   state == 'menu':        render_menu()
elif state == 'playing':     render_game()
elif state == 'player_dead': render_gameover()
elif state == 'victory':     render_victory()
