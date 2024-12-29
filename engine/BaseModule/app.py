from flask import Flask, jsonify
import random
from flask_cors import CORS
from BaseModule.model import Model
from BaseModule.time import BaseScheduler
from BaseModule.physical_environment import Position
from BaseModule.bus_agent import BusAgent
from BaseModule.physical_environment import GeoGrid
import json
import warnings
from random import Random
warnings.simplefilter(action='ignore', category=FutureWarning)
model = Model()
count = 0
def readroute(id: int):
    with open('route.geojson', 'r', encoding='utf-8') as file:
        data = json.load(file)
    routename = data['features'][id]['properties']

    route = data['features'][id]
    """ 公交线路经纬度 """
    return route
def readsite():
    with open('site.geojson', 'r', encoding='utf-8') as file:
        data = json.load(file)
        index=0
        pos = []
        while index < len(data['features']):
            pos.append(data['features'][index]['geometry']['coordinates'])
            index=index+1
        return pos
def  get_agent():
    # pos = readsite()

    # mygrid = GeoGrid()
    #
    # # 首先导入路网，将其转换为二维网格
    # mygrid.add_path(pos)
    # x, y = mygrid.get_path()
    # mygrid.visualize_grid(x, y)

    # timesch=BaseScheduler(model)
    agent = []
    for i in range(30):
        routeinfo = readroute(i)
        route = routeinfo['geometry']['coordinates']
        route_name = routeinfo['properties']['name']
        agent.append(BusAgent(unique_id=i, model=model,route=route,route_name=route_name))
    return agent
        # timesch.add(agent[i])
        # mygrid.add_agent(agent[i])
    #
    # for i in range(1):
    #     i=i+1
    #     for j in range(30):
    #         data.append(agent[j].pos)
    #     timesch.step()
agent = get_agent()
timesch = BaseScheduler(model)
for i in range(30):
    timesch.add(agent[i])

app = Flask(__name__)
CORS(app)
@app.route('/get_data', methods=['GET'])
def get_data():

    data = []
    for i in range(30):
        data.append(agent[i].pos)
    timesch.step()
    print(data)
    return jsonify({"status": "success", "data": data})


if __name__ == '__main__':
    app.run(debug=True,port=5000)
