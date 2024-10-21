import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO


if __name__ == '__main__':
    # /root/ultralytics/cfg/models/yolov8.yamls
    model = YOLO(r'C:\Users\fan\Desktop\yolov11\ultralytics-main\ultralytics\cfg\models\11\yolo11s.yaml')
    model.load('yolo11s.pt') # loading pretrain weights
    model.train(data=r'C:\Users\fan\Desktop\yolov11\ultralytics-main\dataset\data.yaml',
                cache=False,
                imgsz=640,
                epochs=300,
                batch=8,
                close_mosaic=0,
                workers=8,
                # device='0',
                optimizer='auto', # using SGD
                # patience=0, # close earlystop
                # resume=True, # 断点续训,YOLO初始化时选择last.pt
                # amp=False, # close amp
                fraction=1,
                project='runs/train',
                name='yolov11',
                )