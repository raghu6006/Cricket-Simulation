from player import Country, PlayerType, Player, Team

def create_team(batter_names, bowler_names, country):
    players = []
    for batter_name in batter_names:
        batter = Player(batter_name, country, PlayerType.BAT)
        players.append(batter)
    for bowler_name in bowler_names:
        bowler = Player(bowler_name, country, PlayerType.BOWL)
        players.append(bowler)
    
    team = Team(country, players)
    team.set_batting_order(players)
    team.process_players()
    return team

def indian_team():
    batter_names = ["Rohit", "Gill", "Kohli", "Sky", "Shreyas", "Hardik"]
    bowler_names = ["Jadeja", "Ashwin", "Bhuvi", "Shami", "Bumrah"]
    country = Country.IND
    return create_team(batter_names, bowler_names, country)

def australian_team():
    batter_names = ["Warner", "Khawaja", "Marnus", "Smith", "Head", "Green"]
    bowler_names = ["Carey", "Cummins", "Lyon", "Starc", "Boland"]
    country = Country.AUS
    return create_team(batter_names, bowler_names, country)
    