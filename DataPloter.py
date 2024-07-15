import os
from Definitions.definition import DataAndPeaks, Peak, PeakGuess
from tools import Tools
import matplotlib.pyplot as plt
import numpy as np

from typing import List, Tuple


class DataPloter:
    def __init__(self, directory: str):
        self.directory = directory

    def plot_and_save(self, data_and_peaks: DataAndPeaks, key: str):
        data: np.ndarray = np.array(data_and_peaks.data)
        dict_peaks = data_and_peaks.peaks
        x = data[:,0]
        self.__create_data_scatter__(x, data[:,1], key)
      
        y_total = np.zeros_like(x) 
        if dict_peaks is not None:
            for peak_name, peak in dict_peaks.items():
                peak = dict_peaks[peak_name]
                (x,y) = self.__generate_lorentzian_response_(x, peak)
                y_total+=y
                self.__plot__(x, y, peak_name)
        else:
            print('Data without peaks')
        
        self.__plot__(x, y_total, "Total fits.")
        plt.legend()
        filename = os.path.join(self.directory, key + ".png")
        plt.savefig(filename, dpi = 300, bbox_inches='tight' )
        plt.close()
        
    def __plot__(self, x: np.ndarray, y: np.ndarray, key: str):
        if len(x) == len(y):
            plt.plot(x, y,  label=key)
        else:
            print(f"Error with {key}: {len(x)} is different of {len(y)} ")
            
            
    def __create_data_scatter__(self, x: np.ndarray, y: np.ndarray, key: str):
        
        plt.scatter(x, y, c="blue", marker="o", edgecolors="black", alpha=0.7, label=key)  # Add label

        plt.xlabel("Raman shift (cm-1)", fontsize=12)
        plt.ylabel("Absolut Intensity", fontsize=12)
        plt.title(f"Data {key} fited.", fontsize=14)

        plt.grid(True, linestyle="--", linewidth=0.5, color="gray")
        # plt.xlim(0, 6)  # Set x-axis limits (optional)
        # plt.ylim(0, 10)  # Set y-axis limits (optional)

        plt.legend()

        plt.tight_layout()
        
    def __generate_lorentzian_response_(self, x: np.ndarray, peak: Peak):
        y = self.__lorentzian__(x, peak)
        return (x, y)
               
    def __lorentzian__(self,x: np.array, peak: Peak):
        return peak.A * peak.gamma**2/ (peak.gamma**2 + (x - peak.x0)**2)
        
        
                    