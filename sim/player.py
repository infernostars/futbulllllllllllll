import math
from enum import Enum, IntEnum
from typing import Optional

class Position:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def distance(self, position: "Position"):
        """
        Calculates the distance between the point you run this with and another point.
        :param position: The other point.
        :return: A numeric distance between the two points.
        """
        return math.sqrt((self.x-position.x)**2+(self.y-position.y)**2)


    def distance_line(self, point1: "Position", point2: "Position"):
        return (abs((point2.x-point1.x)*(point1.y-self.y)-(point1.x-self.x)*(point2.y-point1.y))/
                point1.distance(point2))

    def moveto(self, position: "Position", distance: float):
        if self.distance(position) < distance:
            self.x, self.y = position.x, position.y
        else:
            current_distance = self.distance(position)
            if current_distance != 0:  # Avoid division by zero
                deltax = (position.x - self.x) * (distance / current_distance)
                deltay = (position.y - self.y) * (distance / current_distance)
                self.x += deltax
                self.y += deltay

class Player:
    class PlayerType(IntEnum):
        GOALIE = 0
        OTHER_DEFENSE = 1
        OFFENSIVE_MIDFIELDER = 16
        DEFENSIVE_MIDFIELDER = 17
        CENTRAL_MIDFIELDER = 18
        SECOND_STRIKER = 32
        CENTER_FORWARD = 33

    def __init__(self, name: str, passing: int, shooting: int, stamina: int, position: Position, part: PlayerType):
        self.name = name
        self.base_passing = passing
        self.base_shooting = shooting
        self.max_stamina = stamina
        self.stamina = stamina
        self.possession_time = 0
        self.position = position
        self.part = part

    def __str__(self):
        return self.name

    def get_nearest_player(self, other_players: list["Player"]) -> Optional["Player"]:
        """
        Returns the nearest player from the list of other players.
        :param other_players: List of other players on the field.
        :return: The nearest player object.
        """
        if not other_players:
            return None

        nearest_player = other_players[0]
        min_distance = self.position.distance(nearest_player.position)

        for player in other_players[1:]:
            distance = self.position.distance(player.position)
            if distance < min_distance:
                min_distance = distance
                nearest_player = player

        return nearest_player

    def move(self):
        match self.part:
            case 0:
                pass
            case _:
                pass