import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import subprocess
from yolo import YOLO


class ComponentRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("构件识别与生成构建表")

        self.yolo = YOLO()

        self.upload_button = tk.Button(root, text="上传图纸", command=self.upload_drawing)
        self.upload_button.pack(pady=10)

        self.preview_label = tk.Label(root, text="图纸预览: 尚未上传图纸")
        self.preview_label.pack(pady=10)

        self.recognize_button = tk.Button(root, text="开始识别", command=self.recognize_components, state=tk.DISABLED)
        self.recognize_button.pack(pady=10)

        self.extract_table_button = tk.Button(root, text="提取构建表", command=self.extract_table, state=tk.DISABLED)
        self.extract_table_button.pack(pady=10)

        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.pack(pady=10)

        self.image_path = ""

    def upload_drawing(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png")])
        if self.image_path:
            self.preview_label.config(text=f"图纸预览: {self.image_path}")
            self.recognize_button.config(state=tk.NORMAL)

    def recognize_components(self):
        try:
            image = Image.open(self.image_path)
            r_image, couter = self.yolo.detect_image(image, crop=True, count=True)  # 进行构件识别与数量统计
            r_image.show()

            # 假设 detect_image 返回识别到的构件数量
            component_count = couter # 假设这个方法返回检测到的构件数量
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"构件识别完成，识别到 {component_count} 个构件。\n")

            self.extract_table_button.config(state=tk.NORMAL)  # 启用提取表格按钮
        except Exception as e:
            messagebox.showerror("错误", f"识别失败: {e}")

    def extract_table(self):
        try:
            command = [
                "paddleocr",
                "--image_dir", self.image_path,
                "--type", "structure",
                "--image_orientation", "true"
            ]
            # 执行命令
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                self.result_text.insert(tk.END, f"提取结果:\n{result.stdout}\n")
            else:
                messagebox.showerror("错误", f"提取失败: {result.stderr}")
        except Exception as e:
            messagebox.showerror("错误", f"提取构建表时发生错误: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ComponentRecognitionApp(root)
    root.mainloop()