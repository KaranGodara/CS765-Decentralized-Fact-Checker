import os

class Trustworthiness:
    def __init__(self, r, id):
        # Storing the voter id
        self.voter_ID = id

        # We store in the lifetime of the voter, number of correct and number of
        # incorrect votes casted by it
        self.num_correct = 0
        self.num_incorrect = 0

        # To update the rating, we increase a rating only when the voter correctly
        # votes for certain number of times, so to keep track of current net correct 
        # votes we use this variable
        self.net_correct_current = 0
        self.average_news_per_day = r
        self.curr_net_required = max(1, 0.1*self.average_news_per_day)

        # Starting the trust from minimum value of 1
        self.trustworthiness = 1

        self.min_trust = 1
        self.max_trust = 1000

        self.curr_max = 1000

    # function to help update the net correct votes required for further increase in
    # trustworthiness
    def set_new_net_required(self):
        # If current trustworthiness >= 551, need 10*average_news_per_day net votes
        # this helps in slow increase when already having high trustworthiness, to prevent
        # accumulation of voters with high trust scores
        if self.trustworthiness >= 551:
            self.curr_net_required = max(1, 10*self.average_news_per_day)
        # If current trustworthiness <= 50, need 0.1*average_news_per_day net votes
        # to increase trust, to intially fastly separate honest vs non-honest
        elif self.trustworthiness <= 50:
            self.curr_net_required = max(1, 0.1*self.average_news_per_day)
        # Remaining updates are in between the two extremes
        else:
            k = (self.trustworthiness - 1) / 50
            self.curr_net_required = max(1, k*self.average_news_per_day)

    # This function dynamically decides what is the max rating a voter can acheive based on his 
    # fraction of news correctly voted. We use this policy only when rating reaches atleast 501
    def update_curr_max(self):
        if self.trustworthiness >= 501:
            self.curr_max = int(((self.num_correct*1.0) / (self.num_correct + self.num_incorrect)) * self.max_trust)

            # To prevent sudden fall of some voter who luckily reached 501 but his fraction says he should
            # be below 500, hence we set curr_max as 501 for that case so that the voter doesn't fall but 
            # stays at 501
            if self.curr_max < 501:
                self.curr_max = 501
    
    # Update the trustworthiness if possible, when voter votes correctly 
    def mark_correct(self):
        # Updating the correct count, both global one and the one that is maintained at each rating
        self.net_correct_current += 1
        self.num_correct += 1

        # Seeing if rating could potentially increase
        if(self.curr_net_required <= self.net_correct_current):
            self.trustworthiness += 1
            self.update_curr_max()
            self.trustworthiness = min(self.curr_max, self.trustworthiness)
            
            # Getting ready for new rating level
            self.net_correct_current = 0
            self.set_new_net_required()

    # Update the trustworthiness if possible, when voter votes incorrectly 
    def mark_incorrect(self):
        self.net_correct_current -= 1
        self.num_incorrect += 1

        # Seeing if rating could potentially decrease
        if -self.curr_net_required >= self.net_correct_current :
            self.trustworthiness -= 1
            self.trustworthiness = max(self.min_trust, self.trustworthiness)

            # Getting ready for new rating level
            self.net_correct_current = 0
            self.set_new_net_required()

    # Function to print the current trustworthiness of the voter
    def print_trustworthiness(self, filename, curr_count):
        # Creating the directories in the path if not present already
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Writing the trustworthiness to the file
        with open(filename, 'a') as file:
            file.write(f"News Count : {curr_count}, Trust Value : {self.trustworthiness}\n")

    
