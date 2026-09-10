import cv2

def save_frame(frame, i):
    cv2.imwrite(f"frames/frame{i}.jpg", frame)
    print(f"Saved frame{i}.jpg")
    return i + 1