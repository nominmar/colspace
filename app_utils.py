import random
import streamlit as st
import matplotlib.patheffects as path_effects

from game import ColorSpaces
from display import plot_cie1931
from _util import generate_random_rgb

def process_cmyk_input():
    guess = st.text_input('Enter your guess (e.g., 0,100,100,0 for CMYK):', value='0,0,0,1')
    cmyk_values = guess.split(',')
    if len(cmyk_values) == 4:
        try:
            c, m, y, k = map(int, cmyk_values)
            if all(0 <= value <= 100 for value in (c, m, y, k)):
                guess = (c, m, y, k)
            else:
                st.error('Each CMYK value must be between 0 and 100.')
                st.stop()
        except ValueError:
            st.error('Please enter integer values for CMYK.')
            st.stop()
    else:
        st.error('Please enter four values separated by commas for CMYK.')
        st.stop()
    return guess

def process_rgb_input():
    guess = st.text_input('Enter your guess (e.g., 255,0,0 for RGB):', value='1,1,1')
    rgb_values = guess.split(',')
    if len(rgb_values) == 3:
        try:
            r, g, b = map(int, rgb_values)
            if all(0 <= value <= 255 for value in (r, g, b)):
                guess = (r, g, b)
            else:
                st.error('Each RGB value must be between 0 and 255.')
                st.stop()
        except ValueError:
            st.error('Please enter integer values for RGB.')
            st.stop()
    else:
        st.error('Please enter three values separated by commas for RGB.')
        st.stop()
    return guess

def get_user_input():
    guess_type = st.selectbox('Select the color space of your guess:', ['RGB', 'CMYK'], index=0)
    if guess_type == 'CMYK':
        guess = process_cmyk_input()
    else:
        guess = process_rgb_input()
    return guess, guess_type

def plot_plane(fig, ax_, best_guess, last_guess):
    if best_guess:
        ax_.plot(best_guess.x, best_guess.y, 'x', markersize=8, color='red', label=f'Best Guess', mew=2, path_effects=[path_effects.withStroke(linewidth=4, foreground='black')])
    if last_guess:
        ax_.plot(last_guess.x, last_guess.y, '+', markersize=8, color='black', label=f'Latest guess', mew=2, path_effects=[path_effects.withStroke(linewidth=4, foreground='black')])
        ax_.axhline(y=last_guess.y, color='black', linestyle='-.', linewidth=0.5)
        ax_.axvline(x=last_guess.x, color='black', linestyle='-.', linewidth=0.5)
        ax_.legend()
    return fig

def get_game_settings():
    with st.sidebar:
        st.write('### Game Settings')
        max_tolerance = st.number_input("Max Error Tolerance", min_value=0.01, max_value=0.1, value=0.01)
        st.markdown('<small>You win if Euclidian distance to target is less than this</small>', unsafe_allow_html=True)
        max_tries = st.number_input("Max Number of Tries", min_value=1, max_value=100, value=20)
        difficulty = st.selectbox('Select the difficulty:', ['Easy', 'Medium', 'Hard'], index=1)
        st.markdown('<small>Medium and hard will ensure target color is not at the edges of sRGB space </small>', unsafe_allow_html=True)
    return max_tolerance, max_tries, difficulty

def set_session_state(max_tries=10, max_tolerance=0.01, level='Medium'):
    if 'rgb' not in st.session_state:
        if level == 'Medium':
            st.session_state.rgb = generate_random_rgb(max_value=170)
        elif level == 'Hard':
            st.session_state.rgb = generate_random_rgb(max_value=100)
        else:
            st.session_state.rgb = generate_random_rgb()
    if ('game_' not in st.session_state): 
        st.session_state.game_ = ColorSpaces(
                                         max_guesses=max_tries,
                                         max_tolerance=max_tolerance, 
                                         level=level)
    elif  (max_tolerance != st.session_state.game_.max_tolerance) | (max_tries != st.session_state.game_.max_guesses) | (st.session_state.game_.level != level):
        st.session_state.game_ = ColorSpaces(
                                         max_guesses=max_tries,
                                         max_tolerance=max_tolerance,
                                         level=level)
    if '_plane' not in st.session_state:
        st.session_state.plane, st.session_state.ax = plot_cie1931((st.session_state.game_.target_x, st.session_state.game_.target_y)) 

def game_faq():
    with st.expander('Game movement FAQ', expanded=False):
        with open("./data/faq.html", "r") as file:
            faq_html = file.read()
            st.components.v1.html(faq_html, height=500)

def game_instructions():
    with st.container():
        st.markdown('---')
        st.markdown('<h3>Color Space Game - Instructions 🎮🎨</h3>', unsafe_allow_html=True)
        with open("./data/intro.html", "r") as file:
            instructions = file.read()
            st.components.v1.html(instructions, height=100)
        game_faq()
        st.markdown('---')