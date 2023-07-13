import numpy as np

exp = np.exp
PI = np.pi
sqrt = np.sqrt
ln = np.log
INF = float("inf")

def select(*args):
    '''Given probabilities, selects an event'''
    cum_prob = []
    previous_prob = 0
    for arg in args:
        cum_prob.append(previous_prob+arg)
        previous_prob+=arg
    x = np.random.random()*cum_prob[-1]
    for index, element in enumerate(cum_prob):
        if x<=element:
            return index
    return len(args)-1

def sigmoid(x, factor=1, scale=1):
    return factor/(1+exp(-x*scale))

OVERS = 20
TEAM_SIZE = 11


PITCH_DOT_FACTOR = 1.1
PITCH_BOUND_FACTOR = 1.2

HOME_TEAM_FACTOR = 1.1


WICKET_HEIGHT = 1
WICKET_WIDTH = 0.3214
WIDE_DIST = 0.5714

PLAYER_HEIGHT = 2.46
PLAYER_FIELDING = 0.8
PLAYER_RUNNING = 0.8
PLAYER_EXPERIENCE = 0.5
BOWL_MEAN = [0.4, 1]
BOWL_COV = [[0.08,0], [0,0.2]]
BATSMAN_BATTING = 0.9
BATSMAN_BOWLING = 0.2
BOWLER_BATTING = 0.5
BOWLER_BOWLING = 0.9 

TYPICAL_BAT_SCORE = {'dots':0.4, 'ones':0.25, "twos":0.15, "threes":0.05, "fours":0.1, "sixes":0.05}
BAT_SCORE_KEYS = ["dots", "ones", "twos", "threes", "fours", "sixes"]

BATTER_HEIGHT_STRIKING_LIMIT = 1.2

