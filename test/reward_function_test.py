import pytest

from reward_function import reward_function
from reward_function_params import RewardFunctionParams


class TestRewardFunction:

    def test_reward_function_no_wheels_on_track(self):
        params = RewardFunctionParams()
        params.all_wheels_on_track = False
        reward: float = reward_function(params.to_dict())
        assert reward == 0.001

