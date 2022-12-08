from enum import Enum

class Action(Enum):
    RFI = 1
    FacingRFI = 2
    RFIVs3Bet = 3

class Position(Enum):
    UTG = 3
    UTG1  = 4
    UTG2  = 5
    Lojack  = 6
    Hijack  = 7
    Cutoff  = 8
    Button  = 9
    SmallBlind  = 1
    BigBlind = 2

