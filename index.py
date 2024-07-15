from typing import Dict
import numpy as np
from Definitions.definition import DataAndPeaks, ParameterPeak, PeakBounds, PeakGuess
from dataAnalyser.DataFitter import DataFitter
from DataTools import DataTools
from Definitions.PeakSelection import PeakSelection
from ParameterPloter import ParameterPloter
from DataPloter import DataPloter
from dataAnalyser.dataAnalyzer import DataTruncator, BaselineCorrector
from fileManager import TXTFileManager
from RenishawFileReader import RenishawFileReader
from mapManager import MapManager
class DataProcessor:
    def __init__(self):
        self.data_tools = DataTools()
        self.directory = "data"
        
    def ajust_save(self):
        txt_file_manager = TXTFileManager(self.directory)
        txt_file_manager.reset_folder()
        #  read data and turn it in a apropiete format
        renishaw_reader = RenishawFileReader("mapa.txt")
        experimental_data = renishaw_reader.get_data()

      
        # truncate and remove the  baseline
        truncator = DataTruncator(100, 500)
        baseline_corrector = BaselineCorrector([110, 250, 370, 450, 500])
        self.data_tools.interact_in_dictionary(experimental_data.data_and_peaks, truncator.truncate )
        self.data_tools.interact_in_dictionary(experimental_data.data_and_peaks, baseline_corrector.remove_baseline)


        # define what is the peaks to ajust

        peak_guess_1 = PeakGuess(
                x0=140,
                gamma=10.,
                A=50.
            )
        peak_guess_2 = PeakGuess(
                x0=166.,
                gamma=10.,
                A=500.
            )
        peak_guess_3 = PeakGuess(
                x0=293,
                gamma=4.,
                A=2100.
            )
        peak_guess_4 = PeakGuess(
                x0=270,
                gamma=7.,
                A=100.
            )
        peak_guess_5 = PeakGuess(
            x0=330,
            gamma=10.,
            A=100.
        )
            
        # define bounds of the peaks  
        peak_bounds1 = PeakBounds(x0_min=139.5, x0_max=140)
        peak_bounds2 = PeakBounds(x0_min=155, x0_max=167)
        peak_bounds3 = PeakBounds(x0_min= 285, x0_max=297)
        peak_bounds4 = PeakBounds(x0_min= 260, x0_max=280)
        peak_bounds5 = PeakBounds(x0_min= 320, x0_max=340)
        
        dict_peak_guess = {
            "peak1": peak_guess_1,
            "peak2": peak_guess_2,
            "peak3": peak_guess_3,
            "peak4": peak_guess_4,
            "peak5": peak_guess_5
         }
        
        dict_peak_bounds = {
            "peak_bounds1": peak_bounds1,
            "peak_bounds2": peak_bounds2,
            "peak_bounds3": peak_bounds3,
            "peak_bounds4": peak_bounds4,
            "peak_bounds5": peak_bounds5
        }

        peak_selection = PeakSelection(dict_peak_guess, dict_peak_bounds)
        data_fitter = DataFitter(peak_selection)

        self.data_tools.interact_in_dictionary(experimental_data.data_and_peaks, data_fitter.perform_fit)
        ajusted_exp_data = data_fitter.get_experimental_data()
        
        txt_file_manager.add_data_to_file(ajusted_exp_data, "data.txt")
   
    def read_experimental(self):
        txt_file_manager = TXTFileManager(self.directory)
        self.exp_data = txt_file_manager.read_txt_file(self.directory + "/data.txt")

    def parameter_plot( self,
            x_param: ParameterPeak,
            y_param: ParameterPeak,
            peak_one: str,
            peak_two: str,
            dir: str):
        if self.exp_data is None:
            return
        dict_data_and_peaks = self.exp_data.data_and_peaks
        param_ploter = ParameterPloter(x_param, y_param, peak_one, peak_two, self.directory)
        self.data_tools.interact_in_dictionary(dict_data_and_peaks, param_ploter.plot)
        param_ploter.save_plot()
    
    def plot_fitted_data(self):
        data_plotter = DataPloter(self.directory)
        self.data_tools.interact_in_dictionary(self.exp_data.data_and_peaks, data_plotter.plot_and_save)
        
    def save_data_and_ajust(self):
        if self.exp_data is None: 
            return
        dict_data_and_peaks = self.exp_data.data_and_peaks 
        ploter = DataPloter()
        self.data_tools.interact_in_dictionary(dict_data_and_peaks, ploter.plot_and_save)
        
    def plot_map(self, peak_name: str, parameter: ParameterPeak):
        if self.exp_data is None: 
            return
        dict_data_and_peaks = self.exp_data.data_and_peaks
        map_manager = MapManager(peak_name, parameter)
        self.data_tools.interact_in_dictionary(dict_data_and_peaks, map_manager.add_data_map)
        map_manager.show()
      
        
    
processor = DataProcessor()
# processor.ajust_save()
processor.read_experimental()



