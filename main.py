import cv2
import camera
import time

#计算fps
def calculate_fps(previous_time, fps_num) -> tuple[float, float, int]:
    #获取当前时间
    current_time = time.perf_counter()
    #帧数+1
    fps_num += 1
    #判断是否过了一秒
    if current_time - previous_time >= 1:
        
        #如果过了一秒，输出平均fps并重置fps_num和previous_time
        fps = fps_num / (current_time - previous_time)
        fps_num = 0
        previous_time = current_time
        return fps, previous_time,fps_num
    else:
        #如果没有，返回
        return 0, previous_time, fps_num

def main():
    #1创建摄像头对象
    my_camera = camera.Camera(0)
    previous_time = time.perf_counter()
    fps_num = 0
    fps = 0
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
                
                tfps, previous_time, fps_num = calculate_fps(previous_time, fps_num)

                fps = tfps if tfps != 0 else fps
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
