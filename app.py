import streamlit as st
import random

st.set_page_config(
    page_title="Snake and Ladder Game",
    page_icon="🎲",
    layout="centered"
)

st.title("🐍 Snake and Ladder")
st.write("Roll the dice and reach Square 100 before the computer!")

# Snakes and Ladders
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

# Initialize session state
if "player_pos" not in st.session_state:
    st.session_state.player_pos = 1

if "computer_pos" not in st.session_state:
    st.session_state.computer_pos = 1

if "message" not in st.session_state:
    st.session_state.message = ""

def move(position):
    dice = random.randint(1, 6)
    new_position = position + dice

    if new_position > 100:
        new_position = position

    message = f"🎲 Rolled a {dice}. "

    if new_position in ladders:
        message += f"🪜 Ladder! {new_position} → {ladders[new_position]}"
        new_position = ladders[new_position]
    elif new_position in snakes:
        message += f"🐍 Snake! {new_position} → {snakes[new_position]}"
        new_position = snakes[new_position]

    return new_position, message

st.subheader("Current Positions")

col1, col2 = st.columns(2)

with col1:
    st.metric("😀 You", st.session_state.player_pos)

with col2:
    st.metric("🤖 Computer", st.session_state.computer_pos)

if st.button("🎲 Roll Dice"):
    # Player Turn
    player_pos, player_msg = move(st.session_state.player_pos)
    st.session_state.player_pos = player_pos

    if player_pos == 100:
        st.success("🏆 Congratulations! You won!")
        st.stop()

    # Computer Turn
    computer_pos, computer_msg = move(st.session_state.computer_pos)
    st.session_state.computer_pos = computer_pos

    if computer_pos == 100:
        st.error("🤖 Computer wins!")
        st.stop()

    st.session_state.message = (
        f"### Your Turn\n{player_msg}\n\n"
        f"### Computer Turn\n{computer_msg}"
    )

st.markdown(st.session_state.message)

st.divider()

st.subheader("Game Rules")

st.write("""
- Reach **Square 100** to win.
- Landing on the bottom of a ladder takes you up.
- Landing on a snake's head sends you down.
- If your roll would take you past 100, you stay where you are.
""")

if st.button("🔄 Restart Game"):
    st.session_state.player_pos = 1
    st.session_state.computer_pos = 1
    st.session_state.message = ""
    st.rerun()
