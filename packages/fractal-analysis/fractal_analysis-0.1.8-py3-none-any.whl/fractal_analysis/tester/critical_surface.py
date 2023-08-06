import functools
import math
from abc import ABC, abstractmethod
from typing import Union, List

import numpy as np
from numpy import linalg
from scipy.linalg import sqrtm


class CriticalSurfaceBrownianMotion(ABC):
    """
        alpha: significance level (look at quantiles of order alpha/2 and 1 − alpha/2)
    """

    def __init__(self,
                 N: int,
                 alpha: float = 0.05,
                 k: int = 1,
                 chi2_trials: int = 100000):
        self.N = N
        self.alpha = alpha
        self.k = k
        np.random.seed(6)
        self.chi2 = np.random.chisquare(df=1, size=(self.N, chi2_trials))

    @functools.cached_property
    def matrix_A_k(self):
        A_k = np.zeros((self.N, self.N))
        for i in range(self.N):
            for j in range(self.N):
                if abs(i - j) == self.k:
                    A_k[i, j] = 0.5 / (self.N - self.k)
                # elif i == j:
                #     A_k[i, j] = 1 / self.N #todo add k=0 case
        return A_k

    @abstractmethod
    def _autocovariance_matrix_increment(self, sig2: float, H: Union[List[float], np.ndarray, float],
                                         add_on_sig2: float):
        pass

    def _eigenvalues(self, sig2: float, H: Union[List[float], np.ndarray, float], add_on_sig2: float):
        Sigma: np.ndarray = self._autocovariance_matrix_increment(sig2=sig2, H=H, add_on_sig2=add_on_sig2)
        square_root_Sigma: np.ndarray = sqrtm(Sigma)
        A_k = self.matrix_A_k
        mat = square_root_Sigma.dot(A_k)
        mat = mat.dot(square_root_Sigma)
        eigenvalues, _ = linalg.eig(mat)
        return eigenvalues

    def _generalized_chi2(self, sig2, H: Union[List[float], np.ndarray, float], add_on_sig2: float):
        eigenvalues = self._eigenvalues(sig2=sig2, H=H, add_on_sig2=add_on_sig2)
        stat = np.array(eigenvalues.dot(self.chi2))
        return stat

    def quantile(self, sig2, H: Union[List[float], np.ndarray, float], add_on_sig2: float = 0):
        dist = self._generalized_chi2(sig2=sig2, H=H, add_on_sig2=add_on_sig2)
        quantile = [0, 0]
        quantile[0] = np.percentile(a=dist, q=100 * self.alpha / 2)
        quantile[1] = np.percentile(a=dist, q=100 - 100 * self.alpha / 2)
        return quantile


class CriticalSurfaceFBM(CriticalSurfaceBrownianMotion):
    """
        Source paper: Michał Balcerek, Krzysztof Burnecki. (2020)
                      Testing of fractional Brownian motion in a noisy environment.
                      Chaos, Solitons & Fractals, Volume 140, 110097.
                      https://doi.org/10.1016/j.chaos.2020.110097
    """

    def _r_k(self, k: int, H: float):
        twoH = 2 * H
        return 0.5 * ((k + 1) ** twoH + abs(k - 1) ** twoH - 2 * k ** twoH)

    def _r_M_k(self, k: int, add_on_sig2: float, H: float):
        r_k = self._r_k(k=k, H=H)
        if k == 0:
            r_M_k = r_k + 2 * add_on_sig2
        elif k == 1:
            r_M_k = r_k - add_on_sig2
        else:
            r_M_k = r_k
        return r_M_k

    def _autocovariance_matrix_increment(self, sig2: float, add_on_sig2: float, H: float):
        if not isinstance(H, (float, int)) or H > 1 or H < 0:
            raise ValueError(f'H is {H}, but it needs to be a float in [0,1].')
        Sigma = np.zeros((self.N, self.N))
        for i in range(self.N):
            for j in range(self.N):
                k = abs(i - j)
                Sigma[i, j] = sig2 * self._r_M_k(k=k, add_on_sig2=add_on_sig2, H=H)
        return Sigma


class CriticalSurfaceMFBM(CriticalSurfaceBrownianMotion):
    """
        Source paper: Balcerek, Michał, and Krzysztof Burnecki. (2020) Testing of Multifractional Brownian Motion.
                          Entropy 22, no. 12: 1403.
                          https://doi.org/10.3390/e22121403
    """

    @functools.lru_cache(maxsize=128)
    def _D(self, x: float, y: float):
        gam_xy = math.gamma(x + y + 1)
        gam_x = math.gamma(2 * x + 1)
        gam_y = math.gamma(2 * y + 1)
        sin_xy = math.sin(math.pi * (x + y) / 2)
        sin_x = math.sin(math.pi * x)
        sin_y = math.sin(math.pi * y)
        return math.sqrt(gam_x * gam_y * sin_x * sin_y) / 2 / gam_xy / sin_xy

    def _autocovariance_matrix(self, delta_t: int, delta_s: int, H: Union[List, np.ndarray]):
        Sigma = np.zeros((self.N, self.N))
        for i in range(self.N):
            for j in range(self.N):
                ht_idx = min(self.N - 1, i + delta_t)
                hs_idx = min(self.N - 1, j + delta_s)
                ht = H[ht_idx]
                hs = H[hs_idx]
                h = ht + hs
                D = self._D(x=ht, y=hs)
                Sigma[i, j] = D * (
                        (i + delta_t + 1) ** h + (j + delta_s + 1) ** h - abs(i + delta_t - j - delta_s) ** h)
        return Sigma

    def _autocovariance_matrix_increment(self, sig2: float, H: Union[List, np.ndarray], add_on_sig2=None):
        if isinstance(H, (float, int)):
            raise ValueError('H needs to be a list for MBM.')
        cov_t1_s1 = self._autocovariance_matrix(delta_t=1, delta_s=1, H=H)
        cov_t1_s0 = self._autocovariance_matrix(delta_t=1, delta_s=0, H=H)
        cov_t0_s1 = self._autocovariance_matrix(delta_t=0, delta_s=1, H=H)
        cov_t0_s0 = self._autocovariance_matrix(delta_t=0, delta_s=0, H=H)
        return cov_t1_s1 - cov_t1_s0 - cov_t0_s1 + cov_t0_s0

    # def _autocovariance_matrix_increment(self, sig2: float, H: Union[List, np.ndarray], add_on_sig2=None):
    #     if isinstance(H, (float, int)):
    #         raise ValueError('H needs to be a list for MBM.')
    #     Sigma = np.zeros((self.N, self.N))
    #     for i in range(self.N):
    #         for j in range(self.N):
    #             h1 = H[i]
    #             h2 = H[j]
    #             h = h1 + h2
    #             # D = self._D(alpha=h)
    #             D = self._D(x=h1, y=h2)
    #             k = abs(i - j)
    #             Sigma[i, j] = sig2 * D * ((i + 1) ** h + (j + 1) ** h - abs(i - j) ** h)
    #     return Sigma
