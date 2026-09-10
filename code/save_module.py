import cv2

class FrameSaver:
    def __init__(self):
        self.frame_count = 0

    def save_frame(self, frame):
        cv2.imwrite(f"frames/frame{self.frame_count}.jpg", frame)
        print(f"Saved frame{self.frame_count}.jpg")
        self.frame_count += 1


