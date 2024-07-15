
from typing import List
import numpy as np
from Definitions.definition import DataAndPeaks, PeakGuess
from tools import Tools


class ParamListMaker:
    def __init__(self):
        self.params = [] 
        
    def makeList(self, peak_guess: PeakGuess, _:str):
        self.params.extend([peak_guess.x0, peak_guess.A, peak_guess.gamma])
    
class DataTruncator:
    def __init__(self, x_min: float, x_max: float):
        self.x_min = x_min
        self.x_max = x_max
        self.tools = Tools()
        
    def truncate(self, data_and_peaks: DataAndPeaks, _: str):
        data_and_peaks.data = self.tools.truncate(np.array(data_and_peaks.data), self.x_min, self.x_max).tolist()
      
class BaselineCorrector:
    def __init__(self, anchor_points: List[float]):
        self.x_intersection = anchor_points
        self.tools = Tools()
              
    def remove_baseline(self, data_and_peaks: DataAndPeaks, _: str):
        data_and_peaks.data = self.tools.baseline(np.array(data_and_peaks.data), self.x_intersection).tolist()