import os
from PIL import Image
import numpy as np
import cv2

def copy_and_resize_files(src_dir, dest_dir, resize_factor=0.5):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)  # 如果目标目录不存在，则创建

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith("0.jpg"):
                src_file_path = os.path.join(root, file)
                dest_file_path = os.path.join(dest_dir, file)

                # 使用Pillow读取图片
                img_pil = Image.open(src_file_path)
                img_np = np.array(img_pil)  # 将PIL图像转换为numpy数组

                # 如果图片是RGBA格式，转换为RGB格式
                if img_np.shape[2] == 4:
                    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)

                # 使用OpenCV调整图片大小
                new_width = int(img_np.shape[1] * resize_factor)
                new_height = int(img_np.shape[0] * resize_factor)
                img_resized = cv2.resize(img_np, (new_width, new_height), interpolation=cv2.INTER_AREA)

                # 将OpenCV图像转换回PIL图像，然后保存
                img_resized_pil = Image.fromarray(img_resized)
                img_resized_pil.save(dest_file_path)

# 使用示例
src_dir = "Y:\\DAOI 14\\檢測圖檔\\站一\\20240119\\F5121-240100748-001.1\\OK"
dest_dir = "C:\\Users\\VFC0646\\Desktop\\F5121-240100748-001.1\\OK"  # 确保替换为你的实际目标目录路径

copy_and_resize_files(src_dir, dest_dir, resize_factor=0.5)
