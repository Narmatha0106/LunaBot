# Simulated proximity sensor - stands in for a real ultrasonic/IR sensor.


def sensor_detects_obstacle(next_pos: tuple, dynamic_positions: list, safe_radius: int = 1) -> bool:
    # True if an obstacle is within safe_radius cells of where the rover wants to go next.
    for ox, oy in dynamic_positions:
        if abs(ox - next_pos[0]) <= safe_radius and abs(oy - next_pos[1]) <= safe_radius:
            return True
    return False
