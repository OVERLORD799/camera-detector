#此模块用于从摄像头中获取图像并将它传递给其他模块进行处理

import cv2

class Camera:
    #创建camera对象，index为摄像头的索引号
    def __init__(self, index)  -> None:
        self.index = index
        self.camera = cv2.VideoCapture(index)

    #检查摄像头是否成功打开
    def is_opened(self)  -> bool:
        return self.camera.isOpened()

    #读取下一帧
    def read_frame(self)   -> tuple[bool, any]: 
        return self.camera.read()

    #释放摄像头
    def release(self) -> None:  
        self.camera.release()