import cv2

#1创建摄像头对象
my_camera = cv2.VideoCapture(0)
#2检查摄像头有没有成功打开
if my_camera.isOpened():
    print("It's on!")
while True:

    break
    #读取下一帧
    success, frame = my_camera.read()
    #如果读取失败，退出
    if not success:
        break
    #显示帧
    cv2.imshow("camera", frame)
    #检查用户是否按下q键
    #如果按下q键，退出
    key = cv2.waitKey(2)
    if key == 27:
        break
    
#释放摄像头
my_camera.release()
#关闭所有窗口
cv2.destoryAllWindows()