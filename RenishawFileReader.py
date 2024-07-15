import numpy as np
from typing import Dict, List

from Definitions.definition import DataAndPeaks, ExperimentalData

class RenishawFileReader:
    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.data_map:  ExperimentalData  = ExperimentalData({})
        
    def add_data(self, key: str, coordinates: List[float]) -> None:
        if (self.data_map.data_and_peaks.get(key) is None):
            data_and_peak = DataAndPeaks([], None)
            self.data_map.data_and_peaks[key] = data_and_peak
        self.data_map.data_and_peaks[key].data.append(coordinates)


    def get_data(self) ->  ExperimentalData:
        with open(self.file_path, "r") as file:
            for line in file:   
                fields = line.strip().split("\t")
                label = fields[0] + "_" + fields[1]
                self.add_data(label, [float(fields[2]), float(fields[3])])
        
        return self.data_map

          
    
         
     
