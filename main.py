from player import *
from match import *
import create

india = create.indian_team()
aus = create.australian_team()
hyderabad_pitch = Field(home_team=india)

match = Match(india, aus, hyderabad_pitch)
match.toss()
match.start_first_innings()
match.start_second_innings()

print(match.score_card())
print(match)
