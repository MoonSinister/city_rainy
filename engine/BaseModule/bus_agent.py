from typing import List, Tuple
from BaseModule.agent import Agent
from BaseModule.model import Model


class BusAgent(Agent):
    def __init__(self, unique_id: int, model: Model, route: List[Tuple[float, float]],route_name: str) -> None:
        super().__init__(unique_id, model)
        if not route:
            raise ValueError("Route cannot be empty.")
        self.route_name = route_name
        self.route = route
        self.current_index = 0
        self.pos = route[0]
        self.unique_id = unique_id

    def move(self) -> None:
        """沿路线行驶"""
        if self.current_index < len(self.route) - 1:
            self.current_index += 1
            self.pos = self.route[self.current_index]
            print(f"Moved to position {self.pos}.")
        else:
            print("Reached the end of the route. Cannot move further.")





    def step(self) -> None:
        print(f"Hi, I am a bus agent, ID: {str(self.route_name)}.")
        self.move()
