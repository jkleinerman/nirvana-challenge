import json
import statistics
import sys

import server


EXIT_FAILURE = 1
strategy = {'min': min, 'max': max, 'mean': statistics.mean}


class ApiClient(object):

    def __init__(self,
                 server: server.ApiServer,
                 member_id: int,
                 coalesce_strategy: str,
                 *base_api_urls: list[str]):
        """
        """
        self.api_server = api_server
        self.member_id = member_id
        try:
            self.coalesce_strategy = strategy[coalesce_strategy]
        except KeyError:
            print(f'Invalid Coalesce Strategy: {coalesce_strategy}')
            print('Options are: "min", "max" or "mean"')
            sys.exit(EXIT_FAILURE)
        self.base_api_urls = base_api_urls

        self.deductible_list = []
        self.stop_loss_list = []
        self.oop_max_list = []



    def get_from_srv(self):
        """
        """

        for base_api_url in self.base_api_urls:
            api_url = base_api_url + f'?member_id={self.member_id}'
            server_resp = json.loads(self.api_server.answer_client(api_url))

            self.deductible_list.append(server_resp['deductible'])
            self.stop_loss_list.append(server_resp['stop_loss'])
            self.oop_max_list.append(server_resp['oop_max'])

        deductible = self.coalesce_strategy(self.deductible_list)
        stop_loss = self.coalesce_strategy(self.stop_loss_list)
        oop_max = self.coalesce_strategy(self.oop_max_list)

        return f'{{"deductible": {deductible}, "stop_loss": {stop_loss}, "oop_max": {oop_max}}}'






if __name__ == "__main__":

    api_server = server.ApiServer()
    api_client = ApiClient(api_server, 1, 'min',
                           'https://api1.com',
                           'https://api2.com',
                           'https://api3.com')

    print(api_client.get_from_srv())
