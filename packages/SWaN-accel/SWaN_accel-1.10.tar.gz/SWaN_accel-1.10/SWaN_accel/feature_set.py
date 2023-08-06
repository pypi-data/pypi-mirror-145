import SWaN_accel.spectrum as spectrum
import SWaN_accel.orientation as orientation
import pandas as pd
import SWaN_accel.config as config
import SWaN_accel.utils as utils
import SWaN_accel.energy as energy
from numpy.linalg import norm
import numpy as np

def compute_extra_features(X,sampling):
   
    feature_list = []

    spectrum_feature_extractor = spectrum.FrequencyFeature(X, sr=sampling)
    spectrum_feature_extractor.fft()
    spectrum_feature_extractor.peaks()
    feature_list.append(spectrum_feature_extractor.dominant_frequency())
    feature_list.append(spectrum_feature_extractor.dominant_frequency_power())
    feature_list.append(spectrum_feature_extractor.total_power())


    ori_feature_extractor = orientation.OrientationFeature(X, subwins=config.winSize)
    ori_feature_extractor.estimate_orientation(unit='deg')
    feature_list.append(ori_feature_extractor.ori_x_median())
    feature_list.append(ori_feature_extractor.ori_y_median())
    feature_list.append(ori_feature_extractor.ori_z_median())
    feature_list.append(ori_feature_extractor.ori_var_sum())
    feature_list.append(ori_feature_extractor.ori_range_max())
    feature_list.append(ori_feature_extractor.zerocross_x_angle())
    feature_list.append(ori_feature_extractor.zerocross_y_angle())
    feature_list.append(ori_feature_extractor.zerocross_z_angle())

    X_vm = utils.vec2colarr(norm(X, ord=2, axis=1))
    energy_feature_extractor = energy.EnergyFeature(X_vm, subwins=30)
    energy_feature_extractor.get_energies()
    feature_list.append(energy_feature_extractor.smv_energy_sum())
    feature_list.append(energy_feature_extractor.smv_energy_var())

    ## calculate autocorrelation (create a dataframe for each feature)


    # def estimated_autocorrelation(x):
    #     """
    #     http://stackoverflow.com/q/14297012/190597
    #     http://en.wikipedia.org/wiki/Autocorrelation#Estimation
    #     """
    #     n = len(x)
    #     variance = x.var()
    #     x = x - x.mean()
    #     r = np.correlate(x, x, mode='full')[-n:]
    #     assert np.allclose(r, np.array([(x[:n - k] * x[-(n - k):]).sum() for k in range(n)]))
    #     result = r / (variance * (np.arange(n, 0, -1)))
    #     return result




    result = pd.concat(feature_list, axis=1)
    return result
