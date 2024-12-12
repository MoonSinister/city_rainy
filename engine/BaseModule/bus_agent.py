from typing import Tuple
from BaseModule.agent import Agent
from BaseModule.model import Model
from BaseModule.physical_environment import Position

class BusAgent(Agent):
    def __init__(self, unique_id: int, model: Model, bounds: Tuple[Tuple[float, float], Tuple[float, float]]) -> None:
        super().__init__(unique_id, model)
        self.bounds = bounds  # ((min_lat, max_lat), (min_lon, max_lon))

    def is_within_bounds(self, pos: Position) -> bool:
        """检查当前位置是否在指定范围内"""
        min_lat, max_lat = self.bounds[0]
        min_lon, max_lon = self.bounds[1]
        lat, lon = pos
        return min_lat <= lat <= max_lat and min_lon <= lon <= max_lon

    def move(self) -> None:
        """尝试移动到一个新的位置，并检查是否在范围内"""
        if self.pos is not None:
            new_lat = self.random.uniform(self.bounds[0][0], self.bounds[0][1])
            new_lon = self.random.uniform(self.bounds[1][0], self.bounds[1][1])
            new_pos = (new_lat, new_lon)
            if self.is_within_bounds(new_pos):
                self.pos = new_pos
                print(f"Moved to new position: {self.pos}")
            else:
                print("New position is out of bounds, staying at current position.")

    def step(self) -> None:
        print(f"Hi, I am a bus agent, ID: {str(self.unique_id)}.")
        self.move()
