from trust import Trustworthiness
from voter import Voter
import simpy

class DApp : 
    def __init__(self, r, N, q, p, data_dir, env):
        # Number of news coming in day to the App, in real life this can
        # be calculated by using slow(or fast) moving averages.
        # But for the sake of simulation we assume it to be a constant throughout
        self.average_news_per_day = r

        self.env = env

        # Number of voters in the system
        self.N = N

        # Directory to store the data of simulation
        self.data_dir = data_dir

        # Trustworthiness of each voter, storred as a dictionary
        self.trustworthiness = dict()
        for id in range(self.N):
            self.trustworthiness[id] = Trustworthiness(self.average_news_per_day, id)

        # Queue to get the request for verification of news in DApp
        self.news_queue = simpy.Store(env)

        # Queue to get votes on the news
        self.vote_queue = simpy.Store(env)

        # Dictionary to store links to voters
        self.voter_links = dict()

        # Dictionary to store temporarily votes of news on whom decision is not yet taken
        self.votes_on_news = dict()
        self.votes_count_news = dict() 

        # Keeping a count of number of news on which decision has been made
        self.num_news = 0

        # To keep track of news voted fake or correct
        self.real_news = 0
        self.fake_news = 0

    def put_news(self, news):
        # Adding new news to news_queue to make it available for voting
        self.news_queue.put(news)

    def put_vote(self, vote):
        # Adding votes to vote_queue to receieve votes from voters on news
        self.vote_queue.put(vote)

    def set_new_link(self, link, id):
        # Setting the link to voter "id"
        self.voter_links[id] = link

    def get_news(self):
        # Function to receive new news, mark them to start voting procedure and send them to 
        # voters to get votes
        while True:
            # Receving the news
            news = yield self.news_queue.get()
            # print(f"DApp : Got news with ID {news} at {self.env.now}")

            # Making news ready to get votes, -1 indicates vote not yet received
            self.votes_on_news[news] = [-1 for _ in range(self.N)]
            self.votes_count_news[news] = 0

            # Sending this news to all voters to vote on it
            for id in range(self.N):
                # print(f"DApp : Sending news {news} to voter {id}")
                self.voter_links[id].send_news_to_voter(news)

    def make_decision_on_news(self, news):
        # Note for simulation every new's correct result is 1 and hence
        # malicious voters always vote 0, where honest voters with probability
        # 0.9 or 0.7, 1
        # print(f"Making decision on news with ID {news} at {self.env.now} ")

        # This stores the total votes saying news is correct (ie vote 1)
        votes_received = 0

        # This stores total votes possible on any decision
        max_votes = 0

        # Iterating through votes and calculating weighted votes
        for i in range(self.N):
            votes_received += self.votes_on_news[news][i]*self.trustworthiness[i].trustworthiness
            max_votes += self.trustworthiness[i].trustworthiness

        # If votes_received are greater than equal to half of max, we say news is correct
        # Else news is fake
        news_voted = 0
        if max_votes / 2.0 <= votes_received :
            # Appropriately modifying 
            news_voted = 1

        if news_voted == 0:
            self.fake_news += 1
        else:
            self.real_news += 1

        # Marking that the news has been decided fake or not
        self.num_news += 1

        # Appropriately updating the trustworthiness of voters based on the decision
        # Also printing the current value of trust in a file for plotting purposes
        for i in range(self.N):
            if self.votes_on_news[news][i] == news_voted:
                self.trustworthiness[i].mark_correct()
            else:
                self.trustworthiness[i].mark_incorrect()

            # printing the data to the file
            self.trustworthiness[i].print_trustworthiness(f"{self.data_dir}/trust_{i}", self.num_news)

        # Removing the temporary data associated with the news
        del self.votes_on_news[news]
        del self.votes_count_news[news]
            
    
    def register_vote(self, vote):
        # This function process the vote received in the vote queue
        news = vote[0]
        voter_id = vote[2]
        voter_vote = vote[1]
        self.votes_on_news[news][voter_id] = voter_vote
        self.votes_count_news[news] += 1

        # If all the voters have voted, we make a decision on the news cause no
        # more votes would be coming now
        if self.votes_count_news[news] == self.N:
            self.make_decision_on_news(news)
    
    def get_votes(self):
        # Function to receive votes from the voters on some news
        while True:
            # Receving the news
            vote = yield self.vote_queue.get()

            # Registering the news
            self.register_vote(vote)

            





        