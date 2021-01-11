
class Voting:
    myVote = ""
    def __init__(self):
        self.votingName = ""
        self.votes = {}        

    def createNewVoteOptionList(self, options):
        for option in options:
            self.votes["%s" % option] = "0"
