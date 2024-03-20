import os
import threading
from tkinter import Tk, Label, Button, filedialog, StringVar, Text, END, Scrollbar, HORIZONTAL
from tkinter.ttk import Progressbar
import cv2
from PIL import Image
import numpy as np

def resize_and_copy_files(src_dir, dest_dir, resize_factor=0.5, progress_callback=None, finished_callback=None):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)  # 如果目标目录不存在，则创建

    total_files = 0
    eligible_files = {}  # 保存符合条件的文件路径
    for root, dirs, files in os.walk(src_dir):
        jpg_files = [file for file in files if file.endswith('.jpg')]
        target_files = [file for file in jpg_files if file.endswith('0.jpg')]
        
        # 如果目录下没有以'0.jpg'结尾的图片，则使用所有.jpg文件
        if not target_files and jpg_files:
            eligible_files[root] = jpg_files
            total_files += len(jpg_files)
        elif target_files:
            eligible_files[root] = target_files
            total_files += len(target_files)

    processed_files = 0
    for root, target_files in eligible_files.items():
        for file in target_files:
            src_file_path = os.path.join(root, file)
            dest_file_path = os.path.join(dest_dir, file)

            # 使用Pillow读取图片
            img_pil = Image.open(src_file_path)
            img_np = np.array(img_pil)  # 将PIL图像转换为numpy数组

            # 如果图片是RGBA格式，转换为RGB格式
            if img_np.shape[-1] == 4:
                img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)

            # 使用OpenCV调整图片大小
            new_width = int(img_np.shape[1] * resize_factor)
            new_height = int(img_np.shape[0] * resize_factor)
            img_resized = cv2.resize(img_np, (new_width, new_height), interpolation=cv2.INTER_AREA)

            # 将OpenCV图像转换回PIL图像，然后保存
            img_resized_pil = Image.fromarray(img_resized)
            img_resized_pil.save(dest_file_path)

            processed_files += 1
            if progress_callback:
                progress = (processed_files / total_files) * 100
                progress_callback(file, progress)

    if finished_callback:
        finished_callback()

def update_progress(filename, progress):
    progress_var.set(f"Copying {filename}... {progress:.2f}%")
    progress_bar['value'] = progress
    text.insert(END, f"Copied {filename}\n")
    text.see(END)

def copy_finished():
    progress_var.set("Copy finished!")
    text.insert(END, "All files have been copied successfully.\n")
    text.see(END)

def start_copy():
    src = source_var.get()
    dest = destination_var.get()
    thread = threading.Thread(target=resize_and_copy_files, args=(src, dest, 0.5), kwargs={'progress_callback': update_progress, 'finished_callback': copy_finished})
    thread.daemon = True  # 将线程设置为守护线程
    thread.start()

def browse_source():
    directory = filedialog.askdirectory()
    source_var.set(directory)

def browse_destination():
    directory = filedialog.askdirectory()
    if directory:
        # 将目录路径标准化并确保使用'/'作为路径分隔符
        directory = directory.replace(os.sep, '/')
        
        # 标准化源路径，并使用'/'作为路径分隔符
        normalized_source_path = os.path.normpath(source_var.get()).replace(os.sep, '/')
        source_path_elements = normalized_source_path.split('/')

        extra_path_elements = []
        if "OK" in source_var.get():
            extra_path_elements = source_path_elements[-2:]
        elif "NG" in source_var.get():
            extra_path_elements = source_path_elements[-3:]

        # 使用'/'连接目录和额外的路径元素，确保路径分隔符的一致性
        final_path = "/".join([directory] + extra_path_elements)
        destination_var.set(final_path)


app = Tk()
app.title("Copy and Resize Files")

source_var = StringVar()
destination_var = StringVar()
progress_var = StringVar(value="Progress...")

Label(app, text="Source Directory:").pack()
Button(app, text="Browse Source", command=browse_source).pack()
Label(app, textvariable=source_var, wraplength=400).pack()

Label(app, text="Destination Directory:").pack()
Button(app, text="Browse Destination", command=browse_destination).pack()
Label(app, textvariable=destination_var, wraplength=400).pack()

Button(app, text="Start Copy", command=start_copy).pack()

Label(app, textvariable=progress_var).pack()
progress_bar = Progressbar(app, orient=HORIZONTAL, length=400, mode='determinate')
progress_bar.pack()

text = Text(app, width=75, height=10)
scroll = Scrollbar(app, orient="vertical", command=text.yview)
text.configure(yscrollcommand=scroll.set)
text.pack(side="left", fill="y")
scroll.pack(side="right", fill="y")

app.mainloop()
