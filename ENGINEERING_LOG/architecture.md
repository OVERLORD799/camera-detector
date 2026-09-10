# Camera Detector Architecture

本文只描述当前代码中的有效结构。历史设计原因记录在对应日期的 Engineering Log 中。

## 模块职责

| 模块 | 当前职责 |
| --- | --- |
| `code/main.py` | 程序入口、采集循环、画面显示、用户输入和资源清理 |
| `code/camera.py` | 创建摄像头设备、报告打开状态、读取帧和释放设备 |
| `code/fps_module.py` | `FPSCounter` 保存计时、帧计数和最新 FPS 状态，计算约一秒周期的平均 FPS 并将其绘制到帧 |
| `code/save_module.py` | `FrameSaver` 保存文件序号，将帧转为灰度图并写入 JPEG |
| `cv2` | 提供底层摄像头访问与窗口 API |

## 依赖关系

```text
code/main.py
  ├─> camera.Camera
  │     └─> cv2.VideoCapture
  ├─> fps_module.FPSCounter
  ├─> save_module.FrameSaver
  └─> cv2 window APIs
```

`code/main.py` 不直接操作 `cv2.VideoCapture`、`cv2.putText()` 或 `cv2.imwrite()`。`code/camera.py` 不负责显示画面或处理键盘输入。FPS 文字的计算与绘制由 `FPSCounter` 完成，帧保存由 `FrameSaver` 完成。

## 数据流

```text
摄像头
  → Camera.read_frame()
  → (success, frame)
  → code/main.py
  → FPSCounter.show_fps()
      → calculate_fps()
      → cv2.putText()
  → cv2.imshow()
  → S/s 按键触发 FrameSaver.save_frame()
  → cv2.cvtColor(..., COLOR_BGR2GRAY)
  → cv2.imwrite()
```

当 `success` 为 `False` 时，`main.py` 结束采集循环，不继续处理该帧。

`FPSCounter` 使用 `time.perf_counter()` 计算实际经过时间，在内部保存统计周期起点、帧数和最新 FPS，并通过 `show_fps()` 将结果绘制到传入的帧。S/s 保存发生在 FPS 文字绘制之后；`FrameSaver` 再将该 BGR 帧转为灰度图，因此生成的 JPEG 是带 FPS 文字的单通道图像。

## 资源生命周期

1. `code/main.py` 创建 `Camera(0)`、`FPSCounter()` 和 `FrameSaver()`。
2. `is_opened()` 决定是否进入采集循环。
3. 采集循环位于 `try` 中。
4. `finally` 负责调用 `Camera.release()` 和 `cv2.destroyAllWindows()`。
5. 摄像头打开失败时，程序释放设备对象后退出。

摄像头由 `Camera` 管理，显示窗口由 `code/main.py` 管理。

## 错误边界

- 打开失败通过 `is_opened() == False` 表达。
- 读取失败通过 `read_frame()` 返回的 `success == False` 表达。
- 查询已经关闭的窗口可能产生 `cv2.error`，由 `main.py` 捕获并转为退出流程。

## 验证状态

当前结构已通过静态检查。可控计时验证了 `FPSCounter` 保留状态、按周期计算平均 FPS、重置帧计数并修改传入帧。`FrameSaver` 已验证可以连续写入两张灰度图并保留递增序号。可控主循环回归测试覆盖了显示、保存后 Q 退出、窗口关闭、读取失败、摄像头释放和窗口清理，所有断言通过。仓库仍没有保存自动化测试。
