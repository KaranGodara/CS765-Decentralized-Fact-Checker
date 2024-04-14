class Link:
    # This class acts as communication link between voter and DApp
    def __init__(self, voter, DApp):
        self.voter = voter
        self.DApp = DApp

    # Function to send news to voter from DApp
    def send_news_to_voter(self, news):
        self.voter.put_news(news)

    # Function to send vote on news to DApp from voter
    def send_vote_to_DApp(self, news, vote):
        self.DApp.put_vote((news, vote, self.voter.ID))