# from BondsListMaker import BondsListMaker
# from DataTools import DataTools
from Definitions.definition import PeakBounds, PeakGuess
# from dataAnalyzer import ParamListMaker


from typing import Dict


class PeakSelection:
    def __init__(self, dict_peak_guess: Dict[str, PeakGuess], dict_peak_bounds: Dict[str, PeakBounds ]):
        self.dict_peak_guess = dict_peak_guess
        self.dict_peak_bounds = dict_peak_bounds

