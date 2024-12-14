import osmnx as ox
import matplotlib.pyplot as plt

# 定义城市名称并下载数据
city_name = "Tianjin, China"

# 获取城市的道路网络
# network_type 可以是 'all_private', 'all', 'bike', 'drive', 'drive_service', 'walk'
G = ox.graph_from_place(city_name, network_type='drive')

# 输出一些关于图的信息
stats = ox.basic_stats(G)
print(stats)

# 可视化路网
fig, ax = ox.plot_graph(G, node_size=0, edge_color='black', edge_linewidth=0.5)

# 如果需要保存图像
plt.savefig("tianjin_road_network.png", dpi=300)
