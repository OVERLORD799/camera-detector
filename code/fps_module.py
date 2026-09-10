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



