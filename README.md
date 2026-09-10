# Camera Detector

一个使用 OpenCV 读取并显示电脑摄像头画面的练习项目。

## 环境

- Python 3.11.16
- 依赖见 `requirements.txt`

安装依赖：

```powershell
python -m pip install -r requirements.txt
```

## 运行

```powershell
python code/main.py
```

程序默认打开索引为 0 的摄像头。按 Q/q 或关闭画面窗口可以退出，按 S/s 可以将当前带有 FPS 信息的画面转为灰度图并保存到 `frames/`。

当前代码已经包含基本采集、显示、资源清理、每秒平均 FPS 显示和当前帧保存流程。实际运行已验证 Q/q 与窗口关闭的退出和资源释放，已生成的摄像头帧验证了 FPS 文字叠加与 JPEG 保存。无效设备索引与可控读取失败测试也已确认程序能正常退出并释放资源。

## 工程文档

- [项目目标](ENGINEERING_LOG/goal.md)
- [当前架构](ENGINEERING_LOG/architecture.md)
- [2026-08-30：资源生命周期](ENGINEERING_LOG/2026-08-30.md)
- [2026-08-31：Camera 抽象](ENGINEERING_LOG/2026-08-31.md)
- [2026-09-03：每秒平均 FPS](ENGINEERING_LOG/2026-09-03.md)
- [2026-09-06：完成预览、FPS、当前帧保存与失败路径验证](ENGINEERING_LOG/2026-09-06.md)
- [2026-09-10：封装 FPS 与帧保存状态并加入灰度处理](ENGINEERING_LOG/2026-09-10.md)
