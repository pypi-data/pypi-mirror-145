from time import sleep
import numpy as np
from typing import List

from poker_game_runner.state import Observation

class Bot:

    def __init__(self, actions: List[int]) -> None:
        self.actions = actions

    def get_name(self):
        return "testBot"

    def act(self, obs: Observation):
        counter = sum([sum([1 for action in round if action.player == obs.my_index]) for round in obs.history])
        if len(self.actions) > counter:
            action = self.actions[counter]
            if action == "throw":
                return self.actions[10000] #out of range exception
            if action == "slow":
                sleep(10)
                return obs.get_min_raise()
            return action