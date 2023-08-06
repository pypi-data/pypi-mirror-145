from typing import Union, List, Annotated

import numpy as np
import pandas as pd
import math
import random


class FbmSimulator:
    """
        Source paper: todo:add source paper
        Corresponding Matlab code: todo:add link to matlab code
        Main idea: we use Lamperti transform to transfer FBM (self-similar process) to a stationary process, and
                   simulate the stationary process using circulant embedding approach (Wood, A.T.A., Chan, G., 1994.
                   Simulation of stationary Gaussian processes in [0, 1]^d. Journal of computational and graphical
                   statistics 3, 409–432). Then a subsequence of the simulated stationary process is convert back to
                   the FBM series. Because we need to use its subsequence, the stationary process needs to have a longer
                   length (lamperti_series_len_multiplier*series_len) than the FBM series.
    """

    def __init__(self,
                 series_len: int,
                 hurst_parameter: float,
                 lamperti_series_len_multiplier: int = 5,
                 tmax: float = 1,
                 const: float = 1,
                 seed: int = None):
        """
            series_len: length of the fbm series to simulate
            hurst_index: hurst parameter of fbm
            lamperti_series_len_multiplier: bigger value (usually <=10) provides more accuracy; default value is 5
            tmax: the time runs in [0,tmax]; the default value is 1
            const: standard derivation at initial point; default value is 1

        """
        self.series_len = series_len
        self.hurst_parameter = hurst_parameter
        if not (0 < self.hurst_parameter < 1):
            raise ValueError(f'Hurst index must be in range (0, 1).')
        self.tmax = tmax
        if not self.tmax > 0:
            raise ValueError(f'tmax must be positive.')
        self.const = const
        if not self.const > 0:
            raise ValueError(f'const must be positive.')
        self.seed = seed
        self.lamperti_series_len_multiplier = lamperti_series_len_multiplier
        self.lamperti_series_len = self.lamperti_series_len_multiplier * self.series_len

    @property
    def _lamperti_subseq_index(self):
        seires_step = self.tmax / self.series_len
        series_t = np.arange(start=seires_step, stop=self.tmax + seires_step, step=seires_step)
        # transfer time to (1,e)
        series_exp_t = (np.exp(1) - 1)/self.tmax * series_t + 1
        # log of time in (1,e) is in (0,1)
        log_series_exp_t = np.log(series_exp_t)
        max_log_series_exp_t = np.max(log_series_exp_t)
        lamperti_subseq_index = np.rint(log_series_exp_t * self.lamperti_series_len / max_log_series_exp_t) - 1
        return lamperti_subseq_index.astype(int)

    def _line_circulant(self, m):
        """
            First line of the circulant matrix C built with covariances of the stationary process.
        """