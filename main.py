import streamlit as st
from display import display_cie_color
from app_utils import (
    get_game_settings, 
    get_user_input, 
    plot_plane, 
    set_session_state, 
    game_instructions
)


st.set_page_config(layout="centered")

def run():
    max_tolerance, max_tries, level = get_game_settings()
    set_session_state(max_tries, max_tolerance, level)
    game_instructions()

    container = st.container()
    col1, col2 = container.columns([5,8])

    with col1:
        row1 = st.container()
        row2 = st.container()

        with row2:
                guess, guess_type = get_user_input()
                st.session_state.game_.add_guess(guess, guess_type)
                if st.session_state.game_.game_over:
                    st.write('Game Over. Best guess was:', st.session_state.game_.best_guess.input) 
                    st.write('Number of tries: ', st.session_state.game_.num_guesses)

        with row1:
            subcol1, subcol2, subcol3 = st.columns(3)
            with subcol1:
                st.write(' **Target Color**')
                fig = display_cie_color(st.session_state.game_.target_x, st.session_state.game_.target_y)
                st.pyplot(fig, use_container_width=True)
                st.markdown(f'<small>(x, y): ({st.session_state.game_.target_x:.3f}, {st.session_state.game_.target_y:.3f})</small>', unsafe_allow_html=True)
            with subcol2:
                st.markdown(' **Best </br>Guess**', unsafe_allow_html=True)
                best_guess = st.session_state.game_.best_guess
                if best_guess is not None:
                    fig = display_cie_color(best_guess.x,best_guess.y)
                    st.pyplot(fig, use_container_width=True)
                    st.markdown(f'<small>(x, y): ({best_guess.x:.3f}, {best_guess.y:.3f})</small>', unsafe_allow_html=True)
            with subcol3:
                st.write('**Latest Guess**')
                latest_guess = st.session_state.game_.last_guess
                if latest_guess is not None:
                    
                    fig = display_cie_color(latest_guess.x, latest_guess.y)
                    st.pyplot(fig, use_container_width=True)
                    st.markdown(f'<small>(x, y): ({latest_guess.x:.3f}, {latest_guess.y:.3f})</small>', unsafe_allow_html=True)
            st.write('---')
    with col2:
        st.write('### Game Chromaticity Diagram')
        fig = plot_plane(st.session_state.plane, 
                        st.session_state.ax,
                                st.session_state.game_.best_guess,
                                st.session_state.game_.last_guess) 
        st.pyplot(fig)

    st.write('---')
run()