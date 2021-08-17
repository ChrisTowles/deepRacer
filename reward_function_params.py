
from typing import Dict, Union, Any, List, Optional, cast


class RewardFunctionParams(object):
    def __init__(self):
        self.speed: float = 0.0
        self.all_wheels_on_track: bool = True
        self.waypoints: List[(float, float)] = [(0.0, 0.0)]
        self.closest_waypoints: List[int] = [0, 0]
        self.heading: float = 0.0

    def to_dict(self) -> Dict:
        return vars(self)
