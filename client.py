import json
import statistics
import sys
import argparse

import server

# Exit code when there is an error
EXIT_FAILURE = 1

# Dictionary of functions applied to list of data to coalesce data.
strategy_funcs = {'min': min, 'max': max, 'mean': statistics.mean}


class ApiClient(object):
    """Simulates the API client."""

    def __init__(self,
                 api_server: server.ApiServer,
                 coalesce_strategy: str,
                 *base_api_urls: list[str]):
        """
        Inits the client "connecting" to a server previously created.
        Establishes a default coalesce strategy.
        Receives a variable amount of API URLs that then will be used
        to coalesce the data according to the coalesce strategy.
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
        Connects to all server APIs that are in base_api_urls list with
        member_id received as argument, to fill deductible_list,
        stop_loss_list and oop_max_list lists.
        Since the server sends the response as string, it is converted
        to dictionary with json module
        """

        # Cleans the lists if there is old data
        self.deductible_list = []
        self.stop_loss_list = []
        self.oop_max_list = []

        for base_api_url in self.base_api_urls:
            api_url = base_api_url + f'?member_id={member_id}'
            server_resp = json.loads(self.api_server.respond_client(api_url))

            try:
                self.deductible_list.append(server_resp['deductible'])
                self.stop_loss_list.append(server_resp['stop_loss'])
                self.oop_max_list.append(server_resp['oop_max'])
            except KeyError:
                print('There is missing information in server response.')

        # # For debug
        # print(f'Deductible List: {self.deductible_list}\n'
        #       f'Stop Loss List: {self.stop_loss_list}\n'
        #       f'Oop Max List: {self.oop_max_list}\n'
        #      )


    def output_to_user(self) -> str:
        """
        Returns a string with the format of a JSON with the values
        deductible, stop_loss and oop_max according to the coalesce strategy.
        """

        try:
            deductible = self.coalesce_strategy(self.deductible_list)
            deductible = round(deductible, 2) # makes sense in case mean strat.
            stop_loss = self.coalesce_strategy(self.stop_loss_list)
            stop_loss = round(stop_loss, 2) # makes sense in case mean strat.
            oop_max = self.coalesce_strategy(self.oop_max_list)
            oop_max = round(oop_max, 2) # makes sense in case mean strat.
        except (ValueError, statistics.StatisticsError):
            # This exception can happen when one of the lists are empty
            # For example: get_from_srv() was NOT called yet
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


    base_api_urls = [
        'https://api1.com',
        'https://api2.com',
        'https://api3.com'
    ]

    api_server = server.ApiServer()
    api_client = ApiClient(api_server, strategy, *base_api_urls)

    api_client.get_from_srv(member_id)
    result = api_client.output_to_user()

    print('For the following APIs:')
    for base_api_url in base_api_urls:
        print(f'- {base_api_url}')
    print(f'Using member ID: {member_id} and Coalesce Strategy: {strategy}\n'
          f'The result is: {result}'
         )
