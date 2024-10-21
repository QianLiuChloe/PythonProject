import os
import shutil

# 指定原始图片目录
src_image_dir = 'F:\earn\yolov8-pytorch-master\yolov8-pytorch-master\VOCdevkit\VOC2007\JPEGImages'

# 指定原始标签目录
src_label_dir = 'F:\earn\yolov8-pytorch-master\yolov8-pytorch-master\VOCdevkit\VOC2007\Annotations'

# 指定修改后的数据集目录
dst_dir = r'F:\earn\yolov8-pytorch-master\yolov8-pytorch-master\VOCdevkit\VOC2007\renam'

# 创建修改后的数据集目录
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

# 初始化计数器
counter = 1

# 遍历原始标签目录
for label_filename in os.listdir(src_label_dir):
    # 检查是否为 XML 文件
    if label_filename.endswith('.xml'):
        # 提取原始图片名称
        base_name = os.path.splitext(label_filename)[0]

        # 构建原始图片路径
        src_image_path = os.path.join(src_image_dir, f'{base_name}.jpg')

        # 修改图片名称
        new_image_filename = f'{counter}.jpg'

        # 修改标签名称
        new_label_filename = f'{counter}.xml'

        # 复制图片到修改后的数据集目录
        dst_image_path = os.path.join(dst_dir, new_image_filename)
        shutil.copy(src_image_path, dst_image_path)

        # 复制标签到修改后的数据集目录
        src_label_path = os.path.join(src_label_dir, label_filename)
        dst_label_path = os.path.join(dst_dir, new_label_filename)
        shutil.copy(src_label_path, dst_label_path)

        # 递增计数器
        counter += 1

print('数据集修改完成!')