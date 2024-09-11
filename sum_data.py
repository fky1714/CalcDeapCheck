import pandas as pd

# CSVファイルを読み込む
file_path = './data_410_423.csv'
data = pd.read_csv(file_path)

# 2列目に'LEGEND'が含まれる行をフィルタリングし、3列目の値を合計する
total_sum = data[data.iloc[:, 1].str.contains('LEGEND', na=False)].iloc[:, 2].sum()

print(total_sum)
