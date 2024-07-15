from enum import Enum
from typing import Dict, List, NamedTuple, Tuple, Union

from typing import List, Dict

import numpy as np


class ParameterPeak(Enum):
    x0 ="x0"
    A = "A"
    gamma = "gamma"
    x0Error = "x0Error"
    AError = "AError"
    gammaError = "gammaError"


class PeakGuess:
    def __init__(
            self,
            x0: float,
            A: float,
            gamma: float,
            ):
        
        self.x0 = x0
        self.A = A
        self.gamma = gamma
        
    def get_list_param(self):
        return [self.x0, self.A, self.gamma]
    
   
        
class Peak:
    def __init__(
            self,
            x0: float,
            A: float,
            gamma: float,
            
            x0Error: float,
            AError: float,
            gammaError: float
            ):
        
        self.x0 = x0
        self.A = A
        self.gamma = gamma
        self.x0Error = x0Error
        self.AError = AError
        self.gammaError = gammaError
        
    def get_param(self, param: ParameterPeak) -> Union[float, None]:
        if hasattr(self, param.value):
            return getattr(self, param.value)
        return None

class DataAndPeaks:
    def __init__(self, data: List[List[float]], dic_peaks:   Union[Dict[str, Peak], None]): 
        self.data = data
        self.peaks = dic_peaks

class ExperimentalData:
    def __init__(self, dic_data_and_peaks: Dict[str, DataAndPeaks]):
        self.data_and_peaks = dic_data_and_peaks

class PeakBounds:
    def __init__(
            self, 
            x0_min: float = -np.inf,
            A_min: float= 0,
            gamma_min: float = 0,
            x0_max: float= np.inf,
            A_max: float = np.inf,
            gamma_max: float = np.inf
            ):

        self.x0_min = x0_min
        self.A_min = A_min
        self.gamma_min = gamma_min
        self.x0_max = x0_max
        self.A_max = A_max
        self.gamma_max = gamma_max

        
        
        

