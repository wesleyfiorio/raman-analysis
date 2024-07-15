from typing import List
import numpy as np
import matplotlib.pyplot as plt
from DataTools import DataTools
from dataAnalyser.DataFitter import DataFitter
from Definitions.definition import DataAndPeaks, ExperimentalData, ParameterPeak
from tools import Tools

class MapManager:
    def __init__(self, peak_name: str, parameter: ParameterPeak):
        self.peak_name = peak_name
        self.parameter = parameter
        self.x_y_z_array: List[List[float]] = []

    def add_data_map(self, data_and_peaks: DataAndPeaks, key: str):
        peaks = data_and_peaks.peaks
        if peaks is None:
            return     
        if  not self.peak_name in peaks:
            return 
        peak = peaks[self.peak_name]
        z = peak.get_param(self.parameter)
        if z is None:
            return
        
        x_y: List[str] = key.split("_")
        try: 
            x: float = float(x_y[0])
            y: float = float(x_y[1])
        except ValueError:
            print(f"Error: Invelid data format in {key}")
     
        self.x_y_z_array.append([x, y, z]) 
        plt.scatter(x, y, c=z, cmap= "inferno", alpha = 0.8)
        # mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(f'x: {sel.target[0]}, y: {sel.target[1]}, z: {z[sel.index]}'))
    
    def save_to_gwyddion(self, filename: str):
        with open(filename, "w") as file:
            file.write(f"# { self.peak_name} {self.parameter.value}\n")
            for row in self.x_y_z_array:
                file.write(" ".join(f"{val:.6f}" if not np.isnan(val) else "NaN" for val in row) + "\n")
                
    def show(self):
        x_y_z = np.array(self.x_y_z_array)
        plt.scatter(x_y_z[:, 0], x_y_z[:, 1], c=x_y_z[:, 2], cmap="inferno", alpha=1, marker= "s")
        plt.colorbar(label=self.peak_name + "  " + self.parameter.value)
        plt.clim(min(x_y_z[:, 2]), max(x_y_z[:, 2]))
        plt.show()
        plt.close()
