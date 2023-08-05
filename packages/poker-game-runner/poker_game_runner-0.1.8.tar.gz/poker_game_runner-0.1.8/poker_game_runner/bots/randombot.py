import numpy as np

from poker_game_runner.state import Observation

class Bot:
    def get_name(self):    
        return "randomBot"

    def act(self, observation: Observation):
        return np.random.choice(observation.legal_actions)