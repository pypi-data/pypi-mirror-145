from enum import IntEnum
from typing import List, Tuple
import eval7

RANKS = '23456789TJQKA'
SUITS = 'cdhs'

class HandType(IntEnum):
    STRAIGHTFLUSH = 9
    FOUROFAKIND = 8
    FULLHOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREEOFAKIND = 4
    TWOPAIR = 3
    PAIR = 2
    HIGHCARD = 1
    ERROR = 0

""" class Range:
    def __init__(self, rangeStr) -> None:
        self.range = eval7.HandRange(rangeStr)

    def is_hand_in_range(self, handCards: Tuple[str]) -> bool:
        evalHand = tuple(map(eval7.Card, sorted(handCards, key=lambda x: RANKS.index(x[0]), reverse=True)))
        rangeHands = [hand[0] for hand in self.range.hands]
        return evalHand in rangeHands """

class Range:

    def __init__(self, rangeStr: str) -> None:
        self.rangeList = rangeStr.split(", ")
        self.expandedRangeList = []
        for rangeElem in self.rangeList:
            if rangeElem[0] == rangeElem[1] and rangeElem[0] in RANKS: #pair
                if len(rangeElem) == 2: # single combo
                    self.expandedRangeList.append(rangeElem)
                else:
                    startIndex = RANKS.index(rangeElem[0])
                    if len(rangeElem) == 3 and rangeElem[2] == '+': # X and above combo
                        endIndex = 12
                    elif len(rangeElem) == 5 and rangeElem[2] == '-' and rangeElem[3] == rangeElem[4]: # X_low to X_high combo
                        endIndex = RANKS.index(rangeElem[3])
                    else:
                        raise ValueError
                    includedRanks = RANKS[startIndex:endIndex+1]
                    self.expandedRangeList += [rank + rank for rank in includedRanks]
            elif rangeElem[0] in RANKS and rangeElem[1] in RANKS and rangeElem[2] in "os": #non pair
                if len(rangeElem) == 3: #single combo
                    self.expandedRangeList.append(rangeElem)
                else:
                    highCardIndex = RANKS.index(rangeElem[0])
                    startIndex = RANKS.index(rangeElem[1])
                    if len(rangeElem) == 4 and rangeElem[3] == '+':
                        endIndex = highCardIndex - 1
                    elif len(rangeElem) == 7 and rangeElem[3] == '-' and rangeElem[0] == rangeElem[4] and rangeElem[5] in RANKS and rangeElem[6] == rangeElem[2]:
                        endIndex = RANKS.index(rangeElem[5])
                    else:
                        raise ValueError
                    includedRanks = RANKS[startIndex:endIndex+1]
                    self.expandedRangeList += [rangeElem[0] + rank + rangeElem[2] for rank in includedRanks]
            else:
                raise ValueError

    def is_hand_in_range(self, handCards: Tuple[str]):
        for card in handCards:
            if not self.__validateCard(card):
                raise ValueError

        handCardsLst = list(handCards)
        handCardsLst.sort(key=lambda x: RANKS.index(x[0]), reverse=True)
        highCard = handCardsLst[0]
        lowCard = handCardsLst[1]
        handStr = highCard[0] + lowCard[0]

        if highCard[0] != lowCard[0]: #not pair
            if highCard[1] == lowCard[1]: #suited
                handStr += 's'
            else:
                handStr += 'o'

        return handStr in self.expandedRangeList

    def __validateCard(self, cardStr):
        if not len(cardStr) == 2 or cardStr[0] not in RANKS or cardStr[1] not in SUITS:
            return False
        else:
            return True

def get_hand_type(cards: List[str]):
    evalCards = list(map(eval7.Card, cards))
    handTypeStr = eval7.handtype(eval7.evaluate(evalCards))
    return hand_str_to_enum(handTypeStr)

def card_num_to_str(card_num: int):
    rank_num = int(card_num / 4)
    suit_num = card_num % 4
    return RANKS[rank_num] + SUITS[suit_num]

def hand_str_to_enum(hand_str: str):
    hand_str_lower = hand_str.lower()
    if hand_str_lower == "high card":
        return HandType(1)
    elif hand_str_lower == "pair":
        return HandType(2)
    elif hand_str_lower == "two pair":
        return HandType(3)
    elif hand_str_lower == "trips":
        return HandType(4)
    elif hand_str_lower == "straight":
        return HandType(5)
    elif hand_str_lower == "flush":
        return HandType(6)
    elif hand_str_lower == "full house":
        return HandType(7)
    elif hand_str_lower == "quads":
        return HandType(8)
    elif hand_str_lower == "straight flush":
        return HandType(9)
    return HandType(0)