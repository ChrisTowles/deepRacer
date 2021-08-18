import pytest

from reward_function import reward_function, calc_wheels_on_track_and_speed, calc_abs_stearing
from reward_function_params import RewardFunctionParams


class TestRewardFunction:

    def test_reward_function_no_wheels_on_track(self):
        params = RewardFunctionParams()
        params.all_wheels_on_track = False
        reward: float = reward_function(params.to_dict())
        assert reward == 0.001

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


    def test_reward_function_calc_abs_stearing_to_much(self):
        params = RewardFunctionParams()

        params.steering_angle = -20
        reward: float = calc_abs_stearing(steering_angle=params.steering_angle)
        assert reward == 0.800


    def test_reward_function_calc_abs_stearing_stright(self):
        params = RewardFunctionParams()

        params.steering_angle = 0
        reward: float = calc_abs_stearing(steering_angle=params.steering_angle)
        assert reward == 1.0
