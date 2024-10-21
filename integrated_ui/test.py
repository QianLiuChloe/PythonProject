import pandas as pd

# 示例数据
data = {
    'MARK': [1, 2, 3],
    'TYPE': ['A', 'B', 'C'],
    'SIZE (MINIMUM)': [10, 20, 30],
    'REINFORCEMENT': [True, False, True]
}

# 创建 DataFrame
df = pd.DataFrame(data)

# 打印 DataFrame 的列名
print("DataFrame 列名:")
print(df.columns)

# 直接在列名中查找包含 "SIZE" 的列
matching_columns = [col for col in df.columns if 'SIZE' in col.upper()]

# 打印匹配的列名列表
print("匹配的列名列表:")
print(matching_columns)

if matching_columns:
    size_col_name = matching_columns[0]
    print(f"列名包含 'SIZE' 的列是: {size_col_name}")
else:
    print("没有找到包含 'SIZE' 的列名。")