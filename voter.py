import random
import simpy
import os

class Voter:
    def __init__(self, ID, q, p, env):
        self.ID = ID
        self.honest = self.generate_RV(1-q)

        # By default, setting being correct probability as 0. That is assuming voter is malicious
        self.correct_prob = 0

        
        ##################### USEFUL FOR MALICIOUS STRATEGY 1 ########################
        # If voter is honest, need to change the probability of being correct
        if self.honest == 1:
            # With probability p, making honest people 90% correct
            # and with sprobability 1-p, making remaining honest people 70% correct 
            is_more_correct = self.generate_RV(p)
            self.correct_prob = is_more_correct*0.9 + (1-is_more_correct)*0.7
        ##############################################################################
        

        # Making the queue that would get news to vote on
        self.news_queue = simpy.Store(env)

        self.env = env

        ##################### USEFUL FOR MALICIOUS STRATEGY 2 ########################
        # # Idea is to initially assume malicious people vote correctly to gain trust and 
        # # then start lying. We will make them start lying after half the simulation time
        # # NOTE : Need above correct_prob changes too
        # is_more_correct = self.generate_RV(p)
        # self.correct_prob = is_more_correct*0.9 + (1-is_more_correct)*0.7
        # self.num_voted = 0
        ##############################################################################


        ##################### USEFUL FOR MALICIOUS STRATEGY 3 ########################
        # Idea is initially voters as selected during setup would behave as honest or
        # malicious, then at half time of simulation, some honest miners would also
        # turn into malicious voters. 
        # if self.honest == 1:
        # # With probability p, making honest people 90% correct
        # # and with probability 1-p, making remaining honest people 70% correct 
        #   is_more_correct = self.generate_RV(p)
        #   self.correct_prob = is_more_correct*0.9 + (1-is_more_correct)*0.7
        # self.num_voted = 0
        # self.change_personality = 0
        ##############################################################################


    def set_link_to_DApp(self, link):
        # Link to DApp for communication
        self.link_to_DApp = link

    # Helper Function : Generating 1 with probability z and 0 otherwise
    def generate_RV(self, z):
        sample = random.random()
        if sample < z:
            return 1
        else:
            return 0

    def mark_vote_changer(self):
        self.change_personality = 1
    
    # Function that would decide what the voter is gonna vote for the current news
    def cast_vote(self):
        ########################## Malicious strategy 1 #############################
        # If voter is malicious, the vote is always gonna be 0. Whereas for honest this is
        # 1 with prob either 0.9 or 0.7 based on type of honest voter
        return self.generate_RV(self.correct_prob)
        ##############################################################################

        ########################## Malicious strategy 2 #############################
        # self.num_voted += 1
        # if self.num_voted > 6000:
        #     if self.honest:
        #         return self.generate_RV(self.correct_prob)
        #     else:
        #         return 0
        
        # else:
        #     return self.generate_RV(self.correct_prob)
        ##############################################################################

        ########################## Malicious strategy 3 #############################
        # self.num_voted += 1
        # if self.num_voted > 6000:
        #     if self.honest and self.change_personality == 1:
        #         return 0
        #     else:  
        #         return self.generate_RV(self.correct_prob)
        # else:
        #     return self.generate_RV(self.correct_prob)
        ##############################################################################



    # Function used by link, which would allow it to add news for voter to vote
    def put_news(self, news):
        self.news_queue.put(news)

    # Function to get news to vote on and then vote on it using helper function cast_vote
    def get_news_to_vote(self):
        while True:
            # Here we would receive news to vote as they come
            news = yield self.news_queue.get()
            # print(f"Voter : Got news with ID {news} at {self.env.now}")


            # Deciding the vote
            vote = self.cast_vote()

            self.link_to_DApp.send_vote_to_DApp(news, vote)

    # Function to print the type and ID of the voter
    def print_info(self, filename):
        # Creating the directories in the path if not present already
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Writing the trustworthiness to the file, 
        with open(filename, 'w') as file:
            file.write(f"Agent ID : {self.ID}\n")
            if self.honest == 1:
                file.write(f"Agent Type : Honest\n")
            else:
                file.write(f"Agent Type : Malicious\n")
            file.write(f"Correctness Probability : {self.correct_prob}\n")
            file.write("\nTrustwothiness Measure : \n")



            
