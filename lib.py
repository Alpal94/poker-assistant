from enum import Enum

class Action(Enum):
    RFI = "RFI"
    FacingRFI = "FacingRFI"
    RFIVs3Bet = "RFIVs3Bet"

class Position(Enum):
    UTG = "UTG"
    UTG1  = "UTG1"
    UTG2  = "UTG2"
    Lojack  = "Lojack"
    Hijack  = "Hijack"
    Cutoff  = "Cutoff"
    Button  = "Button"
    SmallBlind  = "SmallBlind"
    BigBlind = "BigBlind"
