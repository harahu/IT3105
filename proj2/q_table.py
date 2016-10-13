import random

class qTable:
    """
    Implements a table tracking the estimated values
    for state action pairs in an MDP.
    """
    def __init__(self, nS, nA):
        self.nS = nS
        self.nA = nA
        self.table = [[0 for i in range(nA)] for j in range(nS)]

    def getQ(self, s, a):
        return(self.table[s][a])

    def setQ(self, s, a, value):
        self.table[s][a] = value

    def getMaxQ(self, s):
        """
        Returns the highest Q-value
        for a given state.
        """
        return max(self.table[s])

    def getMaxQAction(self, s):
        """
        Returns a random action that has the highest Q-value
        for a given state.
        """
        max_q = self.getMaxQ(s)
        all_actions = [i for i, x in enumerate(self.table[s]) if x == max_q]
        return random.choice(all_actions)
