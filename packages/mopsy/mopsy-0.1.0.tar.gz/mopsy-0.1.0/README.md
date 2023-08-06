# mopsy - Matrix Operations in Python

Convenient library that provides methods to perform row/column operations over numpy and scipy matrices in Python. The goal of this library is to provide a similar interface to perform base R matrix methods/MatrixStats methods in python.

## Installation

Install from pypi

```shell
pip install mopsy
```

## Usage

```python
from mopsy import colsums
import random from rd
# generate a random sparse array with some density
from scipy.sparse import random
mat = random(10, 150, 0.25)

# generate random groups
ngrps = 15
gsets = [x for x in range(15)]
groups = [rd.choice(gsets) for x in range(mat.shape[axis])]

colsum(mat, groups)
```

<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.1.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
