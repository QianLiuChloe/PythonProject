# Ultralytics YOLO 🚀, AGPL-3.0 license

import argparse
from pathlib import Path

import cv2
import pandas as pd
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction
from sahi.utils.yolov8 import download_yolov8s_model

from ultralytics.utils.files import increment_path
from ultralytics.utils.plotting import Annotator, colors


class SAHIInference:
    """Runs YOLOv8 and SAHI for object detection on images with options to view, save, and track results."""

    def __init__(self):
        """Initializes the SAHIInference class for performing sliced inference using SAHI with YOLOv8 models."""
        self.detection_model = None
        self.category_counts = {}

    def load_model(self, weights):
        """Loads a YOLOv8 model with specified weights for object detection using SAHI."""
        yolov8_model_path = f"{weights}"
        # download_yolov8s_model(yolov8_model_path)
        self.detection_model = AutoDetectionModel.from_pretrained(
            model_type="yolov8", model_path=yolov8_model_path, confidence_threshold=0.3, device="cpu"
        )

    def inference(
        self, weights="yolov8n.pt", source="images/", view_img=False, save_img=False, exist_ok=False, track=False
    ):
        """
        Run object detection on images using YOLOv8 and SAHI.

        Args:
            weights (str): Model weights path.
            source (str): Directory containing images.
            view_img (bool): Show results.
            save_img (bool): Save results.
            exist_ok (bool): Overwrite existing files.
            track (bool): Enable object tracking with SAHI
        """
        # 输出设置
        save_dir = increment_path(Path("ultralytics_results_with_sahi") / "exp", exist_ok)
        save_dir.mkdir(parents=True, exist_ok=True)

        # 获取图像文件列表
        image_files = list(Path(source).glob("*.jpg")) + list(Path(source).glob("*.png"))

        # 加载模型
        self.load_model(weights)

        for img_path in image_files:
            # 重置类别计数字典
            self.category_counts = {}

            # 读取图像
            frame = cv2.imread(str(img_path))
            if frame is None:
                print(f"Error reading image: {img_path}")
                continue

            # 初始化注释器
            annotator = Annotator(frame)  # Initialize annotator for plotting detection and tracking results

            # 进行切片预测
            results = get_sliced_prediction(
                frame,
                self.detection_model,
                slice_height=512,
                slice_width=512,
                overlap_height_ratio=0.2,
                overlap_width_ratio=0.2,
            )
            detection_data = [
                (det.category.name, det.category.id, (det.bbox.minx, det.bbox.miny, det.bbox.maxx, det.bbox.maxy))
                for det in results.object_prediction_list
            ]

            # 绘制检测结果
            for det in detection_data:
                annotator.box_label(det[2], label=str(det[0]), color=colors(int(det[1]), True))

                # 更新类别计数
                if det[0] not in self.category_counts:
                    self.category_counts[det[0]] = 0
                self.category_counts[det[0]] += 1

            # 显示图像
            if view_img:
                cv2.imshow(f"Detection: {img_path.name}", frame)
                if cv2.waitKey(0) & 0xFF == ord("q"):
                    break

            # 保存图像
            if save_img:
                output_path = str(save_dir / f"{img_path.stem}_result{img_path.suffix}")
                cv2.imwrite(output_path, frame)
                print(f"Saved to: {output_path}")

            # 保存当前图片的类别计数到 Excel 文件
            df = pd.DataFrame(list(self.category_counts.items()), columns=["Category", "Count"])
            excel_path = str(save_dir / f"{img_path.stem}_category_counts.xlsx")
            df.to_excel(excel_path, index=False)
            print(f"Category counts for {img_path.name} saved to: {excel_path}")

        # 关闭所有窗口
        cv2.destroyAllWindows()

    def parse_opt(self):
        """Parse command line arguments."""
        parser = argparse.ArgumentParser()
        parser.add_argument("--weights", type=str, default=r"D:\PythonProject\SAHI\ultralytics-main\runs\res\weights\best.pt", help="initial weights path")
        parser.add_argument("--source", type=str, default=r"D:\PythonProject\SAHI\ultralytics-main\raw.v1i.yolov8\demo", help="video file path")
        parser.add_argument("--view-img", action="store_true", help="show results")
        parser.add_argument("--save-img", default=True, help="save results")
        parser.add_argument("--exist-ok", action="store_true", help="existing project/name ok, do not increment")
        return parser.parse_args()


if __name__ == "__main__":
    inference = SAHIInference()
    inference.inference(**vars(inference.parse_opt()))