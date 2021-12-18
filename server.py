import random
import re

class ApiServer(object):

    def __init__(self,
                 deductible_interval: tuple[int, int]=(500, 2000),
                 stop_loss_interval: tuple[int, int]=(5000, 15000),
                 oop_max_interval: tuple[int, int]=(3000, 7000)):
        """
        """
        self.deductible_interval = deductible_interval
        self.stop_loss_interval = stop_loss_interval
        self.oop_max_interval = oop_max_interval


    def answer_client(self, api_url: str) -> str:
        """
        """

        try:
            api_number = int(re.search('api(\d)', api_url).groups()[0])
            member_id = int(re.search('member_id=(\d)', api_url).groups()[0])
        except (IndexError, AttributeError):
            print(f'Invalid URL: {api_url}')
            return None

        # Combining API number and member_id number to get different random
        # output.
        # As it is a random output it makes no sense, but it is just a way
        # to use the inputs in the result
        step = api_number + member_id

        deductible = random.randrange(*self.deductible_interval, step)
        stop_loss = random.randrange(*self.stop_loss_interval, step)
        oop_max = random.randrange(*self.oop_max_interval, step)

        return f'{{"deductible": {deductible}, "stop_loss": {stop_loss}, "oop_max": {oop_max}}}'


if __name__ == "__main__":
    api_server = ApiServer((600, 3000),
                           (5077, 14045),
                           (3745, 7021))
    print(api_server.answer_client('https://api2.com?member_id=1'))
