import random
import logging

def conditional_gamma_correction(channel):
    if channel > 0.04045:
        return ((channel + 0.055) / (1.055)) ** 2.4
    else:
        return channel / 12.92

def normalize_rgb(r, g, b):
    return r / 255.0, g / 255.0, b / 255.0

def cie_xyz_to_xy(x_cie, y_cie, z_cie):
    if (x_cie+y_cie+z_cie) == 0:
        x = 0
        y = 0
    else:
        x = x_cie / (x_cie + y_cie + z_cie)
        y = y_cie / (x_cie + y_cie + z_cie)
    return x, y

def cie_xyY_to_XYZ(x, y, Y):
    X = (x * Y) / y
    Z = (1 - x - y) * Y / y
    return X, Y, Z

def generate_random_rgb():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

def generate_random_rgb():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)