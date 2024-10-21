from ultralytics.data.split_data import split_trainval


split_trainval(
    data_root=r"D:\PythonPRroject\SAHI\ultralytics-main\raw.v1i.yolov8\train",
    save_dir="./dataset",
    rates=[1.0],
    gap=200,
    crop_size=640
)