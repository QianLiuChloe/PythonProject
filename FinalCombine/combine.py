import pandas as pd

# 读取表格数据
df1 = pd.read_excel('2-3.xlsx')  # 表格一步骤四
df2 = pd.read_excel('1_category_counts.xlsx')  # 表格二

# 将表格二中的构件类别列（第一列）全部转换为大写
df2.iloc[:, 0] = df2.iloc[:, 0].str.upper()

# 创建一个字典用于存储表格二中每个构件的总数量
quantity_dict = df2.groupby(df2.columns[0])[df2.columns[1]].sum().to_dict()

# 在表格一中添加一列用于存储数量信息，列名可以设为 '数量'
df1['Number'] = 0

# 遍历表格一中的每个构件，并从字典中获取对应的数量
for idx, row in df1.iterrows():
    component_name = row[df1.columns[0]].upper()  # 将表格一中的构件名转换为大写以匹配
    # 如果该构件在字典中存在，则更新数量
    if component_name in quantity_dict:
        df1.at[idx, 'Number'] = quantity_dict[component_name]

# 保存处理后的表格一或创建新表格
df1.to_excel('2-4.xlsx', index=False)
