import os
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from typing import Dict, List, NamedTuple, Tuple, Union
import copy

from Definitions.PeakSelection import PeakSelection
from Definitions.definition import Peak, PeakGuess


class Tools:
    def __init__(self) -> None:
       self.subplots: Dict[str, plt.Axes] = {}

    def gaussian(self, x: np.ndarray, A: float, mu: float, sigma: float):
        return A * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

    def fit_gaussian(self, data):
        y = data[:, 1]
        x = data[:, 0]
        x_max_y = data[y.argmax(), 0]
        p0 = [max(y), x_max_y, 1]
        # Fit curve
        popt, pcov = curve_fit(self.gaussian, x, y, p0=p0)
        return popt

    def truncate(self, data: np.ndarray, x_min: float, x_max: float) -> np.ndarray:
        mask = (data[:, 0] >= x_min) & (data[:, 0] <= x_max)
        return data[mask]

    def calculate_average_in_yaxis(self, data):
        sum_of_numbers = sum(data[:, 1])
        count_of_numbers = len(data[:, 1])
        if count_of_numbers == 0:
            print("Mask out of the range")
            return 0
        return sum_of_numbers / count_of_numbers

    def shift_peak(self, data, popt, value=31.6536 ):
        shift_amount = value - popt[1]
        data[:, 0] += shift_amount
        popt_compy =  copy.deepcopy(popt)
        popt_compy[1] = value
        return data, popt_compy

    def normalize_using_GaAs_peak(self, data):
        y_max = np.max(data[:, 1])
        data[:, 1] /= y_max
        return data
    


    def baseline(self, data: np.ndarray, x_data: List[float]) -> np.ndarray:
        y_data = self.__find_y_for_listX__(x_data, data)
        polynomiun_degree = len(x_data) -1
        coeffs = np.polyfit(x_data, y_data, polynomiun_degree)
        fitted_curve = np.polyval(coeffs, data[:, 0]) 
        
        data[:, 1] = data[:, 1] - fitted_curve
        
        return data
    
    def __find_nearest_number__(self, list_number: List[float], target: float):
        return min(list_number, key = lambda x: abs(x - target))
     
    def __find_nearest_list_number__(self, list_number_x: List[float],  data: np.ndarray):
        list_number_calculated = []
        for num in  list_number_x: 
            nearest_number = self.__find_nearest_number__(list(data[:, 0]), num)
            list_number_calculated.append(nearest_number)
        
        
        return list_number_calculated
    
    def __find_y_for_x__(self, x: float, data: np.ndarray):
        x_values = data[:, 0]
        index = np.where(x_values == x )[0]
        
        if len(index) == 0:
            return None
        
        return data[index[0],1]
    
    def __find_y_for_listX__(self, list_x: List[float], data: np.ndarray):
        y_list: List[float] =[]
        list_x_corrected = self.__find_nearest_list_number__(list_x, data)
        for x in list_x_corrected: 
            y_list.append(self.__find_y_for_x__(x, data))
        return y_list
    
    def lorentzian(self, x_data: np.ndarray, params: PeakGuess) -> np.ndarray:
        return params.A * (params.gamma**2 / ((x_data - params.x0)**2 + params.gamma**2))

    def multiple_lorentzians(self, x_data: np.ndarray, *params_list: float) -> np.ndarray:
        if len(params_list) % 3 != 0:
            raise ValueError("Invalid number of parameters. Each Lorentzian requires 3 parameters.")
        
        result = np.zeros_like(x_data)
        for i in range(0, len(params_list), 3):
            lorentzian_params = PeakGuess(x0=params_list[i], gamma=params_list[i+1], A=params_list[i+2])
            result += self.lorentzian(x_data, lorentzian_params)
        return result
    
    def __peak_guess__(self, dict_peak: Dict[str, Peak]) -> Tuple[float, ...]:
        flattened_list = []
        
        for peak in dict_peak.values():
            flattened_list.extend([peak.x0, peak.gamma, peak.A])

        return tuple(flattened_list)

    def flattened_tuple_to_dict_peak_guess(self, float_list: Tuple[float, ...]) -> Dict[str, Peak]:
        if len(float_list) % 3 != 0:
                raise ValueError("The input list has an invalid length. It must be a multiple of 3.")

        dict_peak: Dict[str, PeakGuess] = {}
        for i in range(0, len(float_list), 3):

            peak = Peak(x0=float_list[i], gamma=float_list[i+1], A=float_list[i+2])
            dict_peak["peak" + str(i)] = peak
        
        return dict_peak

    def fit_lorentzians(
            self,
            data: np.ndarray,
            params: Tuple[PeakGuess, ...],
            bds: Union[None, Tuple[list, list] ]= None, 
            key: str = " "
            ) -> Tuple[Tuple[PeakGuess, ...], Tuple[PeakGuess, ...]]: 
        
        if bds == None:
            bds = ([-np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf])

        x_data = data[:, 0]
        y_data = data[:, 1]
        p0 = self.__peak_guess__(params)
        
      
        try :
            popt, pcov = curve_fit(self.multiple_lorentzians, x_data, y_data, p0=p0, bounds=bds)
            print(f"\n The data {key} has been successfully fitted.")
            return self.flattened_tuple_to_dict_peak_guess(popt), self.flattened_tuple_to_dict_peak_guess(np.sqrt(np.diag(pcov)))
        
        except Exception as e:
            print(f"\nAn error occurred while fitting the data: {key}" )
            print(e)
            
        peak_guess = PeakGuess(0, 0, 0)
        tuple_of_zero: Tuple[PeakGuess, ...] = (peak_guess,)
        return (tuple_of_zero, tuple_of_zero)
    



#  One more thing is important in the future. Remove all things relacioned with plots in a new object
#  Move sme complex logics to news def to encampsulate functions
#  Move each class to a new file.
#  There is a lot of problem with naming, for example Raman
#  I can´t improve this. I already spend two days with this code. I can`t spend more time
        



