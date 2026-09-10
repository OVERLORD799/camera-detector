import cv2

class FrameSaver:
    def __init__(self):
        self.frame_count = 0

    def save_frame(self, frame, frame_type):
        if frame_type == "gray":
            frame = self.grey(frame)
        elif frame_type == "color":
            frame = frame
        cv2.imwrite(f"frames/frame{self.frame_count}.jpg", frame)
        print(f"Saved frame{self.frame_count}.jpg")
        self.frame_count += 1

    def grey(self, frame):
        # 将帧转换为灰度图像
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return gray_frame

