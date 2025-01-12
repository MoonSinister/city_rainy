from BaseModule.model import Model
from BaseModule.time import BaseScheduler
from BaseModule.physical_environment import Position
from BaseModule.agent_bus import BusAgent
from BaseModule.physical_environment import GeoGrid
import json
import warnings
from random import Random
warnings.simplefilter(action='ignore', category=FutureWarning)

def readroute(id: int):
    with open('route_map/hexiroute.geojson', 'r', encoding='utf-8') as file:
        data = json.load(file)
    routename = data['features'][id]['properties']

    route = data['features'][id]
    """ 公交线路经纬度 """
    return route
def readsite():
    with open('route_map/hexisite.geojson', 'r', encoding='utf-8') as file:
        data = json.load(file)
        index=0
        pos = []
        while index < len(data['features']):
            pos.append(data['features'][index]['geometry']['coordinates'])
            index=index+1
        return pos
def main():
    pos = readsite()

    mygrid = GeoGrid()

    # 首先导入路网，将其转换为二维网格
    mygrid.add_path(pos)
    x, y = mygrid.get_path()
    mygrid.visualize_grid(x, y)
    # model = Model()
    # timesch=BaseScheduler(model)
    # agent = []
    # for i in range(30):
    #     routeinfo = readroute(i)
    #     route = routeinfo['geometry']['coordinates']
    #     route_name = routeinfo['properties']['name']
    #     agent.append(BusAgent(unique_id=i, model=model,route=route,route_name=route_name))
    #     timesch.add(agent[i])
    #     mygrid.add_agent(agent[i])
    #
    # for i in range(1):
    #     i=i+1
    #     timesch.step()




    # 输出初始化状态






if __name__ == "__main__":
    main()
