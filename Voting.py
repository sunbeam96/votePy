
class Voting:
    myVote = ""
    def __init__(self, name, options):
        self.votingName = name
        self.votes = self.createVotingList(options)        

    def createVotingList(self):
        votingOptions = {}
        for option in votingOptions:
            self.votes["%s" % option] = "0"
        return votingOptions

