# Camera Detector Goals

## 状态定义

- `Not Started`：尚未开始。
- `In Progress`：已有实现或工作进展，但要求的行为或验证尚未全部完成。
- `Blocked`：存在明确阻塞条件。
- `Completed`：实现存在、要求的行为有效，并已完成必要验证。

## 当前目标

当前没有进行中的目标。

## 完成标准

Goal 只有在实现存在、请求的行为有效且必要验证完成后才能标记为 `Completed`。仅通过代码静态检查时，应保留为 `In Progress`，或明确说明该 Goal 本身只要求结构变化。

## 历史已完成目标

| Goal | 状态 | 完成依据 |
| --- | --- | --- |
| 将摄像头采集职责从应用流程中分离 | Completed | 2026-08-31 静态检查确认 `main.py` 不直接使用 `VideoCapture`，设备操作集中在 `Camera`；见 [日志](2026-08-31.md) |
| 完成可靠的摄像头预览流程 | Completed | 实际测试确认设备可打开并持续显示画面，Q/q 与窗口关闭均能退出并释放摄像头；见 [日志](2026-09-06.md) |
| 实时显示 FPS | Completed | 代码将平均 FPS 绘制到画面；实际保存的摄像头帧中可见 `FPS: 29.9` 和 `FPS: 30.0`；见 [日志](2026-09-06.md) |
| 保存当前帧 | Completed | S/s 保存逻辑已实现；生成的 JPEG 文件已确认可以正常读取；见 [日志](2026-09-06.md) |
| 验证失败路径 | Completed | 无效设备索引与可控读取失败测试均确认程序退出并释放资源；见 [日志](2026-09-06.md) |
| 理解帧数据与 Camera 接口契约 | Completed | 实际验证确认成功帧是 BGR 排列的 NumPy `ndarray`，形状为 `(H, W, 3)`、数据类型为 `uint8`；读取失败时返回 `(False, None)` |
| 理解并实现最简单的单帧图像处理 | Completed | 实际验证确认 BGR 帧经 `cv2.cvtColor()` 转换后由 `(H, W, 3)` 变为 `(H, W)`，保持 `uint8`，灰度 JPEG 可正常读取；见 [日志](2026-09-10.md) |
| 将 FPS 与当前帧保存职责从 `main.py` 分离 | Completed | `FPSCounter` 封装 FPS 状态、计算与绘制，`FrameSaver` 封装帧保存状态与行为；可控回归测试已通过；见 [日志](2026-09-10.md) |
| 将图像处理职责从 `main.py` 分离 | Completed | `processor.py` 接收 BGR `ndarray` 并返回灰度图，`main.py` 只调用处理接口；真实摄像头灰度预览与退出/清理回归验证已通过；见 [日志](2026-09-10-processor.md) |
