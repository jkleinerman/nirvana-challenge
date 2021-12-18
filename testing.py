import client
import server
import json
from statistics import mean


if __name__ == "__main__":

    base_api_urls = [
        'https://api1.com',
        'https://api2.com',
        'https://api3.com'
    ]





    strategy = 'min'
    member_id = 1
    print(f'Testing with member_id: {member_id} and strategy: {strategy}')

    api_server = server.ApiServer()

    api_client = client.ApiClient(api_server, strategy, *base_api_urls)
    api_client.get_from_srv(member_id)

    result = json.loads(api_client.output_to_user())

    try:
        assert min(api_client.deductible_list) == result['deductible']
        assert min(api_client.stop_loss_list) == result['stop_loss']
        assert min(api_client.oop_max_list) == result['oop_max']
        print('Test: PASS')

    except AssertionError:
        print('Test: FAILURE')



    strategy = 'max'
    member_id = 4
    print(f'Testing with member_id: {member_id} and strategy: {strategy}')

    api_server = server.ApiServer()

    api_client = client.ApiClient(api_server, strategy, *base_api_urls)
    api_client.get_from_srv(member_id)

    result = json.loads(api_client.output_to_user())

    try:
        assert max(api_client.deductible_list) == result['deductible']
        assert max(api_client.stop_loss_list) == result['stop_loss']
        assert max(api_client.oop_max_list) == result['oop_max']
        print('Test: PASS')

    except AssertionError:
        print('Test: FAILURE')



    strategy = 'mean'
    member_id = 79
    print(f'Testing with member_id: {member_id} and strategy: {strategy}')

    api_server = server.ApiServer()

    api_client = client.ApiClient(api_server, strategy, *base_api_urls)
    api_client.get_from_srv(member_id)

    result = json.loads(api_client.output_to_user())

    try:
        assert round(mean(api_client.deductible_list), 2) == result['deductible']
        assert round(mean(api_client.stop_loss_list), 2) == result['stop_loss']
        assert round(mean(api_client.oop_max_list), 2) == result['oop_max']
        print('Test: PASS')

    except AssertionError:
        print('Test: FAILURE')
