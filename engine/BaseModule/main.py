from BaseModule.model import Model
from BaseModule.time import BaseScheduler
from BaseModule.physical_environment import Position
from BaseModule.agent_bus import BusAgent
from BaseModule.physical_environment import GeoGrid
import json
import warnings
from random import Random
warnings.simplefilter(action='ignore', category=FutureWarning)
model = Model()
def  get_agent():
    agent_list = []
    for i in range(30):
        myagent =BusAgent(unique_id=i, model=model)
        print(i)
        agent_list.append(myagent)
    return agent_list
def main():
    agent_list = get_agent()
    print(agent_list[0].name)
    timesch = BaseScheduler(model)
    for i in range(30):
        timesch.add(agent_list[i])


if __name__ == "__main__":
    main()
