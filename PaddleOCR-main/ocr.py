import os
import cv2
from paddleocr import PPStructure, draw_structure_result, save_structure_res

table_engine = PPStructure(show_log=True)

save_folder = './output'
img_path = r'1.png'
img = cv2.imread(img_path)
result = table_engine(img)
save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])

for line in result:
    line.pop('img')
    print(line)






from PIL import Image

font_path = 'doc/fonts/simfang.ttf'  # PaddleOCR下提供字体包
image = Image.open(img_path).convert('RGB')
im_show = draw_structure_result(image, result, font_path=font_path)
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')
# import os
# import cv2
# from paddleocr import PPStructure,save_structure_res
#
# table_engine = PPStructure(table=False, ocr=False, show_log=True)
#
# save_folder = './output'
# img_path = 'out/3.png'
# img = cv2.imread(img_path)
# result = table_engine(img)
# save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])
#
# for line in result:
#     line.pop('img')
#     print(line)
# box = result[0]['bbox']
# print(box)
# x, y, width, height = box
# cropped_image = img[y:y+height, x:x+width]
#
# # 保存裁剪后的图片
# cv2.imwrite('cropped_table.jpg', cropped_image)