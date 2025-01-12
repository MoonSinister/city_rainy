import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# 读取 Shapefile 文件
gdf = gpd.read_file('./route_map/河西站点.shp', encoding='gbk')

# 检查并设置 CRS（如果没有设置 CRS）
if gdf.crs is None:
    gdf.set_crs('EPSG:4326', inplace=True)

bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
min_lon, min_lat, max_lon, max_lat = bounds
#
# print(f"经纬度范围:")
# print(f"最小经度 (min_lon): {min_lon}")
# print(f"最小纬度 (min_lat): {min_lat}")
# print(f"最大经度 (max_lon): {max_lon}")
# print(f"最大纬度 (max_lat): {max_lat}")
# # 打印前几行数据
print(gdf.head())

# 自定义地图样式并绘制
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color='blue', edgecolor='black', linewidth=0.5)
plt.title('Custom Map Style')
plt.show()

# 将数据保存为 GeoJSON 文件
gdf.to_file("tianjinsite.geojson", driver='GeoJSON')
