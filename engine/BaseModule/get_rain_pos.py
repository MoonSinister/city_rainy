import pandas as pd
import json  # 用于处理 JSON 数据

def extract_coordinates(file_path, output_file):
    # 读取 CSV 文件
    df = pd.read_csv(file_path)

    # 过滤 type 为 4 的行
    filtered_df = df[df["type"] == 4]

    # 检查 h01 到 h12 是否存在非零值
    h_columns = [f"h{str(i).zfill(2)}" for i in range(1, 13)]
    filtered_df = filtered_df[(filtered_df[h_columns] != 0).any(axis=1)]

    # 提取经纬度并转换为列表格式
    coordinates = filtered_df[["longitude", "latitude"]].values.tolist()

    # 将数据保存为 JSON 文件
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(coordinates, json_file, ensure_ascii=False, indent=4)  # 格式化输出

    print(f"数据已保存到 {output_file}")

# 示例：假设文件名为 "data.csv"，输出文件为 "output.json"
csv_file = "./points.csv"
json_output = "output.json"
extract_coordinates(csv_file, json_output)
