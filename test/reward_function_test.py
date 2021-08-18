

import pytest

from reward_function import reward_function, calc_wheels_on_track_and_speed, calc_abs_steering, \
    get_waypoint_look_ahead_average_point, get_angle_between_points
from reward_function_params import RewardFunctionParams


class TestRewardFunction:

    def test_reward_function_no_wheels_on_track(self):
        params = RewardFunctionParams()
        params.all_wheels_on_track = False
        reward: float = reward_function(params.to_dict())
        assert reward == 0.001

    def test_get_angle_between_points(self):
        angle = get_angle_between_points([0.0, 0.0], [0.0, 1.0])
        assert angle == 90

    def test_get_angle_between_points(self):
        angle = get_angle_between_points([0.0, 0.0], [1.0, 1.0])
        assert angle == 45

    def test_get_angle_between_points(self):
        angle = get_angle_between_points([0.0, 0.0], [-1.0, -1.0])
        assert angle == -135

    def test_reward_function_no_wheels_on_track_to_slow(self):
        params = RewardFunctionParams()
        params.all_wheels_on_track = True
        reward: float = calc_wheels_on_track_and_speed(all_wheels_on_track=params.all_wheels_on_track,
                                                       speed=params.speed)
        assert reward == 0.6

    def test_reward_function_no_wheels_on_track_off_track(self):
        params = RewardFunctionParams()
        params.all_wheels_on_track = False
        params.speed = 4
        reward: float = calc_wheels_on_track_and_speed(all_wheels_on_track=params.all_wheels_on_track,
                                                       speed=params.speed)
        assert reward == 0.001

    def test_reward_function_no_wheels_on_track_fast_enough(self):
        params = RewardFunctionParams()
        params.all_wheels_on_track = True
        params.speed = 2
        reward: float = calc_wheels_on_track_and_speed(all_wheels_on_track=params.all_wheels_on_track,
                                                       speed=params.speed)
        assert reward == 1.0

    def test_reward_function_no_wheels_on_track_off_track_and_slow(self):
        params = RewardFunctionParams()
        params.all_wheels_on_track = False
        params.speed = 0.5
        reward: float = calc_wheels_on_track_and_speed(all_wheels_on_track=params.all_wheels_on_track,
                                                       speed=params.speed)
        assert reward == 0.001

    def test_reward_function_calc_abs_steering_to_much(self):
        params = RewardFunctionParams()

        params.steering_angle = -20
        reward: float = calc_abs_steering(steering_angle=params.steering_angle)
        assert reward == 0.800

    def test_reward_function_calc_abs_steering_stright(self):
        params = RewardFunctionParams()

        params.steering_angle = 0
        reward: float = calc_abs_steering(steering_angle=params.steering_angle)
        assert reward == 1.0

    def test_get_waypoint_look_ahead_average_point_fixed_x(self):
        params = RewardFunctionParams()
        params.waypoints = [[0.0, 0.0], [0.0, 1.0], [0.0, 2.0]]
        params.closest_waypoints = [0, 1]
        params.heading = 90
        params.x = 0,
        params.y = 0
        point: [float, float] = get_waypoint_look_ahead_average_point(closest_waypoints=params.closest_waypoints,
                                                                           waypoints=params.waypoints)

        assert point[0] == 0.0
        assert point[1] == 1.5

    def test_get_waypoint_look_ahead_average_point_fixed_y(self):
        params = RewardFunctionParams()
        params.waypoints = [[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]]
        params.closest_waypoints = [0, 1]
        point: [float, float] = get_waypoint_look_ahead_average_point(closest_waypoints=params.closest_waypoints,
                                                                           waypoints=params.waypoints)

        assert point[0] == 1.5
        assert point[1] == 0.0

    def test_get_waypoint_look_ahead_average_point_linear(self):
        params = RewardFunctionParams()
        params.waypoints = [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]]
        params.closest_waypoints = [0, 1]
        point: [float, float] = get_waypoint_look_ahead_average_point(closest_waypoints=params.closest_waypoints,
                                                                           waypoints=params.waypoints)

        assert point[0] == 2.5
        assert point[1] == 2.5

    def test_get_waypoint_look_ahead_average_point_curve(self):
        params = RewardFunctionParams()
        params.waypoints = [[0.0, 0.0], [1.0, 1.0], [2.0, 3.0], [3.0, 1.0], [4.0, 0.0]]
        params.closest_waypoints = [0, 1]
        point: [float, float] = get_waypoint_look_ahead_average_point(closest_waypoints=params.closest_waypoints,
                                                                           waypoints=params.waypoints)

        assert point[0] == 2.5
        assert point[1] == 1.25
