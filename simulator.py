import simpy
from dapp import DApp
from voter import Voter
from link import Link

class Simulator:
    def __init__(self, r, N, q, p, data_dir, env):
        self.r = r
        self.N = N
        self.q = q
        self.p = p
        self.data_dir = data_dir
        self.env = env

    def setup_env(self):
        # Making the DApp for this system
        self.DApp = DApp(self.r, self.N, self.q, self.p, self.data_dir, self.env)

        # Making the voters for this system
        self.voters = dict()

        ######## For Malicious strategy 3 ##############
        # cnt = 0
        ################################################

        for id in range(self.N):
            # Initialising the voters
            self.voters[id] = Voter(id, self.q, self.p, self.env)

            ######## For Malicious strategy 3 ##############
            # if cnt < 125 and self.voters[id].honest == 1:
            #     cnt += 1
            #     self.voters[id].mark_vote_changer()
            #     print(f"Changed personality for {id}")
            ################################################

            # Printing initial info about each voter
            self.voters[id].print_info(f"{self.data_dir}/trust_{id}")

            # Creating the link between voter and DApp
            voter_link = Link(self.voters[id], self.DApp)
            self.DApp.set_new_link(voter_link, id)
            self.voters[id].set_link_to_DApp(voter_link)

    def news_generator(self):
        # This function would continously after some fixed gap, generate news for DApp
        news_ID = 0
        time_bw_news = 10
        while True:
            # print(f"News with ID {news_ID} generated at {self.env.now} ")
            self.DApp.put_news(news_ID)
            news_ID += 1
            yield self.env.timeout(time_bw_news)

    def my_timer(self):
        while True:
            print("Current time is :", self.env.now)
            yield self.env.timeout(100)

    def start_simulation(self):
        # Starting the simulation

        # Starting the DApp
        self.env.process(self.DApp.get_news())
        self.env.process(self.DApp.get_votes())

        # Starting the voters
        for i in range(self.N):
            self.env.process(self.voters[i].get_news_to_vote())

        # Finally, starting the news generation process
        self.env.process(self.news_generator())
        self.env.process(self.my_timer())