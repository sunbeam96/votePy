
class Voting:
    myVote = ""
    def __init__(self, name, options):
        self.votingName = name
        self.votingOptions = options
        self.votes = {}
        self.createVotingList()

    def createVotingList(self):
        for option in self.votingOptions:
            self.votes["%s" % option] = "0"

