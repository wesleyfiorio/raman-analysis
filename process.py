import os
from typing import Tuple
import numpy as np
from tools import PeakGuess, Tools
class Process:   
    def __init__(
                self,

                tools: Tools,
                my_dir: str,
                MASK: Tuple[int, int],
                BASE_LINE: Tuple[int, int],
                params,
                bounds
                ) -> None:
        self.MASK = MASK
        self.BASE_LINE = BASE_LINE
       
        self.tools = tools
        self.my_dir = my_dir
        self.params = params
        self.bounds = bounds

    def process(self, data: np.ndarray):
        data = self.tools.truncate(data, self.MASK[0], self.MASK[1])
        data = self.tools.base_line(data, self.BASE_LINE[0], self.BASE_LINE[1])
        filename = os.path.basename("hello")
        # params_calculated, erros_calculated = self.tools.fit_lorentzians(data, self.params, self.bounds)
        self.tools.add_data_to_the_plot(data, filename, "allDatas")
        # self.tools.add_fits_to_the_plot(data, params_calculated, filename, "allFits")
        self.tools.save_plot("test", "test1", "allDatas")



current_directory = os.getcwd()
tools = Tools()
MASK = (260, 330)
BASE_LINE = (310, 330)

param2_guess = PeakGuess(
        x0=292,
        gamma=5.,
        A=2000.
        )

bounds = ([0, 0, 0], [ np.inf, np.inf, np.inf])

tools1 = Tools()
params = (param2_guess,)
process1 = Process(
    tools1,
    current_directory,
    MASK,
    BASE_LINE,
    param2_guess,
    bounds
)
a= np.array([[1,2], [1,3]])
process1.process(a)

