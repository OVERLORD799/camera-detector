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
python main.py
```

程序默认打开索引为 0 的摄像头。按 Q/q 或关闭画面窗口可以退出。

当前代码已经包含基本采集、显示和资源清理流程，但仓库中尚无本版本的硬件运行验证记录。FPS 显示和保存当前帧仍是待实现目标。

## 工程文档

- [项目目标](ENGINEERING_LOG/goal.md)
- [当前架构](ENGINEERING_LOG/architecture.md)
- [2026-08-30：资源生命周期](ENGINEERING_LOG/2026-08-30.md)
- [2026-08-31：Camera 抽象](ENGINEERING_LOG/2026-08-31.md)
