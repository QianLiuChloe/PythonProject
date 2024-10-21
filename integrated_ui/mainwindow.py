import sys
import os
from pathlib import Path

import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'ultralyticsmain'))
import shutil

import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from yolov8_crop.yolo import YOLO as Crop_yolo
from PaddleOCR.paddleocr import PPStructure, draw_structure_result, save_structure_res
import cv2
from excel import process_excel
from ultralyticsmain.predict_with_sahi import SAHIInference


class ComponentRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("构件识别与生成构建表")

        self.save_folder = os.path.join(os.getcwd(), r"./output")

        # 设置窗口最小尺寸
        self.root.minsize(800, 600)

        # 创建并放置上传图纸按钮
        self.upload_button = Button(root, text="上传图纸", command=self.upload_drawing, width=20, height=5)
        self.upload_button.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # 创建并放置开始识别按钮
        self.recognize_button = Button(root, text="开始识别", command=self.recognize_components, state=tk.DISABLED,
                                       width=20, height=5)
        self.recognize_button.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # 创建并放置提取构建表按钮
        self.extract_table_button = Button(root, text="提取构建表", command=self.extract_table, state=tk.DISABLED,
                                           width=20, height=5)
        self.extract_table_button.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        # 处理excel
        self.excel_table_button = Button(root, text="处理excel", command=self._process_excel, state=tk.DISABLED,
                                         width=20, height=5)
        self.excel_table_button.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

        # sahi
        self.sahi_table_button = Button(root, text="sahi_infer推理", command=self.sahi_infer, state=tk.DISABLED,
                                        width=20, height=5)
        self.sahi_table_button.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # sahi
        self.combine_table_button = Button(root, text="combine", command=self.combine, state=tk.DISABLED,
                                           width=20, height=5)
        self.combine_table_button.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        # 创建结果文本框
        self.result_text = Text(root, height=20, width=40, font=("Arial", 12), wrap=tk.WORD)  # 添加 wrap=WORD 使得文本自动换行
        self.result_text.grid(row=0, column=3, rowspan=4, padx=10, pady=10, sticky='nsew', columnspan=2)

        # 图纸预览区域
        self.preview_image_label = Label(root,relief=tk.SUNKEN)
        self.preview_image_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        self.model_crop = Crop_yolo()
        self.table_engine = PPStructure(show_log=False)
        self.inference = SAHIInference()

        self.image_path = ""

    def upload_drawing(self):
        # 使用文件对话框让用户选择一个文件
        self.image_path = filedialog.askopenfilename(
            initialdir=os.path.join(os.getcwd(), "source"),  # 初始目录为当前工作目录
            title="选择图纸",
            filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*"))
        )

        if self.image_path:  # 确保有图像路径
            try:
                image = Image.open(self.image_path)
                image.thumbnail((600, 750))  # 缩小到适合预览的大小
                photo = ImageTk.PhotoImage(image)
                self.preview_image_label.config(image=photo)
                self.preview_image_label.image = photo  # 保持对图片的引用防止被垃圾回收

                # 启用识别按钮
                self.recognize_button.config(state=tk.NORMAL)

                # 可以在这里添加更多反馈信息，比如显示成功上传的信息
                self.result_text.insert(tk.END, "图纸已成功上传。\n")

            except Exception as e:
                messagebox.showerror("错误", f"无法打开文件: {e}")
                # 如果打开文件失败，禁用识别按钮
                self.recognize_button.config(state=tk.DISABLED)

    def recognize_components(self):
        if os.path.exists('./img_crop'):
            shutil.rmtree('./img_crop')
        try:
            image = Image.open(self.image_path)
            r_image, infos = self.model_crop.detect_image(image, crop=True, count=True)  # 进行构件识别与数量统计
            r_image.thumbnail((750, 600))  # 缩小到适合预览的大小
            photo = ImageTk.PhotoImage(r_image)
            self.preview_image_label.config(image=photo)
            self.preview_image_label.image = photo  # 保持对图片的引用防止被垃圾回收

            # 清空结果文本框并插入新的识别结果
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"result is below:\n{str(infos)}")

            # 启用提取构建表按钮
            self.extract_table_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("错误", f"识别失败: {e}")
            # 如果识别失败，禁用提取构建表按钮
            self.extract_table_button.config(state=tk.DISABLED)

    def extract_table(self):
        if os.path.exists(self.save_folder):
            shutil.rmtree(self.save_folder)
        try:
            save_folder = self.save_folder
            img_path = filedialog.askopenfilename(
                initialdir=os.path.join(os.getcwd(), "img_crop"),  # 初始目录为当前工作目录
                title="选择表格",
                filetypes=(("PNG files", "*.png"), ("All files", "*.*"))
            )
            if not img_path:
                return  # 用户取消了文件选择
            img = cv2.imread(img_path)
            result = self.table_engine(img)
            save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0])

            # 清空结果文本框并插入新的识别结果
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"save result in {save_folder}\n")
            self.result_text.insert(tk.END, str(result))
            self.excel_table_button.config(state=tk.NORMAL)  # 启用处理 Excel 按钮

        except Exception as e:
            messagebox.showerror("错误", f"提取构建表时发生错误: {e}")
            self.excel_table_button.config(state=tk.DISABLED)  # 如果提取失败，禁用处理 Excel 按钮

    def _process_excel(self):
        if os.path.exists("process_excel"):
            shutil.rmtree(r"D:\integrated_ui\process_excel")
        os.makedirs(r"D:\integrated_ui\process_excel")
        all_infos = []
        res = os.listdir(self.save_folder)
        for i in res:
            detail = os.listdir(os.path.join(self.save_folder, i))
            detail = [f for f in detail if f.lower().endswith('.xlsx')]
            # print(detail)
            for r in detail:
                file_path = os.path.join(os.path.join(self.save_folder, i), r)  # 获取完整路径
                try:
                    # 打印调试信息
                    print(f"正在处理文件: {file_path}")

                    news = process_excel(file_path,
                                         os.path.join(r"D:\integrated_ui\process_excel", r))  # 传递完整路径
                    all_infos.append(news)
                except Exception as e:
                    messagebox.showerror("错误", f"处理文件 {i} 时发生错误: {e}")

        # 清空结果文本框并插入新的处理结果
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"{all_infos}")
        self.sahi_table_button.config(state=tk.NORMAL)  # 启用处理 Excel 按钮

    def sahi_infer(self):

        try:
            args = {
                "weights": r"D:\integrated_ui\ultralyticsmain\runs\res\weights\best.pt",
                "source": self.image_path,
                "view_img": False,
                'save_img': False,
                'exist_ok': True,
            }
            self.inference.inference(**args)
            self.result_text.insert(tk.END, "SAHI 推理完成。\n")
            self.combine_table_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("错误", f"SAHI 推理失败: {e}")

    def combine(self):

        # 读取表格数据
        df1 = pd.read_excel(os.path.join(r'.\process_excel', os.listdir(r'.\process_excel')[0]))  # 表格一
        df2 = pd.read_excel(
            os.path.join(r'.\ultralytics_results_with_sahi', os.listdir(r'.\ultralytics_results_with_sahi')[0]))  # 表格一

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
        df1.to_excel(f"{Path(os.listdir('process_excel')[0]).name}", index=False)
        self.result_text.insert(tk.END, "合成表格完成,del process_excel and ultralytics_results_with_sahi。\n")
        shutil.rmtree(r'.\process_excel')
        shutil.rmtree(r'.\ultralytics_results_with_sahi')


if __name__ == "__main__":
    root = tk.Tk()
    app = ComponentRecognitionApp(root)
    root.mainloop()