from player import *
from constants import INF, OVERS

class Field:
    def __init__(self, home_team, dot_factor = 1, bound = 1):
        self.pitch_dot_factor = dot_factor
        self.pitch_bound_factor = bound
        self.home_team = home_team


class BatScoreCard:
    '''Score of a Batsman'''
    def __init__(self, player):
        self.player = player
        self.bowledBy = None
        self.score = 0
        self.yet_to_bat = True

    def updateScore(self, runs, bowler, wicket):
        self.score+=runs
        if wicket:
            self.bowledBy = bowler

    def __str__(self):
        if self.yet_to_bat:
            return f"{self.player.name} not batted yet."
        elif self.bowledBy:
            return f"{self.player.name} scored {self.score} and bowled by {self.bowledBy.name}"
        return f"{self.player.name} currently batting at {self.score}."


class BowlScoreCard:
    '''Wickets, overs by a bowler'''
    def __init__(self, player):
        self.player = player
        self.overs_bowled = 0
        self.balls_bowled = 0
        self.wickets = 0
        self.runs_given = 0

    def updateScore(self, runs, wicket, extra_ball=False):
        self.runs_given+= runs
        if wicket:
            self.wickets+=1
        if extra_ball:
            self.balls_bowled-=1
        self.balls_bowled+=1
        if self.balls_bowled==6:
            self.overs_bowled+=1
            self.balls_bowled=0
    
    def __str__(self):
        return f"{self.player.name} bowled {self.overs_bowled}.{self.balls_bowled} overs and took {self.wickets} wickets"


class ScoreCard:
    ''' Stores the scorecard of an innings'''
    def __init__(self):
        self.bat = {}
        self.bowl = {}


class Innings:
    '''Manages the 2 teams and simulates the play'''
    def __init__(self, batting_team, bowling_team):
        self.batting_team = batting_team
        self.bowling_team = bowling_team
        self.score = 0
        self.wickets = 0
        self.balls = 0
        self.overs = 0
        self.striker = None
        self.non_striker = None
        self.bowler = None
        self.score_card = ScoreCard()

    def get_batter(self):
        return self.batting_team.send_batter()
    
    def get_bowler(self):
        return self.bowling_team.send_bowler()
    
    def terminate(self, target):
        if self.wickets==constants.TEAM_SIZE-1 or self.overs==OVERS or self.score>target:
            return True
        return False
    
    def initialise_score_card(self):
        for player in self.batting_team.players:
            self.score_card.bat[player] = BatScoreCard(player)
        for player in self.bowling_team.bowlers+self.bowling_team.all_rounders:
            self.score_card.bowl[player] = BowlScoreCard(player)

    def initialise_players(self):
        self.striker = self.get_batter()
        self.non_striker = self.get_batter()
        self.bowler = self.get_bowler()

        self.score_card.bat[self.striker].yet_to_bat = False
        self.score_card.bat[self.non_striker].yet_to_bat = False

    def initialise(self):
        self.initialise_score_card()
        self.initialise_players()
    
    def updateScore(self, runs, wicket=False, extra_ball=False):
        self.score+=runs
        if wicket:
            self.wickets+=1
        if extra_ball:
            self.balls-=1
        self.balls+=1
        if self.balls==6:
            self.overs+=1
            self.balls=0
        self.score_card.bat[self.striker].updateScore(runs, self.bowler, wicket)
        self.score_card.bowl[self.bowler].updateScore(runs, wicket, extra_ball)

    def simulate_bowl_bat(self, field):
        '''Simulates the delivery'''
        xpos, ypos = self.bowler.bowl()
        return self.striker.bat(xpos, ypos, self.bowler, self.non_striker, field)
    
    def deliver_ball(self, target, field, prev_no_ball=False):
        '''Delivers a ball and takes care of the updates'''
        if self.terminate(target):
            return 
        
        extra_ball = False

        runs, wicket, wide, no_ball = self.simulate_bowl_bat(field)
        #Proper
        if no_ball or prev_no_ball:
            wicket = False
        if no_ball or wide:
            extra_ball = True

        self.updateScore(runs+(no_ball or wide), wicket, extra_ball)

        if wicket:
            if self.terminate(target):
                return
            self.striker = self.get_batter()
            self.score_card.bat[self.striker].yet_to_bat = False

        if runs%2==1:
            self.striker, self.non_striker = self.non_striker, self.striker

        if self.balls==0 and not extra_ball:
            self.bowler = self.get_bowler()
            self.striker, self.non_striker = self.non_striker, self.striker

        if no_ball:
            self.deliver_ball(target, field, prev_no_ball=True)
        if wide:
            self.deliver_ball(target, field)

    def start_innings(self, field, target=INF):
        while not self.terminate(target):
            self.deliver_ball(target, field)

    def get_scorecard(self):
        summary=f"{self.batting_team.__str__()}"+"\n"
        for player in self.batting_team.batting_order:
            summary+=self.score_card.bat[player].__str__()+"\n"
        summary+=f"{self.bowling_team.__str__()}"+"\n"
        for row in self.score_card.bowl.values():
            summary+=row.__str__()+"\n"
        return summary

    def __str__(self):
        summary = f"Batting team:{self.batting_team.country.value}"
        summary+= "\n "
        summary+= f"Bowling team:{self.bowling_team.country.value}"
        summary+= "\n "
        summary+= f"Runs:{self.score}, Wickets:{self.wickets}, Overs:{self.overs}.{self.balls}"
        return summary

class Umpire:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

    def toss(self):
        toss_won_team =  random.choice([self.team1, self.team2])
        toss_lost_team = self.team1
        if toss_won_team == self.team1:
            toss_lost_team = self.team2
        return toss_won_team, toss_lost_team


class Match:
    def __init__(self, team1, team2, field):
        self.team1 = team1
        self.team2 = team2
        self.field = field
        self.innings1 = None
        self.innings2 = None
        self.umpire = Umpire(team1, team2)

    def toss(self):
        toss_won_team, toss_lost_team = self.umpire.toss()

        self.innings1 = Innings(toss_won_team, toss_lost_team)
        self.innings2 = Innings(toss_lost_team, toss_won_team)

    def start_first_innings(self):
        self.innings1.initialise()
        self.innings1.start_innings(field=self.field)

    def start_second_innings(self):
        self.innings2.initialise()
        self.innings2.start_innings(field=self.field, target=self.innings1.score)

    def score_card(self):
        '''Returns the Score card'''
        summary= "                 SCORE CARD              "
        summary+="\n \n "
        summary+= "               INNINGS 1               "
        summary+="\n"
        summary+=self.innings1.get_scorecard()
        summary+="\n \n"
        summary+= "               INNINGS 2               "
        summary+="\n"
        summary+=self.innings2.get_scorecard()
        return summary

    def __str__(self):
        summary= "               INNINGS 1               "
        summary+="\n"
        summary+=self.innings1.__str__()
        summary+="\n"
        summary+= "               INNINGS 2               "
        summary+="\n"
        summary+=self.innings2.__str__()
        summary+="\n"

        if self.innings1.score==self.innings2.score:
            summary+="         Match tied"
        elif self.innings1.score>self.innings2.score:
            summary+=f"{self.innings1.batting_team.__str__()} won by {self.innings1.score-self.innings2.score} runs"
        else:
            summary+=f"{self.innings1.bowling_team.__str__()} won by {10-self.innings2.wickets} wickets"
        return summary
            

    
