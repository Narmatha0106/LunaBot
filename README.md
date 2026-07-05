# LunaBot — Autonomous Navigation Robot for Lunar Habitats
### (Pure Software Project — runs entirely on a laptop, no hardware required)

LunaBot simulates an autonomous rover that navigates between lunar habitat
modules, avoiding static obstacles (craters/boulders) using an A* global
planner, and dynamic obstacles (drifting dust/debris) using a reactive
sensor-based local avoidance layer.

---

## 1. Project Structure

```
lunabot_sw/
├── lunabot/                 # Core package (the "engine")
│   ├── __init__.py
│   ├── terrain.py           # Terrain / occupancy grid generation
│   ├── planner.py           # A* global path planning algorithm
│   ├── obstacles.py         # Dynamic obstacle simulation
│   ├── sensor.py            # Simulated ultrasonic sensor logic
│   └── robot.py             # LunaRover controller (ties it all together)
├── main.py                  # Interactive GUI application (pygame)
├── report_simulation.py     # Headless batch mode -> generates report images/GIF
├── requirements.txt
└── README.md
```

---

## 2. Prerequisites

- A laptop (Windows / macOS / Linux) — no internet needed after setup.
- Python 3.9 or newer installed.
  - Check: open a terminal / command prompt and run `python3 --version`
    (on Windows try `python --version`).
  - If not installed, download from https://www.python.org/downloads/
    and during installation, tick **"Add Python to PATH"**.

---

## 3. Step-by-Step Setup (from scratch)

**Step 1 — Create a project folder and copy all files into it**
Place the `lunabot/` package folder, `main.py`, `report_simulation.py`,
`requirements.txt`, and this `README.md` all inside one folder, e.g. `LunaBot/`.

**Step 2 — Open a terminal in that folder**
- Windows: open the folder in File Explorer → type `cmd` in the address bar → Enter.
- macOS/Linux: right-click the folder → "Open Terminal here" (or `cd` into it manually).

**Step 3 — Create a virtual environment (recommended, keeps things clean)**
```bash
python3 -m venv venv
```
Activate it:
```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```
You should see `(venv)` appear at the start of your terminal prompt.

**Step 4 — Install the required libraries**
```bash
pip install -r requirements.txt
```
This installs `numpy`, `pygame`, and `matplotlib`.

**Step 5 — Run the interactive GUI application**
```bash
python main.py
```
A window opens showing the lunar terrain grid, the rover, obstacles, and
a live control panel with the mission log.

**Controls:**
| Key | Action |
|---|---|
| `SPACE` | Pause / Resume the mission |
| `N` | Start a new mission (regenerates terrain + obstacles) |
| `ESC` | Quit the application |

**Step 6 — Generate report-ready output images (optional but recommended)**
```bash
python report_simulation.py
```
This runs a full mission with no GUI window and saves two files in the
same folder:
- `lunabot_path.png` — final planned path over the terrain
- `lunabot_run.gif` — animation of the entire mission

Use these images/GIF as figures/screenshots in your project report and
PowerPoint presentation.

---

## 4. How the Navigation Logic Works (quick summary)

1. `terrain.py` generates a grid map of the habitat zone with random
   crater/boulder obstacles.
2. `planner.py` runs the **A\*** search algorithm to compute the shortest
   safe path from the start (Base/Lander) to the goal (Habitat module).
3. `obstacles.py` simulates moving debris/dust drifting across the zone.
4. `sensor.py` checks, at every step, whether a moving obstacle is about
   to block the rover's next move (like an ultrasonic sensor reading).
5. `robot.py` (the `LunaRover` class) executes the plan step-by-step, and
   whenever the sensor reports a blockage, it **replans a new path in
   real time** from its current position — this is the reactive
   avoidance behaviour.
6. `main.py` is the GUI layer — it draws everything and lets you watch
   the mission live and interact with it.

---

## 5. Testing Checklist (before submission)

- [ ] `python main.py` opens the GUI window without errors.
- [ ] Rover reaches the red goal marker in the window (status changes to
      "REACHED GOAL").
- [ ] Pressing `N` generates a new random terrain and restarts the mission.
- [ ] Pressing `SPACE` pauses/resumes correctly.
- [ ] `python report_simulation.py` produces `lunabot_path.png` and
      `lunabot_run.gif` without errors.

---

## 6. Preparing for Submission

1. Take 2–3 screenshots of the running GUI (different mission stages:
   start, mid-navigation with an obstacle replan, goal reached) — use
   your OS screenshot tool (Windows: `Win+Shift+S`, macOS: `Cmd+Shift+4`).
2. Insert these screenshots + `lunabot_path.png` into the project report
   document (see `LunaBot_Software_Project_Report.docx`).
3. Zip the entire project folder (`LunaBot/`) — this is your source-code
   submission.
4. Submit: the report (.docx or PDF export) + the zipped source code
   folder + (optionally) the `lunabot_run.gif` as a demo attachment.

---

## 7. Possible Viva / Review Questions & Short Answers

- **Why A\*?** It guarantees the shortest path and is efficient enough to
  run on low-power onboard processors, unlike more exhaustive search
  methods.
- **What happens if no path exists?** The planner returns `None`, and the
  system logs an error instead of crashing — handled in `robot.py`.
- **How is this different from a hardware rover?** The same navigation
  algorithm (A* + reactive sensing) is designed to be portable to real
  sensors (ultrasonic/IR now, LIDAR/stereo camera later) with minimal
  changes — only `sensor.py` and `obstacles.py` would be replaced with
  real sensor drivers.
- **What is the time complexity of A\*?** O(E) in the worst case where E
  is the number of edges explored, bounded by grid size squared for a
  grid graph; in practice it explores far fewer nodes due to the
  heuristic.
