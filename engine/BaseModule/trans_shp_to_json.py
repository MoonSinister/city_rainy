import osmnx as ox
import geopandas as gpd

# 设置城市和道路类型
place_name = "Tianjin, China"
tags = {'highway': True}  # 选择所有类型的道路

# 下载道路数据
graph = ox.graph_from_place(place_name, network_type='all', custom_filter=tags)

# 转换为 GeoDataFrame
gdf = ox.graph_to_gdfs(graph, nodes=False, edges=True)

# 保存为 SHP 文件
gdf.to_file("tianjin_roads.shp")
def readroute(id: int):
    with open('./route_map/hexiroute.geojson', 'r', encoding='utf-8') as file:
        data = json.load(file)
    routename = data['features'][id]['properties']['name']
    route = data['features'][id]["geometry"]['coordinates']
    routetype = data['features'][id]["geometry"]['type']
    """ 公交线路经纬度 """
    return route, routename,routetype