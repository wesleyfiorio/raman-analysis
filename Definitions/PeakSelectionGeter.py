from BondsListMaker import BondsListMaker
from DataTools import DataTools
from Definitions.PeakSelection import PeakSelection
from dataAnalyser.dataAnalyzer import ParamListMaker


class PeakSelectionGeter:
    def __init__(self, peakSelection: PeakSelection):
        self.dict_param_guess = peakSelection.dict_peak_guess
        self.dict_paramBonds = peakSelection.dict_peak_bounds
    
    def get_list_bonds(self):
        data_tools = DataTools()
        bonds_list_maker = BondsListMaker()
        data_tools.interact_in_dictionary(self.dict_paramBonds, bonds_list_maker.makeList)
        
        return (bonds_list_maker.bounds_min, bonds_list_maker.bonds_max)

    def get_list_param(self):
        data_tools = DataTools()
        param_list_maker = ParamListMaker()
        data_tools.interact_in_dictionary(self.dict_param_guess, param_list_maker.makeList)
        return (param_list_maker.params)