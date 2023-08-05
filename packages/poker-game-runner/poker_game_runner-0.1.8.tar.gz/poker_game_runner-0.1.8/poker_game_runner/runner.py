import multiprocessing
from time import time
import numpy as np
import pyspiel
from poker_game_runner.state import InfoState, card_num_to_str
from typing import List, Tuple
from collections import namedtuple

BlindScheduleElement = namedtuple('BlindScheduleElement', 'next_blind_change small_blind big_blind ante')
Player = namedtuple('Player', 'bot_impl stack id')

def play_tournament_table(bots, start_stack: int, blind_schedule: Tuple[BlindScheduleElement], use_timeout=True):
    json_data = []
    active_players = [Player(bot,start_stack, idx) for idx, bot in enumerate(bots)]
    defeated_players = []
    hand_count = 0
    blinds_iter = iter(blind_schedule)

    current_blinds = next(blinds_iter)
    while len(active_players) > 1:
        print(hand_count)

        json_hand = {
            "hand_count": hand_count,
            "active_players": [player_to_dict(player) for player in active_players],
            "defeated_players": defeated_players
        }

        rewards, json_hand_events = play_hand(active_players, get_blinds_input(current_blinds, len(active_players)), use_timeout)
        json_hand["hand_events"] = json_hand_events

        if hand_count == current_blinds.next_blind_change:
            current_blinds = next(blinds_iter)

        newly_defeated_players, active_players = update_active_players(active_players, rewards, current_blinds.big_blind)

        defeated_players = defeated_players + newly_defeated_players
        active_players = active_players[1:] + [active_players[0]]
        hand_count += 1
        json_data.append(json_hand)
    
    results = defeated_players + [player_to_dict(active_players[0])]
    results.reverse()
    return results, json_data

def player_to_dict(player: Player, defeated = False):
    return {"name": player.bot_impl.get_name(), "id": player.id, "stack": player.stack if not defeated else 0}

def update_active_players(active_players: List[Player], rewards: List[int], big_blind: int):    
    updated_players = [Player(player.bot_impl, int(player.stack+r), player.id) for player,r in zip(active_players, rewards)]

    defeated_players = [player_to_dict(player, True) for player in updated_players if player.stack < big_blind]
    active_players = [player for player in updated_players if player.stack >= big_blind]
    return defeated_players, active_players

def get_blinds_input(current_blinds: BlindScheduleElement, playerCount: int) -> List[int]:
    return [current_blinds.small_blind, current_blinds.big_blind] + ([current_blinds.ante] * (playerCount-2))



def play_hand(players: List[Player], blinds: List[int], use_timeut = True):
    state, info_state, json_events = init_game(players, blinds)

    while not state.is_terminal():
        if state.is_chance_node():
            card_num = np.random.choice(state.legal_actions())
            apply_chance_action(state, info_state, json_events, card_num)
            continue
        
        current_idx = state.current_player()
        action = get_player_action(players[current_idx], state, info_state, current_idx, use_timeut)
        apply_player_action(state, info_state, json_events, current_idx, action)
    
    json_events = json_events + [{"type": "reward", "player": i, "reward": reward} for i, reward in enumerate(state.rewards())]

    return list(map(int, state.rewards())), json_events

def get_player_action(player, state, info_state, current_idx, use_timeout):
    observation = info_state.to_observation(current_idx, state.legal_actions())
    try:
        action = get_player_action_with_timeout(player, observation, 2 if use_timeout else 1000000)
    except BaseException as e:
        print(f"Bot: '{player.bot_impl.get_name()}' caused an exception!!! Folding on their behalf.")
        print(e)
        action = 0
    if not action in state.legal_actions():
        print(f"Bot: '{player.bot_impl.get_name()}' took action '{action}' which is illigal")
        if 0 in state.legal_actions():
            action = 0
        else:
            action = 1
    return action

def get_player_action_with_timeout(player, obs, timeout):
    start = time()
    res = player.bot_impl.act(obs)
    end = time()
    delta = end - start
    if delta > timeout:
        print(f"Bot: '{player.bot_impl.get_name()}' took too long to return. Folding on their behalf.")
        return 0
    return res
    pipeRecv, pipeSend = multiprocessing.Pipe(False)
    p = multiprocessing.Process(target=run_act_on_bot, args=(player.bot_impl, obs, pipeSend) )
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.kill()
    if not pipeRecv.poll():
        pipeRecv.close()
        print(f"Bot: '{player.bot_impl.get_name()}' took too long to return. Folding on their behalf.")
        return 0
    return pipeRecv.recv()

def run_act_on_bot(bot, obs, pipe):
    pipe.send(bot.act(obs))


def apply_player_action(state, info_state, json_events, current_idx, action):
    state.apply_action(action)
    info_state.update_info_state_action(current_idx, action)
    json_events.append({"type": "action", "player": current_idx, "action": int(action)})

def apply_chance_action(state, info_state, json_events, card_num):
    state.apply_action(card_num)
    info_state.update_info_state_draw(card_num)
    json_events.append({"type": "deal", "player": -1, "action": card_num_to_str(card_num)})



def init_game(players, blinds):
    game = pyspiel.load_game("universal_poker", {
        "betting": "nolimit",
        "bettingAbstraction": "fullgame",
        "numPlayers": len(players),
        "stack": " ".join(str(player.stack) for player in players),
        "blind": " ".join(str(blind) for blind in blinds),
        "numRounds": 4,
        "numHoleCards": 2,
        "numBoardCards": "0 3 1 1",
        "numSuits": 4,
        "numRanks": 13,
        "firstPlayer": "3 1 1 1" if len(players) > 2 else "1 1 1 1"
    })

    state = game.new_initial_state()

    #deal private cards
    while state.is_chance_node():
        state.apply_action(np.random.choice(state.legal_actions()))
        continue

    info_state = InfoState(state.history(), [p.stack for p in players], [b for b in blinds])
    json_events = []
    json_events.append({"type": "action", "player": 0, "action": blinds[0]})
    json_events.append({"type": "action", "player": 1, "action": blinds[1]})
    json_events = json_events + [{"type": "deal", "player": int(i/2), "card": card} for i, card in enumerate(map(card_num_to_str, state.history()))]
    return state, info_state, json_events
