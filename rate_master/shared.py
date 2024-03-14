from typing import Optional
class ConstraintDto:
        attribute:str
        op :str
        value:int



class ScalePiece:
        one_piece_cost: str
        two_piece_cost: str
        three_piece_cost: str
        four_piece_cost: str
        additional_piece_cost: str

class ScaleSkid:
        two_skid_cost: str
        four_skid_cost: str
        six_skid_cost: str

class CostDto:
        method: str # Values: "FIXED" or "SCALE"
        attribute: Optional[str] # Values: "SKIDS" or "PIECES"
        scale_piece: Optional[ScalePiece]
        scale_skid: Optional[ScaleSkid]
        fixed_cost: Optional[str]









