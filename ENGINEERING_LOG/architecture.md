# Camera Detector Architecture

本文只描述当前代码中的有效结构。历史设计原因记录在对应日期的 Engineering Log 中。

## 模块职责

| 模块 | 当前职责 |
| --- | --- |
| `main.py` | 程序入口、采集循环、平均 FPS 统计与叠加、画面显示、用户退出判断和窗口清理 |
| `camera.py` | 创建摄像头设备、报告打开状态、读取帧和释放设备 |
| `cv2` | 提供底层摄像头访问与窗口 API |

## 依赖关系

```text
main.py
  ├─> camera.Camera
  │     └─> cv2.VideoCapture
  └─> cv2 window APIs
```

`main.py` 不直接操作 `cv2.VideoCapture`。`camera.py` 不负责显示画面或处理键盘输入。

## 数据流

```text
摄像头
  → Camera.read_frame()
  → (success, frame)
  → main.py
  → 统计成功帧数并约每秒更新平均 FPS
  → cv2.putText()
  → cv2.imshow()
```

当 `success` 为 `False` 时，`main.py` 结束采集循环，不继续处理该帧。

FPS 统计使用 `time.perf_counter()` 计算实际经过时间。`main.py` 在统计周期达到一秒后以“成功帧数 / 实际经过时间”更新显示值；`Camera` 不参与计时或文字绘制。

## 资源生命周期

1. `main.py` 创建 `Camera(0)`。
2. `is_opened()` 决定是否进入采集循环。
3. 采集循环位于 `try` 中。
4. `finally` 负责调用 `Camera.release()` 和 `cv2.destroyAllWindows()`。
5. 摄像头打开失败时，程序释放设备对象后退出。

摄像头由 `Camera` 管理，显示窗口由 `main.py` 管理。

## 错误边界

- 打开失败通过 `is_opened() == False` 表达。
- 读取失败通过 `read_frame()` 返回的 `success == False` 表达。
- 查询已经关闭的窗口可能产生 `cv2.error`，由 `main.py` 捕获并转为退出流程。

## 验证状态

以上结构来自当前代码的静态检查。仓库中没有自动化测试，也没有保留本版本的硬件运行结果。
