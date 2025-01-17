import os
import re
import numpy as np
import cv2

# 视频文件夹路径
videos_dir = "/data/fucongrui/VVC_dataset/10bit"

# 遍历视频文件夹下的所有文件
for filename in os.listdir(videos_dir):
    # 判断文件是否为YUV视频文件
    if not filename.endswith(".yuv"):
        continue

    # 视频文件路径
    video_path = os.path.join(videos_dir, filename)

    # 从文件名中提取视频分辨率和帧率等参数
    match = re.search(r"\w+_\d+_\w+_(\d+)x(\d+)_(\d+)", os.path.basename(video_path))
    if match:
        width, height, fps = int(match.group(1)), int(match.group(2)), int(match.group(3))
    else:
        raise ValueError("Failed to parse video file name: %s" % video_path)

    # 图像保存路径
    output_dir = os.path.splitext(video_path)[0]

    # 创建图像保存目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 读取视频文件
    with open(video_path, "rb") as f:
        # 计算每一帧的大小（8bit）(10bit *3)
        frame_size = int(width * height * 3)
        # 循环读取前9帧
        for i in range(9):
            # 读取一帧数据
            frame_data = f.read(frame_size)
            # 将数据转换为numpy数组（8bit）(10bit-np.uint16)
            frame = np.frombuffer(frame_data, dtype=np.uint16)
            # 将数据重塑为图像矩阵（8bit）
            frame = frame.reshape((int(height*1.5), width))
            # 将图像矩阵转换为BGR格式（8bit）(10bit-cv2.COLOR_YUV2BGR_P010)
            frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_P010)
            # 将图像保存为文件
            output_path = os.path.join(output_dir, "frame%d.jpg" % (i+1))
            cv2.imwrite(output_path, frame)
