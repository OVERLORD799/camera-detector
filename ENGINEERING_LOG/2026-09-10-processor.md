# 2026-09-10：分离图像处理职责并验证灰度预览

## 背景

灰度转换最初由 `FrameSaver` 完成，只有保存路径使用处理后的图像，实时预览仍使用 BGR 帧。为了让图像处理与流程控制、文件保存保持独立，需要建立专门的处理模块。

## 实现

- 新增 `code/processor.py`，`grey(frame)` 接收 BGR NumPy 帧，使用 `cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)` 返回单通道灰度图。
- `code/main.py` 在读取成功后调用处理器，并将返回的灰度帧传给 FPS 绘制、窗口显示和帧保存。
- `code/save_module.py` 不再负责灰度转换，只保存已处理的帧和维护文件序号。
- `code/main.py` 不直接调用 `cv2.cvtColor()`。

## 验证

- 可控 BGR 输入的形状为 `(48, 64, 3)`、数据类型为 `uint8`；处理器返回 `(48, 64)`、`uint8` 灰度图。
- 可控主循环测试中，传给 `imshow()` 的每张图像都是二维灰度帧，S 保存后的 JPEG 也能以二维灰度图读回。
- 可控测试覆盖 Q 退出、窗口关闭和读取失败；各路径均调用摄像头释放和 `destroyAllWindows()`。
- 使用 `camera-detector` Conda 环境运行真实摄像头 30 帧，所有传给 `imshow()` 的帧均为 `(480, 640)` 灰度图。
- 真实预览通过 Q 路径退出，`Camera.release()` 已调用；测试进程与可控测试均以退出码 0 结束。

上述检查未保存为仓库内的自动化测试。

## 结果

“将图像处理职责从 `main.py` 分离”的实现、实时灰度预览和必要回归验证均已完成，目标记为 `Completed`。

## 已知限制

- `FrameSaver.save_frame()` 的 `frame_type` 参数在当前实现中已不再使用。
- 当前处理流程只支持 BGR 到灰度的单一转换。
