import pytest

from reward_function import reward_function, calc_reward_from_wayspoint_vs_heading
from reward_function_params import RewardFunctionParams


class TestRewardFunction:

    def test_calc_reward_from_waypoints_vs_heading(self):
        params = RewardFunctionParams()
        params.waypoints = [(0.0, 0.0), (0.0, 1.0), (0.0, 2.0)]
        params.closest_waypoints = [0, 1]
        params.heading = 0.0
        direction_diff, reward = calc_reward_from_wayspoint_vs_heading(closest_waypoints=params.closest_waypoints,
                                                                       waypoints=params.waypoints,
                                                                       heading=params.heading)

        assert direction_diff == 90
        assert reward == 0.5

    def test_calc_reward_from_waypoints_vs_heading_2(self):
        params = RewardFunctionParams()
        params.waypoints = [(0.0, 0.0), (0.0, 1.0), (0.0, 2.0)]
        params.closest_waypoints = [1, 2]
        params.heading = 0.0
        direction_diff, reward = calc_reward_from_wayspoint_vs_heading(closest_waypoints=params.closest_waypoints,
                                                                       waypoints=params.waypoints,
                                                                       heading=params.heading)

        assert direction_diff == 90
        assert reward == 0.5

    def test_calc_reward_from_waypoints_vs_heading_3(self):
        params = RewardFunctionParams()
        params.waypoints = [(0.0, 0.0), (0.0, 1.0), (0.0, 2.0)]
        params.closest_waypoints = [0, 1]
        params.heading = 90
        direction_diff, reward = calc_reward_from_wayspoint_vs_heading(closest_waypoints=params.closest_waypoints,
                                                                       waypoints=params.waypoints,
                                                                       heading=params.heading)

        assert direction_diff == 0.0
        assert reward == 1.0
