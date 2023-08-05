from typing import Union

import numpy as np

from osaft.solutions.base_arf import BaseARF


class ARFData:
    """Container for plotting data for ARF plots

    :param sol: solution
    """

    _instances = 0
    _line_styles = [
        '-',
        '--',
        ':',
        '-.',
        (0, (5, 10)),
        (0, (3, 1, 1, 1)),
        (0, (1, 2)),
        (0, (8, 10)),
        (0, (5, 5)),
        (0, (5, 1)),
        (0, (3, 10, 1, 10)),
        (0, (3, 5, 1, 5)),
        (0, (3, 1, 1, 1)),
        (0, (3, 10, 1, 10, 1, 10)),
        (0, (3, 5, 1, 5, 1, 5)),
        (0, (3, 1, 1, 1, 1, 1)),
    ]

    def __init__(self, sol: BaseARF) -> None:
        self.sol = sol
        self._arf = None
        self._norm_arf = None
        self._instance = ARFData._instances
        ARFData._instances += 1

    def compute_arf(self, attr_name: str, values: np.ndarray) -> None:
        arf = []
        for val in values:
            setattr(self.sol, attr_name, val)
            arf.append(self.sol.compute_arf())

        self._arf = np.asarray(arf)
        self._plotting = self._arf

    def normalize_arf(self, norm: np.ndarray) -> None:
        self._norm_arf = self._arf / norm
        self._plotting = self._norm_arf

    @property
    def line_style(self) -> Union[str, tuple[int, tuple[int]]]:

        L = len(ARFData._line_styles)
        return ARFData._line_styles[self._instance % L]

    @property
    def arf(self) -> np.ndarray:
        return self._arf

    @property
    def plotting(self) -> np.ndarray:
        return self._plotting

    @property
    def name(self) -> str:
        return self.sol.name


if __name__ == '__main__':
    pass
