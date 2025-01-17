# -*- coding: utf-8 -*-

import math
from functools import partial
import numpy as np
import matplotlib.pyplot as plt
import cv2

import os
from os import path

def readyuv420(filename, bitdepth, W, H, startframe, totalframe, show=False):
    # 从第startframe（含）开始读（0-based），共读totalframe帧

    uv_H = H // 2
    uv_W = W // 2

    if bitdepth == 8:
        Y = np.zeros((totalframe, H, W), np.uint8)
        U = np.zeros((totalframe, uv_H, uv_W), np.uint8)
        V = np.zeros((totalframe, uv_H, uv_W), np.uint8)
    elif bitdepth == 10:
        Y = np.zeros((totalframe, H, W), np.uint16)
        U = np.zeros((totalframe, uv_H, uv_W), np.uint16)
        V = np.zeros((totalframe, uv_H, uv_W), np.uint16)

    plt.ion()

    bytes2num = partial(int.from_bytes, byteorder='little', signed=False)

    bytesPerPixel = math.ceil(bitdepth / 8)
    seekPixels = startframe * H * W * 3 // 2
    fp = open(filename, 'rb')
    fp.seek(bytesPerPixel * seekPixels)

    for i in range(totalframe):

        for m in range(H):
            for n in range(W):
                if bitdepth == 8:
                    pel = bytes2num(fp.read(1))
                    Y[i, m, n] = np.uint8(pel)
                elif bitdepth == 10:
                    pel = bytes2num(fp.read(2))
                    Y[i, m, n] = np.uint16(pel)

        for m in range(uv_H):
            for n in range(uv_W):
                if bitdepth == 8:
                    pel = bytes2num(fp.read(1))
                    U[i, m, n] = np.uint8(pel)
                elif bitdepth == 10:
                    pel = bytes2num(fp.read(2))
                    U[i, m, n] = np.uint16(pel)

        for m in range(uv_H):
            for n in range(uv_W):
                if bitdepth == 8:
                    pel = bytes2num(fp.read(1))
                    V[i, m, n] = np.uint8(pel)
                elif bitdepth == 10:
                    pel = bytes2num(fp.read(2))
                    V[i, m, n] = np.uint16(pel)

        if show:
            print(i)
            plt.subplot(131)
            plt.imshow(Y[i, :, :], cmap='gray')
            plt.subplot(132)
            plt.imshow(U[i, :, :], cmap='gray')
            plt.subplot(133)
            plt.imshow(V[i, :, :], cmap='gray')
            plt.show()
            plt.pause(1)
            # plt.pause(0.001)

    if totalframe == 1:
        return Y[0], U[0], V[0]
    else:
        return Y, U, V


def yuv2rgb(yuvfilename, W, H, startframe, totalframe, show=False, out=False):
    # 从第startframe（含）开始读（0-based），共读totalframe帧
    arr = np.zeros((totalframe, H, W, 3), np.uint8)

    plt.ion()
    with open(yuvfilename, 'rb') as fp:
        seekPixels = startframe * H * W * 3 // 2
        fp.seek(8 * seekPixels)  # 跳过前startframe帧
        for i in range(totalframe):
            print(i)
            oneframe_I420 = np.zeros((H * 3 // 2, W), np.uint8)
            for j in range(H * 3 // 2):
                for k in range(W):
                    oneframe_I420[j, k] = int.from_bytes(fp.read(1), byteorder='little', signed=False)
            oneframe_RGB = cv2.cvtColor(oneframe_I420, cv2.COLOR_YUV2RGB_I420)
            if show:
                plt.imshow(oneframe_RGB)
                plt.show()
                plt.pause(0.001)
            if out:
                outname = yuvfilename[:-4] + '_' + str(startframe + i) + '.png'
                cv2.imwrite(outname, oneframe_RGB[:, :, ::-1])
            arr[i] = oneframe_RGB
    return arr


def get_filelist(dir, Filelist):
    newDir = dir
    if os.path.isfile(dir):
        Filelist.append(dir)
        # # 若只是要返回文件文，使用这个
        # Filelist.append(os.path.basename(dir))
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            if s == 'old' or s == 'images':
                continue
            newDir = os.path.join(dir, s)
            get_filelist(newDir, Filelist)

    return Filelist
    # 判断是否是特定文件名称


if __name__ == '__main__':


   image_path = '/data/fucongrui/VVC_dataset'
   list = get_filelist(image_path, [])
   print(len(list))
   print(list[1])
   # for e in list:
   #     print(e)
    # y, u, v = readyuv420(r'F:\_commondata\video\176x144 qcif\football_qcif.yuv', 8, 176, 144, 1, 5, True)

    #y, u, v = readyuv420(r'G:\Cu-GAN\C_0_BasketballDrill_832x480_50.yuv', 8, 832, 480, 0, 9, True)
    #print(y.shape, u.shape, v.shape)

    #video = yuv2rgb(r'D:\_workspace\akiyo_qcif.yuv', 176, 144, 0, 10, False, True)