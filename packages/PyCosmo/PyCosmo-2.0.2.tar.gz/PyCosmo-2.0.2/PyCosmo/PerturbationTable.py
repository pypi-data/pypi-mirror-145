# This file is part of PyCosmo, a multipurpose cosmology calculation tool in Python.
#
# Copyright (C) 2013-2021 ETH Zurich, Institute for Particle and Astrophysics and SIS
# ID.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from scipy import interpolate


def check_diff(diff, thresh):
    return np.any(diff[np.isfinite(diff)] > thresh)


class PerturbationTable:
    """
    This class has been written to handle operations involving building tabulated data.
    For some of the calculations this is often useful. These tables can then be accessed
    through interpolation routines rather than doing the full calculations repeatedly.
    """

    def __init__(self, cosmo, perturbation):
        self._cosmo = cosmo
        self._params = cosmo.params
        self._perturbation = perturbation
        self._interpolator = None
        self._a_limits = None
        self._k_limits = None

    def powerspec_a_k(self, a=1.0, k=0.1, diag_only=False):

        if self._interpolator is None:
            self._setup_interpolator()
        a = np.atleast_1d(a)
        k = np.atleast_1d(k)

        if np.min(a) < self._a_limits[0] or np.max(a) > self._a_limits[1]:
            raise ValueError(f"found a values outside range {self._a_limits}")
        if np.min(k) < self._k_limits[0] or np.max(k) > self._k_limits[1]:
            raise ValueError(f"found k values outside range {self._k_limits}")

        if diag_only:
            if len(a) != len(k):
                raise ValueError(
                    "for diag_only=True a and k vectors must have same length"
                )
            return np.exp(self._interpolator.ev(np.log(a), np.log(k)))
        return np.exp(self._interpolator.ev(np.log(a), np.log(k)))

    def __getattr__(self, name):
        try:
            return getattr(self, _perturbation, name)
        except AttributeError:
            raise AttributeError(
                f"{self._perturbation} has no attribute {name}"
            ) from None

    def _setup_interpolator(self):
        lna_min = -17
        lna_max = 0.0
        lna_grid = np.linspace(lna_min, lna_max, 200)
        a_grid = np.exp(lna_grid)
        k_grid = self._interp_grid_k()
        lnk_grid = np.log(k_grid)
        values = np.log(self.perturbation.powerspec_a_k(np.exp(lna_grid), k_grid))
        self._interpolator = RectBivariateSpline(lna_grid, np.log(k_grid), values)
        self._a_limits = (lna_min, lna_max)
        self._k_limits = (min(k_grid), max(k_grid))

        if self._params.tabulation_check_accuracy:
            k_grid_middle_points = np.exp(0.5 * lnk_grid[1:] + 0.5 * lnk_grid[:-1])
            mid_values = self.perturbation.powerspec_a_k(a_grid, middle_points)
            interpolated_values = np.exp(
                self._interpolator.ev(np.ex(lna_grid), k_grid_middle_points)
            )
            if not np.allclose(
                mid_values,
                interpolated_values,
                atol=0,
                rtol=self._params.tabulation_rtol,
            ):
                raise ValueError(
                    "the given grid for a and k produced rel error larger "
                    f"than {self._params.tabulation_rtol}"
                )

    def _interp_grid_k(self):
        if self._params.tabulation == "bao":
            c = self._cosmo
            k_wiggles = np.pi / (c.background.r_s() / c.params.h)
            k_first = 10 ** np.linspace(-5, np.log10(k_wiggles), 10)

            h = np.pi / 5
            n = 22
            k_middle = k_wiggles * np.arange(1, n / h) * h

            k_last = 10 ** np.linspace(np.log10(k_middle[-1]), 2, 10)

            k_grid = np.hstack((k_first, k_middle, k_last))

        elif self._params.tabulation == "manual":
            k_grid = self._params.tabulation_k_grid

        # remove duplicates in log values:
        return np.exp(np.array(sorted(set(np.log(k_grid)))))
