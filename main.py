import cv2

#1创建摄像头对象
my_camera = cv2.VideoCapture(0)
#2检查摄像头有没有成功打开
if my_camera.isOpened():
    print("It's on!")
while True:

    break
    #读取下一帧

    #如果读取失败，退出

    #显示帧

    #检查用户是否按下q键

    #如果按下，退出

#释放摄像头

#关闭所有窗口