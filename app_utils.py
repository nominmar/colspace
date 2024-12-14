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
        except ValueError:
            st.error('Please enter integer values for CMYK.')
    else:
        st.error('Please enter four values separated by commas for CMYK.')
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
        except ValueError:
            st.error('Please enter integer values for RGB.')
    else:
        st.error('Please enter three values separated by commas for RGB.')
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
        ax_.legend()
    return fig

def get_game_settings():
    with st.sidebar:
        st.write('### Game Settings')
        max_tolerance = st.number_input("Max Tolerance", min_value=0.001, max_value=0.1, value=0.01)
        max_tries = st.number_input("Max Number of Tries", min_value=1, max_value=20, value=10)
        difficulty = st.selectbox('Select the difficulty:', ['Easy', 'Medium'], index=1)
    return max_tolerance, max_tries, difficulty

def set_session_state(max_tries=10, max_tolerance=0.01, level='Medium'):
    if 'rgb' not in st.session_state:
        if level == 'Medium':
            st.session_state.rgb = generate_random_rgb(max_value=180)
        else:
            st.session_state.rgb = generate_random_rgb()
    if 'game_' not in st.session_state:
        st.session_state.game_ = ColorSpaces(target_color=st.session_state.rgb,
                                         max_guesses=max_tries,
                                         max_tolerance=max_tolerance)
    if '_plane' not in st.session_state:
        st.session_state.plane, st.session_state.ax = plot_cie1931((st.session_state.game_.target_x, st.session_state.game_.target_y)) 

def game_instructions():
    with st.container():
        st.markdown('---')
        st.markdown('### Color Space Game - Instructions')
        st.markdown('''
            Random color is generated and placed on CIE 1931 chromaticity diagram. (White X is the target color) \n
            You can guess the color in either RGB or CMYK color spaces. (Your guess will be displayed on the chromaticity diagram) \n
            Update the tolerance on sidebar, once you are close enough to the target color, it will stop. \n
        ''')
        st.markdown('---')