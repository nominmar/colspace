from typing import Tuple

import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
from colour.plotting import plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931

from converters import xyY_to_rgb

def plot_cie1931(target: Tuple[float, float]) -> Tuple[plt.Figure, plt.Axes]:
    fig, ax = plot_RGB_colourspaces_in_chromaticity_diagram_CIE1931(colourspaces=['sRGB'], 
                                                                    show_spectral_locus=False, 
                                                                    show_diagram_labels=True, 
                                                                    show_centre=False)
    ax.plot(target[0], target[1], 'x', markersize=14, color='white', label='Target', mew=2, path_effects=[path_effects.withStroke(linewidth=4, foreground='black')])
    ax.legend()
    ax.set_title('')
    return (fig, ax)

def display_cie_color(x, y, Y=1.0):
    try:
        rgb = xyY_to_rgb(x, y, Y)
        title = f""
    except ValueError:
        # Return a white square in case of exception
        rgb = [1.0, 1.0, 1.0]
        title = f""

    color_square = np.ones((10, 10, 3))
    color_square[:, :, 0] *= rgb[0]
    color_square[:, :, 1] *= rgb[1]
    color_square[:, :, 2] *= rgb[2]

    plt.figure(figsize=(10, 10))  # Set the figure size to be shorter
    plt.imshow(color_square, interpolation='nearest')
    plt.axis('off')
    plt.title(title, fontsize=12)
    return plt
