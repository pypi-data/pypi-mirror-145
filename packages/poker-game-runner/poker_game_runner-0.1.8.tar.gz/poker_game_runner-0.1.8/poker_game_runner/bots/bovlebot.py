
from poker_game_runner.state import Observation
from poker_game_runner.utils import Range, HandType

class Bot:
  def get_name(self):
      return "mybot"
  
  def act(self, obs: Observation):
    if obs.current_round == 0: #preflop
      return self.do_preflop(obs)
    else:
      return self.do_postflop(obs)
      
  def do_preflop(self, obs: Observation):
    my_stack_in_blinds = obs.player_infos[obs.my_index].stack / obs.big_blind
    if my_stack_in_blinds < 20:
      return self.do_preflop_panic(obs, my_stack_in_blinds)

    raise_actions = [action for action in obs.get_actions_this_round() if action.action > 1]
    if len(raise_actions) == 0: # Open
      return self.do_preflop_open(obs)

    if len(raise_actions) > 0:
      return self.do_preflop_into_raise(obs)

  def do_postflop(self, obs:Observation):
    if self.is_checked_to_me(obs):
      return obs.get_min_raise() #attempt to steal the pot
    
    my_hand_type = obs.get_my_hand_type()
    if my_hand_type > HandType.PAIR and my_hand_type > obs.get_board_hand_type():
      return obs.get_max_raise()
    elif my_hand_type == HandType.PAIR and my_hand_type > obs.get_board_hand_type():
      return obs.get_min_raise()
    else:
      return 0

  def is_checked_to_me(self, obs:Observation):
    call_actions = [action for action in obs.get_actions_this_round() if action.action == 0]
    return len(call_actions) == len(obs.get_active_players())-1 and obs.get_call_size() == 0
  
  def do_preflop_panic(self, obs:Observation, my_stack_in_blinds):
    if my_stack_in_blinds < 10:
      r = Range("44+, A2s+, K4s+, Q6s+, J7s+, T8s+, 98s, A7o+, K9o+, QTo+, JTo") # 25%
    elif my_stack_in_blinds < 15:
      r = Range("66+, A5s+, K9s+, Q9s+, JTs, ATo+, KJo+, QJo") # 16%
    else:
      r = Range("77+, A9s+, KTs+, QJs, AJo+, KQo") # 10%
    
    if r.is_hand_in_range(obs.my_hand):
      return obs.get_max_raise() # all in
    else:
      return 0

  def do_preflop_open(self, obs:Observation):
    open_raise_range = Range("55+, A3s+, K7s+, Q8s+, J9s+, T9s, A9o+, KTo+, QJo") # top 20%
    if open_raise_range.is_hand_in_range(obs.my_hand):
      return obs.get_fraction_pot_raise(1) # raise pot
    else:
      return 0

  def do_preflop_into_raise(self, obs:Observation):
    call_fraction = obs.get_pot_size() / obs.get_call_size()
    if call_fraction < 0.1:
      return 1 #call
    
    if call_fraction < 0.3:
      r = Range("66+, A5s+, K9s+, Q9s+, JTs, ATo+, KJo+, QJo") # 16%
    elif call_fraction < 0.6:
      r = Range("77+, A9s+, KTs+, QJs, AJo+, KQo") # 10%
    else:
      r = Range("88+, ATs+, KJs+, AKo") # 6%

    if r.is_hand_in_range(obs.my_hand):
      return 1
    else:
      return 0