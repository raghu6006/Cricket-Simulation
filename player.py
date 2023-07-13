from enum import Enum
import random
import constants
import numpy as np

class Country(Enum):
    IND = "INDIA"
    PAK = "PAKISTAN"
    AUS = "AUSTRALIA"
    SA = "SOUTH AFRICA"
    SL = "SRI LANKA"
    BAN = "BANGLADESH"
    ENG = "ENGLAND"
    NZ = "NEWZEALAND"

class PlayerType(Enum):
    BAT = 'BATTER'
    BOWL = 'BOWLER'
    KEEP = 'KEEPER'
    AR = 'ALL ROUNDER'

class Player():
    def __init__(self, name, country, playertype):
        self.name = name
        self.country = country
        self.type = playertype
        self.height = constants.PLAYER_HEIGHT
        self.fielding = constants.PLAYER_FIELDING
        self.running = constants.PLAYER_RUNNING
        self.experience = constants.PLAYER_EXPERIENCE
        self.bowling = constants.BATSMAN_BOWLING
        self.batting = constants.BATSMAN_BATTING
        self.bowl_mean = constants.BOWL_MEAN
        self.bowl_cov = constants.BOWL_COV
        self.batting_style = constants.TYPICAL_BAT_SCORE
        if self.type == PlayerType.BOWL:
            self.bowling = constants.BOWLER_BOWLING
            self.batting = constants.BOWLER_BATTING
    
    def __str__(self):
        return f"{self.name} from {self.country}"

    def set_values(self, height, bowling, batting, fielding, running, experience):
        self.height = height
        self.bowling = bowling
        self.batting = batting
        self.fielding = fielding
        self.running = running
        self.experience = experience

    def bowl(self):
        return np.random.multivariate_normal(self.bowl_mean, self.bowl_cov)
    
    def strike(self, xpos, ypos, bowler):
        striking = self.batting
        wide_limit = constants.WICKET_WIDTH + constants.WIDE_DIST

        if xpos<0:
            striking = striking*constants.exp(xpos)
        if xpos>wide_limit:
            striking = striking*constants.exp(wide_limit-xpos)
        
        height_limit = self.height*constants.BATTER_HEIGHT_STRIKING_LIMIT
        if ypos>height_limit:
            striking = striking*constants.exp(height_limit-ypos)
        
        striking*=(1-constants.exp(-bowler.bowling))
        return constants.select(striking, 1-striking)

    def bat(self, xpos, ypos, bowler, non_striker, field):
        striked = self.strike(xpos, ypos, bowler)
        wide_limit = constants.WICKET_WIDTH + constants.WIDE_DIST
        runs = 0
        wicket = False
        wide = False
        no_ball = False
        if not striked:
            if ypos<=1 and xpos<=constants.WICKET_WIDTH:
                wicket = True
            if xpos<0 or xpos>wide_limit:
                wide = True
            if ypos>self.height:
                no_ball = True
            return runs, wicket, wide, no_ball
        
        batting_prob = self.batting_style.copy()
        batting_prob["dots"]*= constants.sigmoid(bowler.bowling, factor=2)
        batting_prob["dots"]*= field.pitch_dot_factor
        running_factor = self.running + non_striker.running
        running_factor = constants.sigmoid(running_factor, factor=2)
        batting_prob["ones"]*= running_factor
        batting_prob["twos"]*=running_factor
        batting_prob["threes"]*=running_factor
        batting_prob["fours"]*= field.pitch_bound_factor
        batting_prob["sixes"]*= field.pitch_bound_factor

        if field.home_team:
            if self.country == field.home_team.country:
                batting_prob["fours"]*= constants.HOME_TEAM_FACTOR
                batting_prob["sixes"]*= constants.HOME_TEAM_FACTOR

        batting_probs=[batting_prob[key] for key in constants.BAT_SCORE_KEYS]

        runs = constants.select(*batting_probs)
        if runs==5:
            runs=6

        return runs, wicket, wide, no_ball


class Team():
    def __init__(self, country, players, captain=None):
        self.country = country
        self.players = players
        self.captain = captain
        self.bowlers = []
        self.batters = []
        self.keeper = None
        self.all_rounders = []
        self.batting_order = {}
        self.remaining_batters= constants.TEAM_SIZE

    def set_captain(self, captain):
        self.captain = captain

    def set_batting_order(self, batting_order):
        self.batting_order = batting_order

    def process_players(self):
        for player in self.players:
            if player.type == PlayerType.BAT:
                self.batters.append(player)
            elif player.type == PlayerType.BOWL:
                self.bowlers.append(player)
            elif player.type == PlayerType.KEEP:
                self.keeper = player
            elif player.type == PlayerType.AR:
                self.all_rounders.append(player)

    def send_bowler(self):
        return random.choice(self.bowlers+self.all_rounders)
    
    def send_batter(self):
        batter = self.batting_order[constants.TEAM_SIZE-self.remaining_batters]
        self.remaining_batters-=1
        return batter
    
    def __str__(self) -> str:
        return self.country.value



    

    