import random
from enum import IntEnum
from typing import Optional

from sim.player import Player
from sim.strategies import MoveResult, Team
from sim.utility import an, list_english


class Move(IntEnum):
    """
    An enumeration of moves. Special moves can be defined by the Strategy being used, but the basic ones and WAIT
    should be used as expected.
    """
    WAIT = 0
    BASIC_GOAL = 1
    BASIC_PASS = 2
    SPECIAL0 = 128
    SPECIAL1 = 129
    SPECIAL2 = 130
    SPECIAL3 = 131
    SPECIAL4 = 132
    SPECIAL5 = 133
    SPECIAL6 = 134
    SPECIAL7 = 135


class MatchEvent:
    class EventKinds(IntEnum):
        NONE = 0
        PASS = 1
        INTERCEPT = 2
        GOAL = 3
        MISSED_GOAL = 4
        SPECIAL_MOVE = 64
        SPECIAL_MOVE_SCORE = 65
        MULTI_SPECIAL_MOVE = 96
        MULTI_SPECIAL_MOVE_SCORE = 97
        HALFTIME = 128
        END = 129
        ENTER_PENALTY = 130
        PENALTY = 131
        MISSED_PENALTY = 132
        VICTORY = 255

    class Info:
        def __init__(self, player: Optional[Player], other_player: Optional[Player], intercepting_player: Optional[Player],
                     score_team_1: Optional[int], score_team_2: Optional[int], special_move_name: Optional[str],
                     players_relevant: Optional[list[Player]], winning_team: Optional[Team]):
            self.player = player
            self.other_player = other_player
            self.intercepting_player = intercepting_player
            self.score_team_1 = score_team_1
            self.score_team_2 = score_team_2
            self.special_move_name = special_move_name
            self.players_relevant = players_relevant
            self.winning_team = winning_team

    def __init__(self, time: int, kind: "MatchEvent.EventKinds", info: Optional["MatchEvent.Info"]):
        self.time = time
        self.kind = kind
        self.info = info

    @classmethod
    def make_event(cls, move: Move, result: MoveResult, time: int, special_move_name: Optional[str]) -> "MatchEvent":
        '''
        Takes a move, its result, and the time it began and produces an event.
        :param time: The time the move happened, in seconds since the start of the match.
        :param move: What move occured.
        :param result: The MoveResult from that move.
        :param special_move_name: An optional string, for the name of a special move.
        :return: A MatchEvent for the move.
        '''
        pass

    @classmethod
    def events_to_printout(cls, ls) -> str:
        '''
        Turns a list of events into a printout.
        :param ls: The list of events to print.
        :return: A string of the events, seperated by newlines.
        '''
        return "\n".join([str(event) for event in ls])

    def get_message(self):
        match self.kind:
            case MatchEvent.EventKinds.NONE:
                pass
            case MatchEvent.EventKinds.PASS:
                return f"{self.info.player} passes to {self.info.other_player}"
            case MatchEvent.EventKinds.INTERCEPT:
                return f"{self.info.player} passes to {self.info.other_player}, but {self.info.intercepting_player} intercepts!"
            case MatchEvent.EventKinds.GOAL:
                return f"{self.info.player} goes for the goal and scores! The score is now {self.info.score_team_1} - {self.info.score_team_2}."
            case MatchEvent.EventKinds.MISSED_GOAL:
                return f"{self.info.player} goes for the goal and misses!"
            case MatchEvent.EventKinds.SPECIAL_MOVE:
                return f"{self.info.player} goes for {an(self.info.special_move_name)}!"
            case MatchEvent.EventKinds.SPECIAL_MOVE_SCORE:
                return f"{self.info.player} goes for {an(self.info.special_move_name)} and scores! The score is now {self.info.score_team_1} - {self.info.score_team_2}."
            case MatchEvent.EventKinds.MULTI_SPECIAL_MOVE:
                return f"{list_english(self.info.players_relevant)} go for {an(self.info.special_move_name)}!"
            case MatchEvent.EventKinds.MULTI_SPECIAL_MOVE_SCORE:
                return f"{list_english(self.info.players_relevant)} go for {an(self.info.special_move_name)} and scores! The score is now {self.info.score_team_1} - {self.info.score_team_2}."
            case MatchEvent.EventKinds.HALFTIME:
                return f"The game is now in halftime!"
            case MatchEvent.EventKinds.END:
                return f"The game is over!"
            case MatchEvent.EventKinds.ENTER_PENALTY:
                return f"The game is over, but we're tied! It's time for penalty kicks!"
            case MatchEvent.EventKinds.PENALTY:
                return f"{self.info.player} goes for the penalty kick and makes it! The score is now {self.info.score_team_1} - {self.info.score_team_2}."
            case MatchEvent.EventKinds.MISSED_PENALTY:
                return f"{self.info.player} goes for the penalty kick and misses!"
            case MatchEvent.EventKinds.VICTORY:
                return f"{self.info.winning_team.name} wins, with a score of {self.info.score_team_1} - {self.info.score_team_2}."

    def __str__(self): #display the event
        minutes = self.time // 60
        seconds = self.time % 60
        stringrep = f"{minutes}:{seconds:02d} - "
        stringrep += self.get_message()
        return stringrep

# idk gonna grab water rq
class Match:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.possession_player = random.choice(team1.players)
        self.time = 0
        self.match_length = 90*60
        self.winner = 0

    def simulate(self):
        events = []
        while self.time < self.match_length:
            events += self.do_time(5)
        events += self.check_win()
        return events

    def check_win(self):
        events = []
        if self.team1.score == self.team2.score:
            events += MatchEvent(self.time, MatchEvent.EventKinds.ENTER_PENALTY)
            events += self.do_penalty()
        else:
            if self.team1.score > self.team2.score:
                self.winner = self.team1
            else:
                self.winner = self.team2
        events += MatchEvent(self.match_length, MatchEvent.EventKinds.VICTORY, self.winner)
        return events

    def do_penalty(self):
        events = []
        def penalty_kick(offensive, defensive):
            return True #calculate odds of the penalty kick succeeding
        team_a = random.choice(self.team1,self.team2)
        team_b = self.team2 if team_a == self.team1 else self.team1
        kicks_a = 0
        kicks_b = 0
        for _ in range(5):
            kicks_a += penalty_kick(team_a,team_b)
            kicks_b += penalty_kick(team_b,team_a)
        if kicks_a > kicks_b:
            self.winner = team_a
        elif kicks_b > kicks_a:
            self.winner = team_b
        else:
            while True:
                if penalty_kick(team_a, team_b):
                    self.winner = team_a
                    break
                if penalty_kick(team_b, team_a):
                    self.winner = team_b
                    break
        return events

    def do_time(self,span):
        start = self.time
        events = []
        while self.time < start+span:
            turn = self.turn(self.time)
            self.time = turn.time
            events.append(turn)
            if self.time >= self.match_length/2:
                events.append(MatchEvent(self.time,MatchEvent.EventKinds.HALFTIME))
            if self.time >= self.match_length:
                events.append(MatchEvent(self.time,MatchEvent.EventKinds.END))
        return events

    def turn(self,time):
        offensive = self.possession_player.team
        defensive = self.team1 if self.team2 == offensive else self.team2
        move = offensive.strategy.pick_move(self.possession_player, offensive, defensive, defensive.defensive)
        result = offensive.strategy.calc_move(move, self.possession_player, offensive, defensive, defensive.defensive)
        self.possession_player = result.new_player
        if result.score_change: offensive.score += 1
        return MatchEvent.make_event(move, result, time+result.time)