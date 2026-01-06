import streamlit as st
import random
import time

# --- ESTÉTICA, UI E ANIMAÇÕES ---
st.set_page_config(page_title="Dark Castle: Animations", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    .stApp { background-color: #050505; font-family: 'VT323', monospace; color: #4af626; font-size: 20px; }
    
    /* Animação: Morte do Monstro */
    @keyframes monsterDeath {
        0% { transform: scale(1) rotate(0deg); opacity: 1; }
        20% { transform: scale(1.2) rotate(10deg); color: red; }
        100% { transform: scale(0) rotate(-45deg); opacity: 0; }
    }
    .monster-die { animation: monsterDeath 1.5s forwards; text-align: center; font-size: 40px; }

    /* Animação: Explosão do Player */
    @keyframes explode {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(2); color: orange; }
        100% { transform: scale(0); opacity: 0; }
    }
    .player-explode { animation: explode 1s infinite; font-size: 50px; text-align: center; }

    /* Animação: Comemoração */
    @keyframes celebrate {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px) scale(1.1); color: gold; }
    }
    .victory-jump { animation: celebrate 0.5s infinite; font-size: 60px; text-align: center; }

    /* Estilo do Boss Fatiado */
    .boss-sliced { 
        color: #ff0000; font-weight: bold; text-shadow: 2px 2px #550000;
        letter-spacing: 5px; transform: skewX(-20deg);
    }

    .hero-panel { background: rgba(0, 255, 0, 0.05); border: 2px solid #4af626; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO ---
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False, 'hero_class': "Viajante", 'level': 1, 'hp': 100, 'max_hp': 100, 
        'mana': 50, 'gold': 0, 'log': ["O destino te chama..."], 'enemy': None,
        'weapon': {"name": "Punhal Enferrujado", "atk": 8, "type": "weapon"},
        'armor': {"name": "Trapos de Couro", "def": 2, "type": "armor"},
        'floor': 1, 'kills_on_floor': 0, 'in_shop': False, 'chest_found': False,
        'inventory': [], 'game_state': 'playing' # playing, player_win, player_dead
    })

def add_log(msg):
    st.session_state.log.insert(0, msg)

# --- SISTEMA DE COMBATE COM ANIMAÇÃO ---
def combat_turn(action):
    enemy = st.session_state.enemy
    # Player Ataca
    dmg = st.session_state.weapon['atk'] + random.randint(5, 12)
    if action == "magic":
        if st.session_state.mana >= 25:
            st.session_state.mana -= 25
            dmg += 40
        else: add_log("❌ Sem mana!"); return

    enemy['hp'] -= dmg
    add_log(f"⚔️ Causou {dmg} de dano!")

    if enemy['hp'] <= 0:
        if enemy['name'] == "🔥 LORDE DAS SOMBRAS":
            st.session_state.game_state = 'player_win'
        else:
            st.session_state.game_state = 'monster_dying'
        return

    # Inimigo Ataca
    edmg = max(2, enemy.get('atk', 15) - st.session_state.armor['def'])
    st.session_state.hp -= edmg
    add_log(f"🩸 Recebeu {edmg} de dano!")

    if st.session_state.hp <= 0:
        st.session_state.hp = 0
        st.session_state.game_state = 'player_dead'

# --- TELAS DE JOGO ---

# 1. TELA DE MORTE DO PLAYER
if st.session_state.game_state == 'player_dead':
    st.markdown("<div class='player-explode'># % * . #<br>💥 EXPLODINDO 💥<br>. * # % .</div>", unsafe_allow_html=True)
    if st.session_state.enemy and st.session_state.enemy['name'] == "🔥 LORDE DAS SOMBRAS":
        st.markdown("<h1 style='color:red; text-align:center;'>HA HA HA HA... FRACO!<br>O MUNDO CAI EM TREVAS!</h1>", unsafe_allow_html=True)
    st.error("☠️ VOCÊ FOI DERROTADO")
    if st.button("TENTAR NOVAMENTE"): st.session_state.clear(); st.rerun()

