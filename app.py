import streamlit as st
import random

st.set_page_config(page_title="Snake and Ladder Game", page_icon="🎲", layout="centered")

st.title("🐍 Snake and Ladder")
st.write("Roll the dice and reach Square 100 before the computer!")

# Snakes and Ladders mapping
ladders = {
    4: 25,
    13: 46,
    33: 49,
    42: 63,
    50: 69,
    62: 81,
    74: 92
}

snakes = {
    27: 5,
    40: 3,
    43: 18,
    54: 31,
    66: 45,
    76: 58,
    99: 41
}

# --- Session state initialization ---
if "player_pos" not in st.session_state:
    st.session_state.player_pos = 1
if "computer_pos" not in st.session_state:
    st.session_state.computer_pos = 1
if "message" not in st.session_state:
    st.session_state.message = ""
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# --- Game logic helpers ---
def roll_dice():
    return random.randint(1, 6)

def apply_move(position, dice_value):
    new_position = position + dice_value
    if new_position > 100:
        # cannot move if it would go past 100
        return position, f"🎲 Rolled a {dice_value}. Can't move past 100, stay at {position}."
    msg = f"🎲 Rolled a {dice_value}. "
    if new_position in ladders:
        dest = ladders[new_position]
        msg += f"🪜 Ladder! {new_position} → {dest}"
        new_position = dest
    elif new_position in snakes:
        dest = snakes[new_position]
        msg += f"🐍 Snake! {new_position} → {dest}"
        new_position = dest
    else:
        msg += f"Moved to {new_position}."
    return new_position, msg

def player_turn():
    if st.session_state.game_over:
        return
    d = roll_dice()
    new_pos, msg = apply_move(st.session_state.player_pos, d)
    st.session_state.player_pos = new_pos
    st.session_state.message = f"### Your Turn\n{msg}\n"
    if new_pos == 100:
        st.session_state.message += "\n🏆 Congratulations! You won!"
        st.session_state.game_over = True

def computer_turn():
    if st.session_state.game_over:
        return
    d = roll_dice()
    new_pos, msg = apply_move(st.session_state.computer_pos, d)
    st.session_state.computer_pos = new_pos
    # append computer message
    st.session_state.message += f"\n### Computer Turn\n{msg}\n"
    if new_pos == 100:
        st.session_state.message += "\n🤖 Computer wins!"
        st.session_state.game_over = True

def player_roll_and_computer_reply():
    # This callback performs player turn and, if game not over, computer turn.
    player_turn()
    if not st.session_state.game_over:
        computer_turn()

def restart_game():
    st.session_state.player_pos = 1
    st.session_state.computer_pos = 1
    st.session_state.message = ""
    st.session_state.game_over = False

# --- UI ---
st.subheader("Current Positions")
col1, col2 = st.columns(2)
with col1:
    st.metric("😀 You", st.session_state.player_pos)
with col2:
    st.metric("🤖 Computer", st.session_state.computer_pos)

# Buttons
roll_col, restart_col = st.columns([2,1])
with roll_col:
    # disable roll button if game over
    if st.session_state.game_over:
        st.button("🎲 Roll Dice", disabled=True)
    else:
        st.button("🎲 Roll Dice", on_click=player_roll_and_computer_reply)

with restart_col:
    st.button("🔄 Restart Game", on_click=restart_game)

# Messages
if st.session_state.message:
    st.markdown(st.session_state.message)

st.divider()

st.subheader("Game Rules")
st.write("""
- Reach **Square 100** to win.
- Landing on the bottom of a ladder takes you up.
- Landing on a snake's head sends you down.
- If your roll would take you past 100, you stay where you are.
""")
