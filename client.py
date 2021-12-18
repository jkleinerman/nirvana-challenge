import json
import statistics
import sys
import argparse

import server


EXIT_FAILURE = 1
strategy_funcs = {'min': min, 'max': max, 'mean': statistics.mean}


class ApiClient(object):

    def __init__(self,
                 server: server.ApiServer,
                 coalesce_strategy: str,
                 *base_api_urls: list[str]):
        """
        """
        self.api_server = api_server
        try:
            self.coalesce_strategy = strategy_funcs[coalesce_strategy]
        except KeyError:
            print(f'Invalid Coalesce Strategy: {coalesce_strategy}')
            print('Options are: "min", "max" or "mean"')
            sys.exit(EXIT_FAILURE)
        self.base_api_urls = base_api_urls

        self.deductible_list = []
        self.stop_loss_list = []
        self.oop_max_list = []



    def get_from_srv(self, member_id: int):
        """
        """

        # Clean if there is old data
        self.deductible_list = []
        self.stop_loss_list = []
        self.oop_max_list = []

        for base_api_url in self.base_api_urls:
            api_url = base_api_url + f'?member_id={member_id}'
            server_resp = json.loads(self.api_server.answer_client(api_url))

            try:
                self.deductible_list.append(server_resp['deductible'])
                self.stop_loss_list.append(server_resp['stop_loss'])
                self.oop_max_list.append(server_resp['oop_max'])
            except KeyError:
                print('There is missing information in server response')


    def output_to_user(self) -> str:
        """
        """

        try:
            deductible = self.coalesce_strategy(self.deductible_list)
            deductible = round(deductible, 2)
            stop_loss = self.coalesce_strategy(self.stop_loss_list)
            stop_loss = round(stop_loss, 2)
            oop_max = self.coalesce_strategy(self.oop_max_list)
            oop_max = round(oop_max, 2)
        except (ValueError, statistics.StatisticsError):
            print("Client didn't get server information or server"
                  " didn't send all the information."
                 )
            return None

        return (f'{{"deductible": {deductible},'
                f' "stop_loss": {stop_loss},'
                f' "oop_max": {oop_max}}}'
               )






if __name__ == "__main__":

    # Creating an argparse object to help the user to use correctly
    # the command line arguments.
    # The -t option is optional when the user wants to test the value
    # of the objective against the Telnyx testing API
    in_parser = argparse.ArgumentParser(description='Connect and coalesce data')
    in_parser.add_argument('-i', '--member-id', type=int,
                           dest='member_id', required=True, help='Member ID')

    in_parser.add_argument('-s', '--strategy', type=str,
                           dest='strategy', required=True,
                           choices={'min','max','mean'},
                           help='Coalesce Strategy')

    args = vars(in_parser.parse_args())

    member_id = args['member_id']
    strategy = args['strategy']


    api_server = server.ApiServer()
    api_client = ApiClient(api_server, strategy,
                           'https://api1.com',
                           'https://api2.com',
                           'https://api3.com')

    api_client.get_from_srv(member_id)

    print(api_client.output_to_user())
