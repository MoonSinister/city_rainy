from typing import List, Tuple
from BaseModule.agent import Agent
from BaseModule.model import Model
from pyproj import Proj, transform
import numpy as np
from scipy.sparse import lil_matrix
from scipy.io import mmwrite, mmread
import json

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
        self.backward = 0 #到达终点后返程

    def readsite(self):
        with open('site.geojson', 'r', encoding='utf-8') as file:
            data = json.load(file)
            index = 0
            pos = []
            while index < len(data['features']):
                pos.append(data['features'][index]['geometry']['coordinates'])
                index = index + 1
            return pos


    def move_by_route_back(self) -> None:
        if self.current_index > 0:
            self.current_index -= 1
            self.pos = self.route[self.current_index]
        else:
            print("Reached the end of the route. go front.")
            self.backward = 0
    def move_by_route_front(self) -> None:
        """沿路线行驶"""
        if self.current_index < len(self.route) - 1 :
            self.current_index += 1
            self.pos = self.route[self.current_index]
            # print(f"Moved to position {self.pos}.")
        else:
            print("Reached the end of the route. go back.")
            self.backward = 1


    def stop_for_site(self) -> None:
        #行驶到站点附近后停靠
        site = self.readsite()
        proj_in = Proj(init='epsg:4326')  # WGS84
        proj_out = Proj(init='epsg:32650')  # UTM Zone 50N
        grid_size = 10
        latitudes = [point[0] for point in site]
        longitudes = [point[1] for point in site]
        y_coords,x_coords = transform(proj_in, proj_out, latitudes, longitudes)
        agent_y,agent_x = transform(proj_in, proj_out, self.pos[0], self.pos[1])
        x_coords = np.array(x_coords)
        y_coords = np.array(y_coords)
        x_min = min(min(x_coords),agent_x)
        y_min = min(min(y_coords),agent_y)
        site_x = ((x_coords - x_min) / grid_size).astype(int)
        site_y = ((y_coords - y_min) / grid_size).astype(int)
        pos_x = ((agent_x - x_min) / grid_size).astype(int)
        pos_y = ((agent_y - x_min) / grid_size).astype(int)

        grid_x_size = max(max(site_x),pos_x) + 1
        grid_y_size = max(max(site_y),pos_y) + 1
        site_grid = np.zeros((grid_x_size, grid_y_size),dtype=int)
        for x, y in zip(site_x, site_y):
            site_grid[x, y] = 1  #
        # print(type(site_grid[0, 0]))
        #将站点存入网格，并且将agent当前位置转化成网格形式，只需要判定agent指定的格是否为1即可

        # np.savetxt('matrix.txt', site_grid, fmt='%d',delimiter=',')
        # np.savetxt('matrix.csv', site_grid, delimiter=',')
        if site_grid[0][0] == 1:
            print('Get to a site,stop for a while')
            self.pos = self.route[self.current_index]
        else:
            self.move_by_route_front()




    def step(self) -> None:
        global backward
        if self.backward == 0:
             # print(f"Hi, I am a bus agent, ID: {str(self.route_name)}.")
            self.move_by_route_front()
             # self.stop_for_site()
        else:
            self.move_by_route_back()
