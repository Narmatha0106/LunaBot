# A* path planning on the grid map.

import heapq


def heuristic(a: tuple, b: tuple) -> float:
    # Manhattan distance - good enough for a grid where diagonal moves are allowed too.
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(node: tuple, grid) -> list:
    (x, y) = node
    size = grid.shape[0]
    candidates = [
        (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
        (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1),
    ]
    return [(nx, ny) for nx, ny in candidates
            if 0 <= nx < size and 0 <= ny < size and grid[nx, ny] == 0]


def a_star(start: tuple, goal: tuple, grid):
    # Returns the shortest path as a list of cells, or None if unreachable.
    open_set = [(0 + heuristic(start, goal), 0, start)]
    came_from = {}
    g_score = {start: 0}
    visited = set()

    while open_set:
        _, cost, current = heapq.heappop(open_set)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path
        if current in visited:
            continue
        visited.add(current)

        for nb in neighbors(current, grid):
            step_cost = 1.4142 if (nb[0] != current[0] and nb[1] != current[1]) else 1.0
            tentative_g = g_score[current] + step_cost
            if nb not in g_score or tentative_g < g_score[nb]:
                g_score[nb] = tentative_g
                priority = tentative_g + heuristic(nb, goal)
                heapq.heappush(open_set, (priority, tentative_g, nb))
                came_from[nb] = current
    return None
