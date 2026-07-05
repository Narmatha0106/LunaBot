# Runs a full mission with no GUI window and saves the results as images.
# Handy for the report and for testing without opening pygame.
# Run with: python report_simulation.py
# Output: lunabot_path.png, lunabot_run.gif

import matplotlib
matplotlib.use("Agg")  # no display needed
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from lunabot import terrain, obstacles, robot

GRID_SIZE = 30
NUM_CRATERS = 9
NUM_DYNAMIC_OBS = 3

grid = terrain.generate_terrain(GRID_SIZE, NUM_CRATERS, seed=7)
START, GOAL = (1, 1), (GRID_SIZE - 2, GRID_SIZE - 2)
terrain.clear_zone(grid, START)
terrain.clear_zone(grid, GOAL)

rover = robot.LunaRover(START, GOAL, grid)
dyn_obstacles = obstacles.spawn_obstacles(NUM_DYNAMIC_OBS, GRID_SIZE, {START, GOAL})

dyn_history = []
max_steps = 400
while not rover.finished and len(rover.history) < max_steps:
    for obs in dyn_obstacles:
        obs.step(GRID_SIZE)
    dyn_positions = [obs.position() for obs in dyn_obstacles]
    dyn_history.append(dyn_positions.copy())
    rover.step(dyn_positions)

for line in rover.status_log:
    print("[LunaBot]", line)

# static path image
fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(grid.T, cmap="copper_r", origin="lower")
xs = [p[0] for p in rover.history]
ys = [p[1] for p in rover.history]
ax.plot(xs, ys, color="lime", linewidth=2, label="Rover path")
ax.scatter(*START, color="cyan", s=120, marker="s", label="Base / Lander", zorder=5)
ax.scatter(*GOAL, color="red", s=120, marker="*", label="Target Habitat", zorder=5)
ax.set_title("LunaBot Navigation Path over Simulated Lunar Terrain")
ax.legend(loc="upper left", fontsize=8)
ax.set_xlabel("Grid X")
ax.set_ylabel("Grid Y")
plt.tight_layout()
plt.savefig("lunabot_path.png", dpi=180)
print("[LunaBot] Saved lunabot_path.png")

# animated gif
fig2, ax2 = plt.subplots(figsize=(6, 6))

def animate(frame):
    ax2.clear()
    ax2.imshow(grid.T, cmap="copper_r", origin="lower")
    ax2.scatter(*START, color="cyan", s=100, marker="s")
    ax2.scatter(*GOAL, color="red", s=100, marker="*")
    trail = rover.history[:frame + 1]
    tx = [p[0] for p in trail]
    ty = [p[1] for p in trail]
    ax2.plot(tx, ty, color="lime", linewidth=2)
    ax2.scatter(tx[-1], ty[-1], color="white", edgecolor="black", s=90, zorder=6, label="LunaBot")
    if frame < len(dyn_history) and dyn_history[frame]:
        dx = [p[0] for p in dyn_history[frame]]
        dy = [p[1] for p in dyn_history[frame]]
        ax2.scatter(dx, dy, color="orange", marker="x", s=70, label="Moving debris")
    ax2.set_title(f"LunaBot Live Navigation - step {frame + 1}/{len(rover.history)}")
    ax2.legend(loc="upper left", fontsize=7)
    ax2.set_xlim(-1, GRID_SIZE)
    ax2.set_ylim(-1, GRID_SIZE)

ani = animation.FuncAnimation(fig2, animate, frames=len(rover.history), interval=150)
ani.save("lunabot_run.gif", writer="pillow", fps=7)
print("[LunaBot] Saved lunabot_run.gif")
