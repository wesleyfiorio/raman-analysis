
from Definitions.definition import ExperimentalData, ParameterPeak, Peak, PeakGuess
from typing import Callable, Dict, List, TypeVar
from tools import Tools
import numpy as np



T = TypeVar('T')


class DataTools:
    def __init__(self):
        self.tools = Tools()

    def interact_in_dictionary(self, dictionary: Dict[str, T], callback: Callable[[T, str], None]):
        for key, value in dictionary.items():
            callback(value, key)


    def experimental_data_to_list(self, exp_data: ExperimentalData, param: ParameterPeak, peakKey: str):
        list_value: List[float] = []
        x_list: List[float] = []
        y_list: List[float] = []

        for key, value in exp_data.data_and_peaks.items():
            dic_peaks = value.peaks
            xy_list: List[str] = key.split("_")
            x_list.append(float(xy_list[0]))
            y_list.append(float(xy_list[1]))
            if dic_peaks is not None:
                peak: Peak = dic_peaks[peakKey]
            list_value.append(self.__get_value__(param, peak))

        return (x_list, y_list, list_value)

    def __get_value__(self, param: ParameterPeak, peak: Peak) -> float:
        attr_name = param.value
        if attr_name:
            return getattr(peak, attr_name)
        else:
            print("there is a problem with the get_value")
            return 0

    def plot_and_save(self, experimetal_data: ExperimentalData):

        experimetal_data.data_and_peaks
        dict_data_and_peaks = experimetal_data.data_and_peaks

        for key, value in  dict_data_and_peaks.items():
            if value.peaks is None:
                print("DataAndPeak is empity!")
                return

            data = value.data
            self.tools.add_data_to_the_plot(np.array(data), key, key)
            for peak in value.peaks.values():
                peakGuessCalculated = PeakGuess(peak.x0, peak.A, peak.gamma)
                self.tools.add_fit_to_the_plot(np.array(data),(peakGuessCalculated, ),key, key  )
                self.tools.save_plot(key, "data", key)