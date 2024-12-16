"""
Creates a random color, takes input in various color spaces, and scores guesses based on distance in CIE1931 space
"""
from dataclasses import dataclass

from _util import generate_random_rgb, setup_logger
from converters import hex_to_rgb, hsl_to_rgb, cmyk_to_rgb, rgb_to_cie1931_xy

logger = setup_logger('colorspaces')

@dataclass
class GuessType:
    name: str
    converter: callable

@dataclass
class Guess:
    input: tuple
    guess_type: str
    x: float
    y: float
    score: float
    is_best: bool
    number: int


guess_types = {
    'HEX': GuessType('HEX', hex_to_rgb),
    'HSL': GuessType('HSL', hsl_to_rgb),
    'CMYK': GuessType('CMYK', cmyk_to_rgb)
}

level_map = {
    'Easy': 255,
    'Medium': 100,
    'Hard': 100
}


class ColorSpaces:
    def __init__(self, 
                target_color: tuple = None, 
                 max_guesses: int = 10,
                 max_tolerance: float = 0.01,
                 level: str = 'Medium'):
        """
        Initialize the ColorSpaces game
        """
        if target_color:
            self.target_x, self.target_y = rgb_to_cie1931_xy(*target_color)
        else:
            self.target_x, self.target_y = rgb_to_cie1931_xy(*generate_random_rgb(max_value=level_map[level]))
        logger.info(f"New game started with target color at ({self.target_x:.3f}, {self.target_y:.3f})")
        self.guesses = []
        self.best_guess = None
        self.num_guesses = 0
        self.max_guesses = max_guesses
        self.max_tolerance = max_tolerance
        self.game_over = False
        self.last_guess = None
        self.level = level

    

    def calculate_distance(self, guess_x: float, guess_y: float) -> float:
        """
        Calculate Euclidean distance between target color and guess in CIE1931 space
        Returns distance normalized between 0 and 1
        """
        distance = ((self.target_x - guess_x) ** 2 + (self.target_y - guess_y) ** 2) ** 0.5
        # Normalize distance to 0-1 range (max possible distance in CIE space is ~0.8)
        normalized_distance = min(distance / 0.8, 1.0)
        return normalized_distance
    
    def normalize_to_xy(self, guess: tuple, 
                  guess_type: str):
        """
        Normalize guess to CIE1931 xy coordinates
        """
        if guess_type == 'RGB':
            x_, y_ = rgb_to_cie1931_xy(*guess)
        elif guess_type == 'HEX':
            rgb_guess = guess_types[guess_type].converter(guess)
            x_, y_ = rgb_to_cie1931_xy(*rgb_guess)
        else:
            rgb_guess = guess_types[guess_type].converter(*guess)
            x_, y_ = rgb_to_cie1931_xy(*rgb_guess)
        return x_, y_

    def _score_guesses(self, distance_to_target: float):
        """
        Score guesses based on distance to target
        """
        is_best = True
        if len(self.guesses) > 0:
            for prev_guess in self.guesses:
                if prev_guess.score <= distance_to_target:
                    is_best = False
                    break        
        if is_best:
            for prev_guess in self.guesses:
                prev_guess.is_best = False
        return is_best

    def add_guess(self, guess: tuple, guess_type: str):
        """
        Add a guess to the game
        """

        if self.num_guesses >= self.max_guesses:
            logger.info("Game over. Maximum number of guesses reached.")
            self.game_over = True
            return
        self.num_guesses += 1
        x_, y_ = self.normalize_to_xy(guess, guess_type)
        distance_to_target = self.calculate_distance(x_, y_)
        current_guess = Guess(
                x=x_,
                y=y_,
                input=guess,
                guess_type=guess_type,
                score=distance_to_target,
                is_best=True,
                number=self.num_guesses)
        self.last_guess = current_guess
        if distance_to_target < self.max_tolerance:
            self.best_guess = current_guess
            current_guess
            self.game_over = True
            self.last_guess = self.best_guess
            logger.info("Game over. Best guess found.")
            return
        is_best = self._score_guesses(distance_to_target) 
        if is_best:
            self.best_guess = current_guess
        self.guesses.append(current_guess)
        logger.info(f"Guess #{self.num_guesses}: ({x_:.3f}, {y_:.3f}), Score: {distance_to_target:.3f}")

if __name__ == '__main__':
    game = ColorSpaces()
    game.add_guess((255, 0, 0), 'RGB')
    game.add_guess((0, 255, 0), 'RGB')
    game.add_guess((0, 0, 255), 'RGB')