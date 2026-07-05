# Builds the terrain grid for the habitat zone.
# 0 = free ground, 1 = crater/boulder (blocked)

import random
import numpy as np


def generate_terrain(size: int, num_craters: int, seed: int = None) -> np.ndarray:
    # Places a few random circular craters on an empty grid.
    if seed is not None:
        random.seed(seed)
    grid = np.zeros((size, size), dtype=int)
    for _ in range(num_craters):
        cx, cy = random.randint(2, size - 3), random.randint(2, size - 3)
        radius = random.randint(1, 2)
        for i in range(size):
            for j in range(size):
                if (i - cx) ** 2 + (j - cy) ** 2 <= radius ** 2:
                    grid[i, j] = 1
    return grid


def clear_zone(grid: np.ndarray, point: tuple) -> None:
    # Make sure start/goal points are never accidentally blocked.
    grid[point] = 0
