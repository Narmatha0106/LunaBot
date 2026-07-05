# Moving obstacles (dust/debris) that drift around the habitat zone.

import random


class DynamicObstacle:
    def __init__(self, grid_size: int, forbidden: set):
        while True:
            self.pos = [random.randint(3, grid_size - 4), random.randint(3, grid_size - 4)]
            if tuple(self.pos) not in forbidden:
                break
        self.dx = random.choice([-1, 0, 1])
        self.dy = random.choice([-1, 0, 1])

    def step(self, grid_size: int) -> None:
        self.pos[0] = min(max(1, self.pos[0] + self.dx), grid_size - 2)
        self.pos[1] = min(max(1, self.pos[1] + self.dy), grid_size - 2)
        if random.random() < 0.25:          # random drift change
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])

    def position(self) -> tuple:
        return tuple(self.pos)


def spawn_obstacles(count: int, grid_size: int, forbidden: set) -> list:
    return [DynamicObstacle(grid_size, forbidden) for _ in range(count)]
