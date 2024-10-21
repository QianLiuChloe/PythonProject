import os
from PIL import Image


def convert_jpg_to_png(input_folder, output_folder):
    # 如果输出文件夹不存在，则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            # 构造完整的文件路径
            img_path = os.path.join(input_folder, filename)

            # 打开图像并进行格式转换
            img = Image.open(img_path)
            # 将文件扩展名改为.png
            new_filename = os.path.splitext(filename)[0] + '.png'
            new_img_path = os.path.join(output_folder, new_filename)

            # 保存为PNG格式
            img.save(new_img_path, 'PNG')
            print(f"已转换: {img_path} -> {new_img_path}")


# 输入文件夹和输出文件夹路径
input_folder = r'C:\Users\chloe\OneDrive\桌面\new'
output_folder = r'C:\Users\chloe\OneDrive\桌面\neww'

# 调用函数进行转换
convert_jpg_to_png(input_folder, output_folder)
