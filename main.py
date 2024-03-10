import math
import random

from sim.strategies import Team, Strategies, create_formation
from sim.player import Player, Position
from sim.match import Match, MatchEvent

predef_formation = [
    (Position(-0.2, 0), Player.PlayerType.CENTER_FORWARD),
    (Position(-0.3, 0), Player.PlayerType.SECOND_STRIKER),
    (Position(-0.4, -0.5), Player.PlayerType.CENTRAL_MIDFIELDER),
    (Position(-0.4, 0.5), Player.PlayerType.CENTRAL_MIDFIELDER),
    (Position(-0.6, 0), Player.PlayerType.OTHER_DEFENSE),
    (Position(-0.8, 0), Player.PlayerType.GOALIE)
    ]

team1_players = create_formation(["Player A",
                                        "Player B",
                                        "Player C",
                                        "Player D",
                                        "Player E",
                                        "Player F",
                                       ], predef_formation)

team_1 = Team("Alpha", team1_players, Strategies.AttackStrategy(), Strategies.DefendStrategy(), -1)

team2_players = create_formation(["Player U",
                                        "Player V",
                                        "Player W",
                                        "Player X",
                                        "Player Y",
                                        "Player Z",
                                       ], predef_formation)

team_2 = Team("Beta", team2_players, Strategies.AttackStrategy(), Strategies.DefendStrategy(), -1)


# Simulate a match
def simulate_match(team1, team2):
    match = Match(team1, team2)
    return match.simulate()


# Run the simulation
events = simulate_match(team_1, team_2)
print(MatchEvent.events_to_printout(events))