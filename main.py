import numpy as np

# 视频文件路径
video_path = "G:\Cu-GAN\data\C_0_BasketballDrill_832x480_50.yuv"

# 视频分辨率和帧率
width = 832
height = 480
fps = 50

# 输出文件路径
output_path = "G:\Cu-GAN\data\output.yuv"

# 读取视频文件
with open(video_path, "rb") as f:
    # 创建输出文件
    with open(output_path, "wb") as out:
        # 计算每一帧的大小
        frame_size = int(width * height * 1.5)
        # 循环读取前9帧
        for i in range(9):
            # 读取一帧数据
            frame_data = f.read(frame_size)
            # 将数据转换为numpy数组
            frame = np.frombuffer(frame_data, dtype=np.uint8)
            # 将数据重塑为图像矩阵
            frame = frame.reshape((int(height*1.5), width))
            # 将图像矩阵写入输出文件
            out.write(frame.tobytes())

