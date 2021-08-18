from typing import Dict, Union, Any, List, Optional, cast, Tuple


class RewardFunctionParams(object):
    def __init__(self):
        self.speed: float = 0.0
        self.all_wheels_on_track: bool = True
        self.waypoints: List[Tuple[float, float]] = [(0.0, 0.0)]
        self.closest_waypoints: List[int] = [0, 0]
        self.heading: float = 0.0
        self.steering_angle: float = 0.0  # agent's steering angle in degrees
        self.progress: float = 0.0  # percentage of track completed
        self.steps: int = 0  # number steps completed

    def to_dict(self) -> Dict:
        return vars(self)
