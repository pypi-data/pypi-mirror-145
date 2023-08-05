from dataclasses import dataclass
from typing import List, Tuple
from poker_game_runner.utils import HandType, card_num_to_str, get_hand_type, hand_str_to_enum

@dataclass(frozen=True)
class PlayerInfo: 
    spent: int
    stack: int
    active: bool

@dataclass(frozen=True)
class ActionInfo: 
    player: int
    action: int
    def __str__(self) -> str:
        player_str = "Player " + str(self.player) + ": "
        if self.action == 0:
            return player_str + "Fold"
        if self.action == 1:
            return player_str + "Call"
        return player_str + "Raise to " + str(self.action)

@dataclass(frozen=True)
class Observation: 
    my_hand: Tuple[str]
    my_index: int
    board_cards: Tuple[str]
    player_infos: Tuple[PlayerInfo]
    history: Tuple[Tuple[ActionInfo]]
    small_blind: int
    big_blind: int
    current_round: int
    legal_actions: Tuple[int]

    def get_my_hand_type(self):
        cards = self.my_hand + self.board_cards
        return get_hand_type(cards)
    
    def get_board_hand_type(self):
        if len(self.board_cards) == 0:
            return HandType.HIGHCARD
        return get_hand_type(self.board_cards)

    def get_player_count(self):
        return len(self.player_infos)

    def get_active_players(self):
        return tuple(p for p in self.player_infos if p.active)
    
    def get_actions_this_round(self):
        return self.get_actions_in_round(self.current_round)

    def get_actions_in_round(self, round_num: int):
        if round_num > 3 or round_num < 0:
            return tuple()
        return self.history[round_num]

    def get_max_spent(self):
        return max(map(lambda p: p.spent, self.player_infos))

    def get_call_size(self):
        return self.get_max_spent() - self.player_infos[self.my_index].spent

    def get_pot_size(self):
        return sum(map(lambda p: p.spent, self.player_infos))
    
    def can_raise(self):
        return any(a for a in self.legal_actions if a > 1)
    
    def get_min_raise(self):
        return min(a for a in self.legal_actions if a > 1) if self.can_raise() else 1

    def get_max_raise(self):
        return max(a for a in self.legal_actions if a > 1) if self.can_raise() else 1

    def get_fraction_pot_raise(self, frac):
        if not self.can_raise():
            return 1
        else:
            pot = self.get_pot_size()
            call = self.get_call_size()
            pot_with_my_call = pot + call
            raise_amount = call + int(pot_with_my_call * frac)
            if raise_amount < self.get_min_raise():
                return self.get_min_raise()
            elif raise_amount > self.get_max_raise():
                return self.get_max_raise()
            else:
                return raise_amount


    def action_to_str(self, action_num: int, player_idx: int = None):
        if player_idx is None:
            player_idx = self.my_index
        if type(action_num) is not int or type(player_idx) is not int:
            return "unexpected types"
        return str(ActionInfo(player_idx, action_num))

class InfoState: 
    player_hands: Tuple[Tuple[str]]
    board_cards: List[str]
    player_infos: List[PlayerInfo]
    history: Tuple[List[ActionInfo]]
    small_blind: int
    big_blind: int
    current_round: int

    def __init__(self, history: List[int], stacks: List[int], blinds: List[int]):
        self.player_hands = tuple(
            tuple(
                map(card_num_to_str,
                    sorted(history[i:i+2], reverse=True)
                )
            )
            for i in range(0,len(history),2)
        )
        self.player_infos = [PlayerInfo(blind, stack-blind, True) for blind, stack in zip(blinds, stacks)]
        self.board_cards = []
        self.history = ([],[],[],[])
        self.small_blind = blinds[0]
        self.big_blind = blinds[1]
        self.current_round = 0

    def update_info_state_action(self, player_idx: int, action: int):
        player_info = self.player_infos[player_idx]
        if action > 1:
            r = action - player_info.spent
            self.player_infos[player_idx] = PlayerInfo(action, player_info.stack - r, player_info.active)
        elif action == 1:
            max_spent = max(map(lambda p: p.spent, self.player_infos))
            c = max_spent - player_info.spent
            self.player_infos[player_idx] = PlayerInfo(max_spent, player_info.stack - c, player_info.active)
        else:
            self.player_infos[player_idx] = PlayerInfo(player_info.spent, player_info.stack, False)
        self.history[self.current_round].append(ActionInfo(player_idx, action))


    def update_info_state_draw(self, card_num = int):
        cards_str = card_num_to_str(card_num)
        self.board_cards.append(cards_str)
        self.current_round = 0 if len(self.board_cards) < 3 else len(self.board_cards)-2
            
    def to_observation(self, player_idx: int, legal_actions: List[int]):
        return Observation(self.player_hands[player_idx], 
                        player_idx, 
                        tuple(self.board_cards), 
                        tuple(self.player_infos), 
                        tuple(tuple(h) for h in self.history),
                        self.small_blind,
                        self.big_blind,
                        self.current_round,
                        tuple(legal_actions))

