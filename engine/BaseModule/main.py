from BaseModule.model import Model
from BaseModule.time import BaseScheduler
from BaseModule.physical_environment import Position
from BaseModule.bus_agent import BusAgent
import json
from random import Random


def readroute(id: int):
    with open('route.geojson', 'r', encoding='utf-8') as file:
        data = json.load(file)
    routename = data['features'][id]['properties']

    route = data['features'][id]
    """ 公交线路经纬度 """
    return route
def main():
    model = Model()
    timesch=BaseScheduler(model)

    route0info = readroute(1)
    route0 = route0info['geometry']['coordinates']
    route0_name=route0info['properties']['name']
    agent0 = BusAgent(unique_id=1, model=model,route=route0,route_name=route0_name)

    timesch.add(agent0)



    for i in range(5):
        i=i+1
        timesch.step()




    # 输出初始化状态






if __name__ == "__main__":
    main()
