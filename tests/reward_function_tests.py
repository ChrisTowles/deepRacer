import pytest


from reward_function import reward_function

def test_reward_function():

          data = {
            'sso': payload.identity.sso,
            'instance_name': instance_name,
            'processor_post_provisioning_message': json.loads(payload.to_json()),
            'operation_log':json.loads(sqllog_json)
        }


    reward: float = reward_function(data)
    assert reward
    
    
