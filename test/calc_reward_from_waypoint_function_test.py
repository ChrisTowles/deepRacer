from typing import Tuple

import pytest

from reward_function import reward_function, calc_reward_from_waypoint_vs_heading, get_waypoint_look_ahead_average_point
from reward_function_params import RewardFunctionParams


class TestRewardFunction:

    def test_calc_reward_from_waypoints_vs_heading(self):
        params = RewardFunctionParams()
        params.waypoints = [(0.0, 0.0), (0.0, 1.0), (0.0, 2.0)]
        params.closest_waypoints = [0, 1]
        params.heading = 0.0
        direction_diff, reward = calc_reward_from_waypoint_vs_heading(closest_waypoints=params.closest_waypoints,
                                                                      waypoints=params.waypoints,
                                                                      heading=params.heading)

        assert direction_diff == 90
        assert reward == 0.5

    def test_calc_reward_from_waypoints_vs_heading_2(self):
        params = RewardFunctionParams()
        params.waypoints = [(0.0, 0.0), (0.0, 1.0), (0.0, 2.0)]
        params.closest_waypoints = [1, 2]
        params.heading = 0.0
        direction_diff, reward = calc_reward_from_waypoint_vs_heading(closest_waypoints=params.closest_waypoints,
                                                                      waypoints=params.waypoints,
                                                                      heading=params.heading)

        assert direction_diff == 90
        assert reward == 0.5

    def test_calc_reward_from_waypoints_vs_heading_3(self):
        params = RewardFunctionParams()
        params.waypoints = [(0.0, 0.0), (0.0, 1.0), (0.0, 2.0)]
        params.closest_waypoints = [0, 1]
        params.heading = 90
        direction_diff, reward = calc_reward_from_waypoint_vs_heading(closest_waypoints=params.closest_waypoints,
                                                                      waypoints=params.waypoints,
                                                                      heading=params.heading)

        assert direction_diff == 0.0
        assert reward == 1.0

    def test_get_waypoint_look_ahead_average_point_fixed_x(self):
        params = RewardFunctionParams()
        params.waypoints = [(0.0, 0.0), (0.0, 1.0), (0.0, 2.0)]
        params.closest_waypoints = [0, 1]
        params.heading = 90
        point: Tuple[float, float] = get_waypoint_look_ahead_average_point(closest_waypoints=params.closest_waypoints,
                                                                           waypoints=params.waypoints)

        assert point[0] == 0.0
        assert point[1] == 1.5

    def test_get_waypoint_look_ahead_average_point_fixed_y(self):
        params = RewardFunctionParams()
        params.waypoints = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]
        params.closest_waypoints = [0, 1]
        point: Tuple[float, float] = get_waypoint_look_ahead_average_point(closest_waypoints=params.closest_waypoints,
                                                                           waypoints=params.waypoints)

        assert point[0] == 1.5
        assert point[1] == 0.0

    def test_get_waypoint_look_ahead_average_point_linear(self):
        params = RewardFunctionParams()
        params.waypoints = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)]
        params.closest_waypoints = [0, 1]
        point: Tuple[float, float] = get_waypoint_look_ahead_average_point(closest_waypoints=params.closest_waypoints,
                                                                           waypoints=params.waypoints)

        assert point[0] == 2.5
        assert point[1] == 2.5

    def test_get_waypoint_look_ahead_average_point_linear(self):
        params = RewardFunctionParams()
        params.waypoints = [(0.0, 0.0), (1.0, 1.0), (2.0, 3.0), (3.0, 1.0), (4.0, 0.0)]
        params.closest_waypoints = [0, 1]
        point: Tuple[float, float] = get_waypoint_look_ahead_average_point(closest_waypoints=params.closest_waypoints,
                                                                           waypoints=params.waypoints)

        assert point[0] == 2.5
        assert point[1] == 1.25
