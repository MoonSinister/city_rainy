from BaseModule.physical_environment import GeoGrid
import json

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


def main():
    # 示例数据（天津市范围内的点）
    pos = readsite()
    route0info = readroute(1)
    route0 = route0info['geometry']['coordinates']

    mygrid =GeoGrid
    #

    # 首先导入路网，将其转换为二维网格
    x,y = mygrid.map_to_grid(pos)

    mygrid.visualize_grid(x,y)

if __name__ == "__main__":
    main()