from .mops import Mops

import numpy as np

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


class Nops(Mops):
    """Internal representation for numpy arrays"""

    def __init__(self, mat: np.ndarray) -> None:
        """Intialize with a numpy matrix

        Args:
            mat (numpy.ndarray): numpy matrix
        """
        super().__init__(mat)

    def iter(self, group=None, axis=0) -> tuple:
        """an Iterator over groups and an axis

        Args:
            group (list, optional): group variable. Defaults to None.
            axis (int, optional): 0 for rows, 1 for columns. Defaults to 0.

        Yields:
            tuple (str, Nops): of group and the submatrix
        """
        mat = self.matrix

        if group is None:
            yield (group, self)
        else:
            idx_groups = self.groupby_indices(group)
            for k, v in idx_groups.items():
                if axis == 0:
                    yield (
                        k,
                        Nops(
                            mat[
                                v,
                            ]
                        ),
                    )
                else:
                    yield (k, Nops(mat[:, v]))
