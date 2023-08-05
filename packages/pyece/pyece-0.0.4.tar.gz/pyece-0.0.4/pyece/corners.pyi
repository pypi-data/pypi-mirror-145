import numpy as np
from .primitive import PointCloud as PointCloud
from typing import Tuple

class Corners(PointCloud):
    def get(self) -> np.ndarray: ...
    @staticmethod
    def product(shape: Tuple) -> Corners: ...
