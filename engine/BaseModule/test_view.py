import requests
import json
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString

# 读取 JSON 数据
with open('road_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 获取所有节点 ID
node_ids = set()  # 用 set 来避免重复的节点 ID
for element in data['elements']:
    if element['type'] == 'way':
        node_ids.update(element['nodes'])

# 根据 node_ids 获取节点的经纬度
# 构造 Overpass API 查询来获取节点数据
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = f"""
[out:json];
node({','.join(map(str, node_ids))});
out body;
"""
response = requests.get(overpass_url, params={'data': overpass_query})

# 检查请求是否成功
if response.status_code != 200:
    print(f"请求失败，状态码: {response.status_code}")
    exit()

# 获取所有节点的经纬度
nodes_data = response.json()
node_coords = {node['id']: (node['lat'], node['lon']) for node in nodes_data['elements']}

# 提取道路的几何数据
features = []
for element in data['elements']:
    if element['type'] == 'way':
        coords = [node_coords[node_id] for node_id in element['nodes'] if node_id in node_coords]
        if coords:
            line = LineString(coords)  # 创建 LineString 对象
            features.append({
                'geometry': line,
                'properties': element  # 可以提取更多属性
            })

# 创建 GeoDataFrame
gdf = gpd.GeoDataFrame(features)

# 设置投影（WGS84 坐标系）
gdf.crs = "EPSG:4326"  # 设置为 WGS84 坐标系统（经纬度）

# 可视化
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color='blue', linewidth=0.5)

# 设置图形标题
ax.set_title("Road Network Visualization", fontsize=16)

# 显示地图
plt.show()
