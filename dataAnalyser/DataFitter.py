from Definitions.PeakSelection import PeakSelection
from Definitions.PeakSelectionGeter import PeakSelectionGeter
from Definitions.definition import DataAndPeaks, ExperimentalData, Peak, PeakGuess


import numpy as np
from scipy.optimize import curve_fit


from typing import Dict, List, Union


class DataFitter:
    def __init__(self, peak_selection: PeakSelection):
        self.peak_selection = peak_selection
        self.experimental_data: ExperimentalData = ExperimentalData({})
        self.dic_data_and_peaks: Dict[str, DataAndPeaks] = {} 

    def __lorentzian__(self, x_data: List[float], peakGuess: PeakGuess):
        return peakGuess.A * (peakGuess.gamma**2 / ((np.array(x_data) - peakGuess.x0)**2 + peakGuess.gamma**2))

    def __multiple_lorentzians__(self, x_data: List[float], *params_list: float):
        
        if len(params_list) % 3 != 0:
            raise ValueError("Invalid number of parameters. Each Lorentzian requires 3 parameters.")

        result = np.zeros_like(x_data)
        for i in range(0, len(params_list), 3):
            x0 = params_list[i]
            gamma = params_list[i+1]
            A = params_list[i+2]
            lorentzian_params = PeakGuess(x0, gamma, A)
            result += self.__lorentzian__(x_data, lorentzian_params)
        return result

    def __fit_lorentzians__(
            self,
            data: List[List[float]],
            key: str = " "
            ):
        
        peak_selection = PeakSelectionGeter(self.peak_selection)
        bounds = peak_selection.get_list_bonds()
        
        if bounds == None:
            bounds = ([-np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf])

        peak_selection = PeakSelectionGeter(self.peak_selection)
        p0 = peak_selection.get_list_param()
        data_ndarray = np.array(data)
        x_data = data_ndarray[:, 0]
        y_data = data_ndarray[:, 1]
     
        try :
            popt, pcov = curve_fit(self.__multiple_lorentzians__, x_data, y_data, p0=p0, bounds=bounds)
            print(f"\n The data {key} has been successfully fitted.")
            perr = np.sqrt(np.diag(pcov))
            dict_peak = self.__convert_list_to_peak__(popt, perr)
            return dict_peak

        except Exception as e:
            print(f"\nAlert: an error occurred while fitting the data: {key}" )
            print(e)
        
        dict_peak1: Dict[str, None] = {}
        dict_peak_guess = self.peak_selection.dict_peak_guess
        list_values = list(dict_peak_guess.keys())
        for peak_name in list_values:
            dict_peak1[peak_name] = None
        
        return None

    def __convert_peak_selection_to_list__(self, peakSelection: PeakSelection):
        param_guess: List[float] = []

        for peak in peakSelection.dict_peak_guess.values():
            param_guess.extend(peak.get_list_param())

        return param_guess

    def __convert_list_to_peak__(self, param_peak: List[float], param_bounds: List[float]) -> Dict[str, Peak]:
        dic_peaks: Dict[str, Peak] = {}

        # Check if the lengths of param_peak and param_bounds are multiples of 3
        if len(param_peak) % 3 != 0 or len(param_bounds) % 3 != 0:
            raise ValueError("Input lists must have lengths that are multiples of 3")

        for i in range(0, len(param_peak), 3):
            peak = Peak(
                x0=param_peak[i],
                A=param_peak[i+1],  
                gamma=param_peak[i+2],
                x0Error=param_bounds[i],
                AError=param_bounds[i+1],
                gammaError=param_bounds[i+2],
            )
            dic_peak_guess = self.peak_selection.dict_peak_guess
            list_values = list(dic_peak_guess.keys())
            indice =int( (i + 1) /3) 
            dic_peaks[list_values[indice]] = peak
        
        return dic_peaks

    def perform_fit(self, data_and_peak: DataAndPeaks, key: str)-> None:
        data = data_and_peak.data
        dic_peak = self.__fit_lorentzians__(data)
        data_and_peak = DataAndPeaks(data, dic_peak) 
        self.dic_data_and_peaks[key] = data_and_peak 
        
    def get_experimental_data(self)-> ExperimentalData:
        return ExperimentalData(self.dic_data_and_peaks)

  