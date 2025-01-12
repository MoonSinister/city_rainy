from flask import Flask, jsonify
import random
from flask_cors import CORS
from BaseModule.model import Model
from BaseModule.time import BaseScheduler
from BaseModule.physical_environment import Position
from BaseModule.agent_bus import BusAgent
from BaseModule.physical_environment import GeoGrid
import json
import csv
import warnings
from random import Random
warnings.simplefilter(action='ignore', category=FutureWarning)
model = Model()
count = 0
def readroute(id: int):
    with open('route_map/hexiroute.geojson', 'r', encoding='utf-8') as file:
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
def read_flood_points():
    """读取积水点数据"""
    flood_points = []
    with open('route_map/points.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            flood_points.append(row)
    return flood_points
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
    for i in range(230):
        routeinfo = readroute(i)
        if routeinfo['geometry']['type'] == 'LineString':
            route = routeinfo['geometry']['coordinates']
        else:
            route = routeinfo['geometry']['coordinates'][0]
        route_name = routeinfo['properties']['name']
        print(i)
        print(route[0])
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


app = Flask(__name__)
CORS(app)
agent = get_agent()
timesch = BaseScheduler(model)
for i in range(230):
    timesch.add(agent[i])
flood_points = read_flood_points()
@app.route('/get_data', methods=['GET'])
def get_data():
    #传入当前时间点agent位置
    posdata = []
    for i in range(230):
        posdata.append(agent[i].pos)

    time_h=0
    time_h = int(1+timesch.time/5)
    timesch.step()
    #传入当前时间点积水点数据，type4
    current_flood_points = []
    for point in flood_points:
        if point['type'] == '4':
            if time_h <= 16:
                depth = point[f'h{time_h:02d}']  # 根据当前小时获取对应深度数据
            else:
                time_h = 16
                depth = point[f'h{time_h:02d}']
            if float(depth) > 0:  # 仅返回有积水的数据
                current_flood_points.append({
                    'longitude': float(point['longitude']),
                    'latitude': float(point['latitude']),
                    'depth': float(depth)
                })


    return jsonify({"status": "success", "data": posdata,"flood_points": current_flood_points})
#


if __name__ == '__main__':
    app.run(debug=True,port=5000)
