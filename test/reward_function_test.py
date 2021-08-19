

import pytest

from reward_function import reward_function, calc_wheels_on_track_and_speed, calc_abs_steering, \
    get_waypoint_look_ahead_average_point, get_angle_between_points, calc_center_line
from reward_function_params import RewardFunctionParams


class TestRewardFunction:

    def test_reward_function_no_wheels_on_track(self):
        params = RewardFunctionParams()
        params.all_wheels_on_track = False

        reward: float = reward_function(params.to_dict())
        assert reward == 1e-3

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
        params.speed = 1.0
        reward: float = calc_wheels_on_track_and_speed(all_wheels_on_track=params.all_wheels_on_track,
                                                       speed=params.speed,
                                                       delta_in_heading=0)
        assert reward == 0.6

    def test_reward_function_no_wheels_on_track_to_slow_bad_delta_heading(self):
        params = RewardFunctionParams()
        params.all_wheels_on_track = True


        reward: float = calc_wheels_on_track_and_speed(all_wheels_on_track=params.all_wheels_on_track,
                                                       speed=params.speed,
                                                       delta_in_heading=20)
        assert reward == 1.0

    def test_reward_function_no_wheels_on_track_off_track(self):
        params = RewardFunctionParams()
        params.all_wheels_on_track = False
        params.speed = 4
        reward: float = calc_wheels_on_track_and_speed(all_wheels_on_track=params.all_wheels_on_track,
                                                       speed=params.speed,
                                                       delta_in_heading=5)
        assert reward == 0.001

    def test_reward_function_no_wheels_on_track_fast_enough(self):
        params = RewardFunctionParams()
        params.all_wheels_on_track = True
        params.speed = 2
        reward: float = calc_wheels_on_track_and_speed(all_wheels_on_track=params.all_wheels_on_track,
                                                       speed=params.speed,
                                                       delta_in_heading=0)
        assert reward == 0.6

    def test_reward_function_no_wheels_on_track_off_track_and_slow(self):
        params = RewardFunctionParams()
        params.all_wheels_on_track = False
        params.speed = 0.5
        reward: float = calc_wheels_on_track_and_speed(all_wheels_on_track=params.all_wheels_on_track,
                                                       speed=params.speed,
                                                       delta_in_heading=0)
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
                                                                      waypoints=params.waypoints,
                                                                      lookahead_by=3)

        assert point[0] == 0.0
        assert point[1] == 1.5

    def test_get_waypoint_look_ahead_average_point_fixed_y(self):
        params = RewardFunctionParams()
        params.waypoints = [[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]]
        params.closest_waypoints = [0, 1]
        point: [float, float] = get_waypoint_look_ahead_average_point(closest_waypoints=params.closest_waypoints,
                                                                           waypoints=params.waypoints,
                                                                      lookahead_by=3)

        assert point[0] == 1.5
        assert point[1] == 0.0

    def test_get_waypoint_look_ahead_average_point_linear(self):
        params = RewardFunctionParams()
        params.waypoints = [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]]
        params.closest_waypoints = [0, 1]
        point: [float, float] = get_waypoint_look_ahead_average_point(closest_waypoints=params.closest_waypoints,
                                                                           waypoints=params.waypoints,
                                                                      lookahead_by=3)

        assert point[0] == 1.5
        assert point[1] == 1.5

    def test_get_waypoint_look_ahead_average_point_curve(self):
        params = RewardFunctionParams()
        params.waypoints = [[0.0, 0.0], [1.0, 1.0], [2.0, 3.0], [3.0, 1.0], [4.0, 0.0]]
        params.closest_waypoints = [0, 1]
        point: [float, float] = get_waypoint_look_ahead_average_point(closest_waypoints=params.closest_waypoints,
                                                                           waypoints=params.waypoints,
                                                                      lookahead_by=3)

        assert point[0] == 1.5
        assert point[1] == 2.0

    def test_calc_center_line_near_center(self):
        params = RewardFunctionParams()
        params.distance_from_center = 1.0
        params.track_width = 5.0
        reward: float = calc_center_line(distance_from_center=params.distance_from_center,
                                                                           track_width=params.track_width)

        assert reward == 0.5

    def test_calc_center_line_far_from_center(self):
        params = RewardFunctionParams()
        params.distance_from_center = 2.0
        params.track_width = 2.0
        reward: float = calc_center_line(distance_from_center=params.distance_from_center,
                                                                           track_width=params.track_width)

        assert reward == 1e-3

    def test_calc_center_line_mid_from_center(self):
        params = RewardFunctionParams()
        params.distance_from_center = 0.0
        params.track_width = 1.0
        reward: float = calc_center_line(distance_from_center=params.distance_from_center,
                                                                           track_width=params.track_width)

        assert reward == 1.0
