import os

def delete_files_with_pattern_recursive(folder_path, pattern):
    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # 如果文件名中包含指定的模式字符串，则删除该文件
            if pattern in filename:
                file_path = os.path.join(root, filename)
                os.remove(file_path)
                print(f"已删除: {file_path}")

# 指定总的文件夹路径和需要匹配的模式
folder_path = r'D:\PythonProject\yolov8-pytorch-master\yolov8-pytorch-master'
pattern = '(1)'

# 调用函数进行递归删除操作
delete_files_with_pattern_recursive(folder_path, pattern)
