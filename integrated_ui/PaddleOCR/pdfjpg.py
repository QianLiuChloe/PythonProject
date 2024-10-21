from pdf2image import convert_from_path


def pdf_to_jpg(pdf_path, output_dir, dpi=300):
    """
    将 PDF 文件中的页面转换为 JPG 图像并保存到指定目录。

    参数:
    pdf_path (str): PDF 文件的路径
    output_dir (str): 输出 JPG 图像的目录
    dpi (int): 图像的分辨率,默认为 300 dpi
    """
    pages = convert_from_path(pdf_path, dpi=dpi)

    for i, page in enumerate(pages):
        output_path = f"{output_dir}/page_{i + 1}.jpg"
        page.save(output_path, "JPEG")


# 使用示例
pdf_to_jpg("input.pdf", "output_dir")