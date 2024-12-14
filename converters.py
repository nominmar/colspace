"""
Color conversion functions
"""
import matplotlib.pyplot as plt
import numpy as np

from matrices import matrix_srgb_xyz, matrix_xyz_srgb
from _util import conditional_gamma_correction, normalize_rgb, cie_xyY_to_XYZ, cie_xyz_to_xy

def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    elif len(hex_color) == 3:
        r, g, b = int(hex_color[0]*2, 16), int(hex_color[1]*2, 16), int(hex_color[2]*2, 16)
    else:
        raise ValueError("Invalid hex color format")
    return r, g, b

def hsl_to_rgb(h, s, l) -> tuple:
    s /= 100
    l /= 100

    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    elif 300 <= h < 360:
        r, g, b = c, 0, x
    else:
        r, g, b = 0, 0, 0

    r = (r + m) * 255
    g = (g + m) * 255
    b = (b + m) * 255

    return int(r), int(g), int(b)

def hsv_to_rgb(h, s, v) -> tuple:
    if s == 0:
        # If saturation is 0, the color is a shade of gray
        return (v, v, v)
    
    h = h % 360  # Ensure hue is within 0–360
    c = v * s  # Chroma
    x = c * (1 - abs((h / 60) % 2 - 1))  # Second largest component of color
    m = v - c  # Match value for brightness adjustment

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    elif 300 <= h < 360:
        r, g, b = c, 0, x

    # Add m to shift to the desired brightness
    r, g, b = r + m, g + m, b + m

    return r, g, b

def rgb_to_cie1931_xy(r, g, b) -> tuple:
    r, g, b = normalize_rgb(r, g, b)
    r = conditional_gamma_correction(r)
    g = conditional_gamma_correction(g)
    b = conditional_gamma_correction(b)
    X, Y, Z = np.dot(np.array(matrix_srgb_xyz), np.array([r, g, b]))
    return cie_xyz_to_xy(X, Y, Z)

def xyY_to_rgb(x, y, Y=1.0) -> tuple:
    if y == 0:  # Avoid division by zero
        raise ValueError("y cannot be zero.")

    X, _, Z = cie_xyY_to_XYZ(x, y, Y)
    RGB_linear = np.dot(np.array(matrix_xyz_srgb), np.array([X, Y, Z]))
    # Clip negative values to zero
    RGB_linear = np.clip(RGB_linear, 0, None)

    RGB = np.array([conditional_gamma_correction(c) for c in RGB_linear])
    # Clip values to [0, 1]
    RGB = np.clip(RGB, 0, 1)

    return tuple(RGB)

def cmyk_to_rgb(c, m, y, k) -> tuple:
    c = c / 100.0
    m = m / 100.0
    y = y / 100.0
    k = k / 100.0
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)

    return int(r), int(g), int(b)
