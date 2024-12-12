import geopandas as gpd
from shapely.geometry import Point

import matplotlib.pyplot as plt
# 创建一个空的GeoDataFrame

gdf = gpd.read_file('天津_站点.shp',encoding = 'utf-8')




print(gdf.head())
"""
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color='blue', edgecolor='black', linewidth=0.5)
plt.title('Custom Map Style')
plt.show()
"""
gdf.to_file("site.geojson", driver='GeoJSON')