# 2. TELA DE VITÓRIA NO BOSS
elif st.session_state.game_state == 'player_win':
    st.markdown("<div class='victory-jump'>🛡️🏆✨<br>VIVA!</div>", unsafe_allow_html=True)
    st.balloons()
    st.success("O LORDE FOI FATIADO EM MIL PEDAÇOS!")
    st.markdown("<h2 class='boss-sliced' style='text-align:center;'>// L // O // R // D // E //</h2>", unsafe_allow_html=True)
    if st.button("RECOMEÇAR LENDA"): st.session_state.clear(); st.rerun()

# 3. TELA DE MORTE DE MONSTRO COMUM
elif st.session_state.game_state == 'monster_dying':
    st.markdown("<div class='monster-die'>💀<br>MONSTRO DERROTADO!</div>", unsafe_allow_html=True)
    time.sleep(1)
    st.session_state.gold += 50
    st.session_state.kills_on_floor += 1
    st.session_state.enemy = None
    st.session_state.game_state = 'playing'
    if st.session_state.kills_on_floor >= 3: # Simplificado para teste
        st.session_state.floor += 1
        st.session_state.kills_on_floor = 0
    st.rerun()

# 4. LOOP PRINCIPAL
elif not st.session_state.game_active:
    st.title("🏰 DARK CASTLE")
    c1, c2 = st.columns(2)
    if c1.button("🛡️ GUERREIRO"): 
        st.session_state.game_active = True
        st.session_state.hero_class = "Guerreiro"
        st.rerun()
    if c2.button("🔮 MAGO"): 
        st.session_state.game_active = True
        st.session_state.hero_class = "Mago"
        st.rerun()

else:
    # PAINEL DO HERÓI (HUD)
    avatar = "🛡️" if st.session_state.hero_class == "Guerreiro" else "🔮"
    hp_p = (st.session_state.hp / st.session_state.max_hp) * 100
    st.markdown(f"""
    <div class="hero-panel">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="font-size: 50px;">{avatar}</div>
            <div style="flex-grow: 1;">
                <div>{st.session_state.hero_class.upper()} | ANDAR {st.session_state.floor}</div>
                <div style="background: #333; width: 100%; height: 12px; border: 1px solid #4af626; margin: 5px 0;">
                    <div style="background: #4af626; width: {hp_p}%; height: 100%;"></div>
                </div>
                <div>HP: {st.session_state.hp}/{st.session_state.max_hp} | 💰 {st.session_state.gold}G</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.enemy:
        enemy = st.session_state.enemy
        st.subheader(f"👹 {enemy['name']}")
        st.progress(max(0, enemy['hp'])/100 if enemy['name'] != "🔥 LORDE DAS SOMBRAS" else max(0, enemy['hp'])/500)
        c1, c2 = st.columns(2)
        if c1.button("⚔️ ATACAR"): combat_turn("attack"); st.rerun()
        if c2.button("🔥 MAGIA"): combat_turn("magic"); st.rerun()

    elif st.session_state.chest_found:
        st.title("🎁 BAÚ ENCONTRADO!")
        if st.button("🔓 ABRIR"):
            st.session_state.inventory.append({"name": "Item Místico", "atk": 20, "type": "weapon"})
            st.session_state.chest_found = False; st.rerun()
    
    else:
        st.title(f"🏰 SALA DE EXPLORAÇÃO")
        if st.button("👣 EXPLORAR PRÓXIMA SALA"):
            if st.session_state.floor == 5:
                st.session_state.enemy = {"name": "🔥 LORDE DAS SOMBRAS", "hp": 500, "atk": 35}
            else:
                roll = random.random()
                if roll < 0.6: st.session_state.enemy = {"name": "Zumbi", "hp": 60, "atk": 15}
                else: st.session_state.chest_found = True
            st.rerun()

    st.divider()
    for line in st.session_state.log[:3]: st.write(f"`{line}`")
