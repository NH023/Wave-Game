class waveHandler():
    def __init__(self):
        self.currentRound = 0

    def nextRound(self):
        self.currentRound += 1
        """
        The round system will run with sets of predetermined spawn locations until stage 20(for now)
        """