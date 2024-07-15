from Definitions.definition import DataAndPeaks, ParameterPeak, Peak
from tools import Tools


from matplotlib import pyplot as plt


class ParameterPloter:
    def __init__(
            self,
            x_param: ParameterPeak,
            y_param: ParameterPeak,
            peak_one: str,
            peak_two: str,
            dir: str
            ):
        self.peak_one = peak_one
        self.peak_two = peak_two
        self.x_param = x_param
        self.y_param = y_param
        self.dir = dir
        self.tools = Tools()

    def plot(self, data_and_peaks: DataAndPeaks, key: str):
        if data_and_peaks.peaks is None:
            return
        try:

            peak_one = data_and_peaks.peaks.get(self.peak_one, None)
            peak_two = data_and_peaks.peaks.get(self.peak_two, None)

            if peak_one is not None and peak_two is not None:
                value_param_one = self.__get_value__(self.x_param, peak_one)
                value_param_two = self.__get_value__(self.y_param, peak_two)

                plt.scatter([value_param_one], [value_param_two])

        except KeyError as e:
            print(f"KeyError: {e} not found in peaks dictionary")
        except Exception as e:
            print(f"An error occurred: {e}")

    def __get_value__(self, param: ParameterPeak, peak: Peak) -> float:
            attr_name = param.value
            if attr_name:
                return getattr(peak, attr_name)
            else:
                print("there is a problem with the get_value")
                return 0



    def save_plot(self):
        plt.xlabel(f"{self.peak_one}, param = {self.x_param.value} ")
        plt.ylabel(f"{self.peak_two}, param = { self.y_param.value}")
        plt.show()