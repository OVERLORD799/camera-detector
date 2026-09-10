import cv2

class Processor:
    def __init__(self):
        pass
    
    def grey(self, frame):
        # 将帧转换为灰度图像
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return gray_frame

    def edges_detector(self, frame):
        a = 5
        b = (a,a)
        # 将帧转换为灰度图像
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #使用高斯滤波
        blurred = cv2.GaussianBlur(gray_frame,b,0)
        # 使用Canny边缘检测算法
        edges_frame = cv2.Canny(blurred, 100, 200)
        return edges_frame
