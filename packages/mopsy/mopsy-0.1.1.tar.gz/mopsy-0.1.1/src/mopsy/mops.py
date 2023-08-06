from itertools import groupby
import numpy as np
from typing import Any, Callable

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "MIT"


class Mops:
    """Base class for all matrix operations"""

    def __init__(self, mat) -> None:
        """Intialize the matrix

        Args:
            mat (numpy.ndarray or scipy.sparse.spmatrix): a matrix
        """
        self.matrix = mat

    def groupby_indices(self, group: list) -> dict:
        """from a group vector, get the list of indices that map to each group

        Args:
            group (list): group variable, any list or array like object

        Returns:
            dict: each group and the list of indices that map to it
        """
        return {
            k: [x[0] for x in v]
            for k, v in groupby(
                sorted(enumerate(group), key=lambda x: x[1]), lambda x: x[1]
            )
        }

    def _apply(self, func: Callable[[list], Any], axis: int):
        """internal function that wraps numpy's apply_along_axis

        Args:
            func (Callable): a function to apply
            axis (int): 0 for rows, 1 for columns

        Returns:
            numpy.ndarray: a dense vector after appling group by
        """
        return np.apply_along_axis(func, axis, self.matrix)

    def apply(
        self, func: Callable[[list], Any], group: list = None, axis: int = 1
    ) -> np.ndarray:
        """apply a function to groups along an axis

        Args:
            func (Callable): a function to apply
            group (list, optional): group variable. Defaults to None.
            axis (int, optional): 0 for rows, 1 for columns. Defaults to 0.

        Raises:
            Exception: ApplyFuncError, when a function cannot be applied

        Returns:
            numpy.ndarray: a matrix
        """
        result = []
        try:
            if group is None:
                result = self.matrix._apply(func, axis=axis)
            else:
                for g, kmat in self.iter(group, axis):
                    tmat = kmat._apply(func, axis=axis)
                    result.append(tmat if axis == 0 else tmat.T)
                result = np.stack(result, axis=axis)
        except Exception as e:
            print(f"Error: applying function: {str(e)}")
            raise Exception("ApplyFuncError")

        return result
