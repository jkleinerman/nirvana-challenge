import random
import re

class ApiServer(object):
    """
    Simulates the API server.
    Every time the client connects the server, it will respond
    with different values of: deductible, stop_loss and oop_max
    gotten randomly from the intervals received in the constructor
    """

    def __init__(self,
                 deductible_interval: tuple[int, int]=(1000, 1200),
                 stop_loss_interval: tuple[int, int]=(10000, 13000),
                 oop_max_interval: tuple[int, int]=(5000, 6000)):
        """
        Limits deductible_interval, stop_loss_interval and opp_max_interval
        to let the function respond_client(), chose values randomly from them.
        By default it is limiting them with the values given in the problem
        statement.
        """
        self.deductible_interval = deductible_interval
        self.stop_loss_interval = stop_loss_interval
        self.oop_max_interval = oop_max_interval



    def respond_client(self, api_url: str) -> str:
        """
        Responds to client with values of deductible, stop_loss and oop_max
        chosen randomly from the intervals.
        To make it more realistic, the random value involves the member_id
        and the API number received in the URL
        """

        # Gets the API number and member ID from the URL received from
        # the client
        try:
            api_number = int(re.search('api(\d)', api_url).groups()[0])
            member_id = int(re.search('member_id=(\d)', api_url).groups()[0])
        except (IndexError, AttributeError):
            print(f'Invalid URL: {api_url}')
            return None

        # Combining API number and member_id number to get different random
        # output.
        # As it is a random output it makes no sense, but it is just a way
        # to use the inputs to get the result
        step = api_number + member_id

        deductible = random.randrange(*self.deductible_interval, step)
        stop_loss = random.randrange(*self.stop_loss_interval, step)
        oop_max = random.randrange(*self.oop_max_interval, step)

        # Return the result as a string to simulate a kind of
        # network connection
        return (f'{{"deductible": {deductible},'
                f' "stop_loss": {stop_loss},'
                f' "oop_max": {oop_max}}}'
               )


# A little testing of the server module
if __name__ == "__main__":
    api_server = ApiServer((600, 3000),
                           (5077, 14045),
                           (3745, 7021))
    print(api_server.respond_client('https://api2.com?member_id=1'))
