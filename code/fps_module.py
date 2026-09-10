import time
import cv2

class FPSCounter:

    def __init__(self):
        self.previous_time = time.perf_counter()
        self.fps_num = 0
        self.fps = 0


    #计算fps
    def calculate_fps(self) -> float:
        #获取当前时间
        current_time = time.perf_counter()
        #帧数+1
        self.fps_num += 1
        #判断是否过了一秒
        if current_time - self.previous_time >= 1:
            
            #如果过了一秒，输出平均fps并重置fps_num和previous_time
            self.fps = self.fps_num / (current_time - self.previous_time)
            self.fps_num = 0
            self.previous_time = current_time
        return self.fps

    def show_fps(self, frame):

        fps = self.calculate_fps()
        
        cv2.putText(
                        frame,
                        f"FPS: {fps:.1f}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA
                    )
    



