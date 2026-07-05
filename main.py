# LunaBot GUI - shows the rover navigating the habitat zone live.
# Run with: python main.py
# Controls: SPACE = pause/resume, N = new mission, ESC = quit

import sys
import pygame
from lunabot import terrain, obstacles, robot

# --- settings you can tweak ---
GRID_SIZE = 26
NUM_CRATERS = 8
NUM_DYNAMIC_OBS = 3
CELL_SIZE = 22
PANEL_WIDTH = 320
FPS = 8

WIDTH = GRID_SIZE * CELL_SIZE + PANEL_WIDTH
HEIGHT = GRID_SIZE * CELL_SIZE

# --- colors ---
COLOR_BG = (20, 22, 28)
COLOR_FREE = (194, 154, 108)
COLOR_OBSTACLE = (40, 30, 25)
COLOR_PATH = (60, 220, 90)
COLOR_ROVER = (255, 255, 255)
COLOR_START = (60, 200, 255)
COLOR_GOAL = (255, 70, 70)
COLOR_DYNAMIC = (255, 165, 0)
COLOR_PANEL = (28, 32, 40)
COLOR_TEXT = (230, 230, 230)
COLOR_TITLE = (110, 170, 255)


class LunaBotApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("LunaBot - Autonomous Lunar Habitat Navigation")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 16)
        self.font_small = pygame.font.SysFont("consolas", 13)
        self.font_title = pygame.font.SysFont("consolas", 20, bold=True)
        self.paused = False
        self.step_count = 0
        self.new_mission()

    def new_mission(self, seed=None):
        self.grid = terrain.generate_terrain(GRID_SIZE, NUM_CRATERS, seed=seed)
        self.start = (1, 1)
        self.goal = (GRID_SIZE - 2, GRID_SIZE - 2)
        terrain.clear_zone(self.grid, self.start)
        terrain.clear_zone(self.grid, self.goal)
        self.rover = robot.LunaRover(self.start, self.goal, self.grid)
        self.dyn_obstacles = obstacles.spawn_obstacles(
            NUM_DYNAMIC_OBS, GRID_SIZE, {self.start, self.goal}
        )
        self.step_count = 0
        self.paused = False

    def update(self):
        if self.paused or self.rover.finished:
            return
        for obs in self.dyn_obstacles:
            obs.step(GRID_SIZE)
        dyn_positions = [obs.position() for obs in self.dyn_obstacles]
        self.rover.step(dyn_positions)
        self.step_count += 1

    def draw_grid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                color = COLOR_OBSTACLE if self.grid[i, j] == 1 else COLOR_FREE
                rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
                pygame.draw.rect(self.screen, color, rect)

        # planned remaining path
        if self.rover.plan:
            for (x, y) in self.rover.plan:
                rect = pygame.Rect(x * CELL_SIZE + 6, y * CELL_SIZE + 6, CELL_SIZE - 13, CELL_SIZE - 13)
                pygame.draw.rect(self.screen, COLOR_PATH, rect)

        # start & goal markers
        self._draw_marker(self.start, COLOR_START)
        self._draw_marker(self.goal, COLOR_GOAL)

        # dynamic obstacles
        for obs in self.dyn_obstacles:
            x, y = obs.position()
            center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.circle(self.screen, COLOR_DYNAMIC, center, CELL_SIZE // 2 - 3)

        # rover
        rx, ry = self.rover.position
        center = (rx * CELL_SIZE + CELL_SIZE // 2, ry * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(self.screen, COLOR_ROVER, center, CELL_SIZE // 2 - 2)
        pygame.draw.circle(self.screen, (0, 0, 0), center, CELL_SIZE // 2 - 2, 2)

    def _draw_marker(self, pos, color):
        x, y = pos
        rect = pygame.Rect(x * CELL_SIZE + 3, y * CELL_SIZE + 3, CELL_SIZE - 7, CELL_SIZE - 7)
        pygame.draw.rect(self.screen, color, rect, border_radius=4)

    def draw_panel(self):
        panel_x = GRID_SIZE * CELL_SIZE
        pygame.draw.rect(self.screen, COLOR_PANEL, (panel_x, 0, PANEL_WIDTH, HEIGHT))

        title = self.font_title.render("LunaBot Control Panel", True, COLOR_TITLE)
        self.screen.blit(title, (panel_x + 15, 15))

        status = "PAUSED" if self.paused else ("REACHED GOAL" if self.rover.finished else "NAVIGATING")
        lines = [
            f"Status : {status}",
            f"Steps  : {self.step_count}",
            f"Start  : {self.start}",
            f"Goal   : {self.goal}",
            f"Rover  : {self.rover.position}",
            "",
            "Controls:",
            " SPACE - Pause / Resume",
            " N     - New Mission",
            " ESC   - Quit",
            "",
            "Mission Log:",
        ]
        y = 55
        for line in lines:
            surf = self.font.render(line, True, COLOR_TEXT)
            self.screen.blit(surf, (panel_x + 15, y))
            y += 22

        # scrollable-ish log (last N entries)
        for entry in self.rover.status_log[-14:]:
            wrapped = self._wrap(entry, 34)
            for w in wrapped:
                surf = self.font_small.render(w, True, (180, 220, 180))
                self.screen.blit(surf, (panel_x + 15, y))
                y += 18

    @staticmethod
    def _wrap(text, width):
        words = text.split()
        lines, cur = [], ""
        for w in words:
            if len(cur) + len(w) + 1 <= width:
                cur = (cur + " " + w).strip()
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_n:
                        self.new_mission()

            self.update()

            self.screen.fill(COLOR_BG)
            self.draw_grid()
            self.draw_panel()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    LunaBotApp().run()
