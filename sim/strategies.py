import abc
from abc import ABC
import random

from sim.player import Player, Position
from sim.match import Move

class MoveResult:
    """
    Represents the result after a move.
    """
    def __init__(self, score_change: bool, time_change: int = 1, new_player: Player | None = None,):
        self.score_change = score_change
        self.new_player = new_player
        self.time_change = time_change

    @classmethod
    def nothing(self,time):
        return MoveResult(False, time, None)


class DefensiveStrategy(ABC):
    pass

class OffensiveStrategy(ABC):
    @abc.abstractmethod
    def pick_move(self, possession_player: Player, possession_team: "Team", opposing_team: "Team",
                  opposing_strat: DefensiveStrategy) -> Move:
        """
        When you subclass this, you should make sure that you return the move you want to do! [Moves enum]
        :param possession_player: The possession player on your team.
        :param possession_team: Your team.
        :param opposing_team: The opposing team.
        :param opposing_strat: The opposing team's strategy. Try to minimize your usage of this.
        :return: a Move that this strategy wants to play.
        """
        ...


    @abc.abstractmethod
    def calc_move(self, move: Move, possession_player: Player, possession_team: "Team",
                  opposing_team: "Team", opposing_strat: DefensiveStrategy) -> MoveResult:
        """
        :param move:
        :param possession_player:
        :param possession_team:
        :param opposing_team:
        :param opposing_strat:
        :return: a MoveReturn, signifying what happened during the move.
        """
        ...

class Team:
    def __init__(self, name: str, players: list[Player], offense: OffensiveStrategy, defense: DefensiveStrategy, side: int):
        self.name = name
        self.players = players
        self.offense = offense
        self.defense = defense
        self.score = 0
        self.side = side #either -1 or 1

    def add_score(self, score: int):
        self.score += score

    def change_offensive_strategy(self, new_strat: OffensiveStrategy):
        self.offense = new_strat

    def change_defensive_strategy(self, new_strat: DefensiveStrategy):
        self.defense = new_strat

    def get_opposing_goal(self):
        return Position(-self.side, random.uniform(0.4,0.6))

# -- specific strategies --

class Strategies:

    class AttackStrategy(OffensiveStrategy):
        def __init__(self):
            self.special_names = ["long goal"]
        def pick_move(self, possession_player: Player, possession_team: "Team", opposing_team: "Team",
                      opposing_strat: DefensiveStrategy) -> Move:
            return random.choice([Move.WAIT,Move.BASIC_GOAL,Move.BASIC_PASS,Move.SPECIAL1])
        def calc_move(self, move: Move, possession_player: Player, possession_team: "Team",
                      opposing_team: "Team", opposing_strat: DefensiveStrategy) -> MoveResult:
            match move:
                case Move.WAIT:
                    return MoveResult.nothing(random.randint(15,30))
                case Move.BASIC_PASS:
                    return random.random() < (possession_player.base_passing)/100
                case Move.BASIC_GOAL:
                    return random.random() < (possession_player.base_shooting)/100
                case Move.SPECIAL1:
                    return True

    class FastStrategy(OffensiveStrategy):
        def pick_move(self, possession_player: Player, possession_team: "Team", opposing_team: "Team",
                      opposing_strat: DefensiveStrategy) -> Move:
            pass
        def calc_move(self, move: Move, possession_player: Player, possession_team: "Team",
                      opposing_team: "Team", opposing_strat: DefensiveStrategy) -> MoveResult:
            pass

    class SlowStrategy(OffensiveStrategy):
        def pick_move(self, possession_player: Player, possession_team: "Team", opposing_team: "Team",
                      opposing_strat: DefensiveStrategy) -> Move:
            pass
        def calc_move(self, move: Move, possession_player: Player, possession_team: "Team",
                      opposing_team: "Team", opposing_strat: DefensiveStrategy) -> MoveResult:
            pass

    class DefendStrategy(DefensiveStrategy):
        ...
    class UnifiedStrategy(DefensiveStrategy):
        ...

    class ManToManStrategy(DefensiveStrategy):
        ...

#utility

def create_player(name, position, type):
    return Player(name, random.randint(60, 100), random.randint(60, 100), random.randint(60,100), position, type)

def create_formation(names, formation):
    players = []
    for idx, name in enumerate(names):
        players.append(create_player(name,formation[idx][0],formation[idx][1]))
    return players