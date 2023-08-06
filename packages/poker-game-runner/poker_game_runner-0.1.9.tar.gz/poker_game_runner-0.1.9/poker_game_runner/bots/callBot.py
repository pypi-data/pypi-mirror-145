import numpy as np

from poker_game_runner.state import Observation

class Bot:
    def get_name(self):
        return "callBot"

    def act(self, observation: Observation):
        return 1