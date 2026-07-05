# LunaRover - combines the A* planner with the sensor check to move
# the rover step by step and replan when something blocks its path.

from . import planner
from . import sensor


class LunaRover:
    def __init__(self, start: tuple, goal: tuple, grid):
        self.start = start
        self.goal = goal
        self.grid = grid
        self.position = start
        self.plan = planner.a_star(start, goal, grid)
        self.history = [start]
        self.status_log = []
        self.finished = False
        if self.plan is None:
            self.status_log.append("ERROR: No initial path found on this terrain.")
            self.finished = True
        else:
            self.status_log.append(f"Mission start. Initial path length: {len(self.plan)} steps.")

    def step(self, dynamic_positions: list) -> None:
        # Move one step closer to the goal, replanning if something's in the way.
        if self.finished or self.position == self.goal:
            self.finished = True
            return

        if not self.plan or len(self.plan) < 2:
            self.status_log.append("No further path available. Halting.")
            self.finished = True
            return

        next_step = self.plan[1]

        if sensor.sensor_detects_obstacle(next_step, dynamic_positions):
            self.status_log.append(f"Obstacle sensed near {next_step}. Replanning route...")
            temp_grid = self.grid.copy()
            for ox, oy in dynamic_positions:
                if 0 <= ox < temp_grid.shape[0] and 0 <= oy < temp_grid.shape[1]:
                    temp_grid[ox, oy] = 1
            new_plan = planner.a_star(self.position, self.goal, temp_grid)
            if new_plan:
                self.plan = new_plan
                self.status_log.append(f"New path found ({len(new_plan)} steps).")
            else:
                self.status_log.append("No alternate path found. Waiting...")
                return

        self.position = self.plan[1]
        self.plan = self.plan[1:]
        self.history.append(self.position)

        if self.position == self.goal:
            self.status_log.append("Goal reached! Habitat module docking complete.")
            self.finished = True
