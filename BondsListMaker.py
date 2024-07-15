from Definitions.definition import PeakBounds
from typing import List

class BondsListMaker:
    def __init__(self):
        self.bounds_min: List[float] = []
        self.bonds_max: List[float] = []

    def makeList(self, peak_bounds: PeakBounds, _: str) -> None:
        self.bounds_min.extend([peak_bounds.x0_min, peak_bounds.A_min, peak_bounds.gamma_min])
        self.bonds_max.extend([peak_bounds.x0_max,  peak_bounds.A_max, peak_bounds.gamma_max,])
