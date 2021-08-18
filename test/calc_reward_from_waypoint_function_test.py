from typing import Tuple

import pytest

from reward_function import reward_function, calc_reward_from_waypoint_vs_heading, \
    get_waypoint_look_ahead_average_point, WaypointCalcResult
from reward_function_params import RewardFunctionParams


class TestRewardFunction:

    def test_calc_reward_from_waypoints_vs_heading_on_x_axis(self):
        params = RewardFunctionParams()
        params.waypoints = [(0.0, 0.0), (0.0, 1.0), (0.0, 2.0)]
        params.closest_waypoints = [0, 1]
        params.heading = 0.0
        params.x = 0,
        params.y = 0
        result: WaypointCalcResult = calc_reward_from_waypoint_vs_heading(closest_waypoints=params.closest_waypoints,
                                                                          waypoints=params.waypoints,
                                                                          heading=params.heading,
                                                                          steering_angle=params.steering_angle,
                                                                          current_point=[params.x, params.y])

        assert result.needed_heading == 90
        assert result.delta_in_heading == 90
        assert result.delta_in_steering == 90
        assert result.reward == 0.001

    def test_calc_reward_from_waypoints_vs_heading_toward_point(self):
        params = RewardFunctionParams()
        params.waypoints = [(0.0, 0.0), (0.0, 1.0), (1.0, 2.0), (2.0, 3.0)]
        params.closest_waypoints = [1, 2]
        params.heading = 0.0
        params.x = 0,
        params.y = 0
        result: WaypointCalcResult = calc_reward_from_waypoint_vs_heading(closest_waypoints=params.closest_waypoints,
                                                                          waypoints=params.waypoints,
                                                                          heading=params.heading,
                                                                          steering_angle=params.steering_angle,
                                                                          current_point=[params.x, params.y])

        assert result.needed_heading == 59.0362
        assert result.delta_in_heading == 59.0362
        assert result.delta_in_steering == 59.0362
        assert result.reward == 0.001

    def test_calc_reward_from_waypoints_vs_heading_on_x_axis(self):
        params = RewardFunctionParams()
        params.waypoints = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0)]
        params.closest_waypoints = [0, 1]
        params.heading = 0
        params.steering_angle = 0
        params.x = 0,
        params.y = 0
        result: WaypointCalcResult = calc_reward_from_waypoint_vs_heading(closest_waypoints=params.closest_waypoints,
                                                                          waypoints=params.waypoints,
                                                                          heading=params.heading,
                                                                          steering_angle=params.steering_angle,
                                                                          current_point=[params.x, params.y])

        assert result.needed_heading == 0
        assert result.delta_in_heading == 0
        assert result.delta_in_steering == 0
        assert result.reward == 1.0

    def test_calc_reward_from_waypoints_vs_heading_steering_already_toward_heading(self):
            params = RewardFunctionParams()
            params.waypoints = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)]
            params.closest_waypoints = [0, 1]
            params.heading = 30
            params.steering_angle = 15
            params.x = 0,
            params.y = 0
            result: WaypointCalcResult = calc_reward_from_waypoint_vs_heading(
                closest_waypoints=params.closest_waypoints,
                waypoints=params.waypoints,
                heading=params.heading,
                steering_angle=params.steering_angle,
                current_point=[params.x, params.y])

            assert result.needed_heading == 45
            assert result.delta_in_heading == 15
            assert result.delta_in_steering == 0
            assert result.reward == 1.0

    def test_calc_reward_from_waypoints_vs_heading_steering_almosty_toward_heading(self):
        params = RewardFunctionParams()
        params.waypoints = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)]
        params.closest_waypoints = [0, 1]
        params.heading = 30
        params.steering_angle = 10
        params.x = 0,
        params.y = 0
        result: WaypointCalcResult = calc_reward_from_waypoint_vs_heading(
            closest_waypoints=params.closest_waypoints,
            waypoints=params.waypoints,
            heading=params.heading,
            steering_angle=params.steering_angle,
            current_point=[params.x, params.y])

        assert result.needed_heading == 45
        assert result.delta_in_heading == 15
        assert result.delta_in_steering == 5
        assert result.reward == 1.0