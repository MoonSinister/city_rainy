from typing import List, Tuple
from BaseModule.agent import Agent
from BaseModule.model import Model


class PolicyAgent(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)

        self.current_index = 0

        self.unique_id = unique_id



    def step(self) -> None:
        print(f"Hi, I am a policy agent, ID: {str(self.route_name)}.")

