import cv2
import camera

def main():
    #1创建摄像头对象
    my_camera = camera.Camera(0)
    #2检查摄像头有没有成功打开
    if my_camera.is_opened():
        print("It's on!")
        try:

            while True:

                #读取下一帧
                success, frame = my_camera.read_frame()
                #如果读取失败，退出
                if not success:
                    break
                #显示帧
                cv2.imshow("camera", frame)
                #检查用户是否按下q键
                #如果按下q键，退出
                key = cv2.waitKey(1)
                if key == ord('q') or key == ord('Q'):
                    break
                #检查用户是否点右上角x键退出
                try:
                    visible = cv2.getWindowProperty("camera", cv2.WND_PROP_AUTOSIZE)
                except cv2.error:
                    break
                    
                if visible   < 0:
                    break
        finally:

                #释放摄像头
                my_camera.release()
                #关闭所有窗口
                cv2.destroyAllWindows()

    else:
        print("It's off!")
        my_camera.release()
        raise SystemExit


if __name__ == "__main__":
    main()