import geopandas as gpd
from shapely.geometry import Point

import matplotlib.pyplot as plt
# 创建一个空的GeoDataFrame

gdf = gpd.read_file('河西线路.shp',encoding = 'gbk')




print(gdf.head())
"""
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color='blue', edgecolor='black', linewidth=0.5)
plt.title('Custom Map Style')
plt.show()
"""
gdf.to_file("hexiroute.geojson", driver='GeoJSON')
