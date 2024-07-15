# example of usage 
from dataAnalyser.DataFitter import DataFitter
from Definitions.PeakSelection import PeakSelection
from Definitions.definition import DataAndPeaks, ExperimentalData, Peak, PeakBounds, PeakGuess


exp_data = ExperimentalData({
        "0_1": DataAndPeaks(
            [[0,0],[0,0]],
            {
                "peak1": Peak(x0=0, A=0, gamma=0, x0Error=0, AError=0, gammaError=0),
                "peak2": Peak(x0=0, A=0, gamma=0, x0Error=0, AError=0, gammaError=0)
            }
            ),
        "0_2": DataAndPeaks(
            [[0,0],[0,0]], 
            {
                "peak1": Peak(x0=0, A=0, gamma=0, x0Error=0, AError=0, gammaError=0),
                "peak2": Peak(x0=0, A=0, gamma=0, x0Error=0, AError=0, gammaError=0)
            }
        )
        })

peak_guess_1 = PeakGuess(
        x0=139.5,
        gamma=10.,
        A=50.
    )

peak_guess_2 = PeakGuess(
        x0=165,
        gamma=10.,
        A=900.
    )

peak_guess_3 = PeakGuess(
        x0=292,
        gamma=5.,
        A=2000.
    )

dict_peak_guess = {
    "peak1": peak_guess_1,
    "peak2": peak_guess_2,
    "peak3": peak_guess_3
    }

peak_bounds1 = PeakBounds(x0_min=139.5, x0_max=145)
peak_bounds2 = PeakBounds(x0_min=155, x0_max=168)
peak_bounds3 = PeakBounds(x0_min= 285, x0_max=297)

dict_peak_bounds = {
    "peak_bounds1": peak_bounds1,
    "peak_bounds2": peak_bounds2,
    "peak_bounds3": peak_bounds3
}
# DataAndPeaks()
data = [[0.,0.],[0.,0.]]
peak_selection = PeakSelection(dict_peak_guess, dict_peak_bounds)
data_and_peaks = DataAndPeaks(data, None)
data_filter = DataFitter(peak_selection)
a = data_filter.__fit_lorentzians__(data)
print(a)
# data_filter.perform_fit(data_and_peaks)