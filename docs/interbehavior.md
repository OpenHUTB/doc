# 虚拟现实驾驶模拟器
欢迎来到针对行为和交互研究的虚拟现实驾驶模拟器。

![](./img/pedestrian/VR_demo.gif)


该模块扩展了 [`Carla`](https://github.com/OpenHUTB/carla) 模拟器，增加了虚拟现实集成、第一人称可操纵的自主车辆、眼动追踪支持和多种沉浸感增强功能。

如果您有任何疑问，希望我们的常见问题解答 [F.A.Q. 维基页面](https://github.com/HARPLab/DReyeVR/wiki/Frequently-Asked-Questions) 和 [问题页面](https://github.com/HARPLab/DReyeVR/issues?q=is%3Aissue+is%3Aclosed) 可以解答其中的一些问题。详细请查看 [视频演示(YouTube)](https://www.youtube.com/watch?v=yGIPSDOMGpY) 。


## 亮点
### 自主车辆
[集成 SteamVR](https://github.com/ValveSoftware/steamvr_unreal_plugin/tree/4.23) 的完全可驾驶**虚拟现实自主车辆**（参见 [EgoVehicle.h](https://github.com/OpenHUTB/carla/blob/OpenHUTB/Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/EgoVehicle.h) ）

- SteamVR HMD 头部跟踪 (朝向 & 位置)

- 我们已经使用以下设备进行了测试：
  
  | 设备 | 虚拟现实支持             | 眼动跟踪 | 操作系统 |
  |--------------------| -- | --- | --- |
  | [HTC Vive Pro Eye](https://business.vive.com/us/product/vive-pro-eye-office/) | ✓                  | ✓ | Windows, Linux |
  | [Quest 2](https://www.oculus.com/quest-2/) | ✓ | × | Windows |
  
  - 虽然我们还没有测试其他耳机，但如果 SteamVR 支持，它们仍然可以用于基本的虚拟现实用途（非眼动追踪）。
  - 由于我们使用 [SRanipal](https://forum.htc.com/topic/5641-sranipal-faq/) 作为眼动追踪器 SDK，因此眼动追踪目前**仅**支持 HTC Vive Pro Eye。我们很乐意通过贡献添加其他 SDK 来支持更多设备。
- 车辆控制：
  - 通用键盘 WASD + 鼠标，按`Z`表示倒车
  - 使用此开源 [LogitechWheelPlugin](https://github.com/HARPLab/LogitechWheelPlugin) 支持 Logitech 方向盘
    - 包括方向盘的力反馈。
    - 我们使用了 [Logitech G923 赛车方向盘和踏板](https://www.logitechg.com/en-us/products/driving/driving-force-racing-wheel.html)
      - 虽然我们可以在没有经过测试的情况下保证开箱即用的功能，但是可以在 [此处](https://github.com/HARPLab/LogitechWheelPlugin/blob/master/README.md) 找到受支持设备的完整列表。
  - 编辑器模式下按`2`（非数字键）表示脱离第一视角车辆控制，按`1`表示进入第一视角车辆控制。

- 逼真的（可参数化的）后视镜和侧视镜

    - 警告：非常耗性能

- 车辆仪表板：

    - 速度计（默认单位为英里/小时）

    - 档位指示器：显示的 D(Drive) 为前进档、R(Reverse) 为倒档，按键盘`Z`进行切换

    - 转向信号：按`Q`为左转向、按`E`为右转向

- 动力学方向盘

    - 可调节参数，响应转向输入

    - 请在 [此处](interbehavior/Tutorials/Model.md) 查看我们的相关文档

- “以自我为中心”的音频

    - 响应式发动机转速（基于油门）

    - 转向灯咔嗒声

    - 档位切换

    - 碰撞

- 与现有的 [Carla PythonAPI](https://carla.readthedocs.io/en/0.9.13/python_api/) 和 [ScenarioRunner](https://github.com/carla-simulator/scenario_runner/tree/v0.9.13) 完全兼容

    - 进行了微小修改。请参阅 [使用](interbehavior/Usage.md) 文档。

- 与 [Carla Recorder 和 Replayer](https://carla.readthedocs.io/en/0.9.13/adv_recorder/) 完全兼容

- 能够将控制权移交给/接管 Carla 的 AI 轮式车辆控制器

- 基于 Carla 的语义分割相机（参见 [`着色器`](interbehavior/Shaders.md) ）


### 自我传感器 <span id="ego_sensor"></span>
与 Carla 兼容的**自主车辆传感器**（参见 [EgoSensor.h](https://github.com/OpenHUTB/carla/blob/OpenHUTB/Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/EgoSensor.h) ）是一种“隐形传感器”，可跟踪以下信息：

- 使用 [HTC Vive Pro Eye](https://enterprise.vive.com/us/product/vive-pro-eye-office/) VR 耳机进行实时**眼动跟踪** 
  - 眼动仪数据包括：
    - 时间信息（基于耳机、世界和眼动仪）
    - 三维眼睛凝视光线（左、右及组合）
    - 2D 瞳孔位置（左和右）
    - 瞳孔直径（左和右）
    - 眼睛睁开度（左和右）
    - 世界中的焦点及命中的参与者信息
    - 完整列表请参见 [DReyeVRData.h:EyeTracker](https://github.com/OpenHUTB/carla/blob/a67930eb9bc3ce2a7f1ffb15efc5fad5efaa3e75/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/DReyeVRData.h#L110)
  - 实时眼标线可视化
- 实时用户输入（油门、转向、刹车、转向信号等）
- 基于摄像头的图像（截图）帧捕获
  - 由于性能密集程度高，通常用于重播而不是实时。
- 与 LibCarla 数据序列化完全兼容，可流式传输到 PythonAPI 客户端（参见 [LibCarla/Sensor](https://github.com/OpenHUTB/carla/tree/OpenHUTB/LibCarla/source/carla/sensor) ）
  - 我们还测试并验证了对（`rospy`）ROS 集成传感器数据流的支持

### 其他补充：
- 用于一次性运行时参数的自定义 DReyeVR 配置文件。请参阅 [DReyeVRConfig.ini](https://github.com/OpenHUTB/carla/blob/OpenHUTB/Unreal/CarlaUE4/Config/DReyeVRConfig.ini) 

    - 特别适用于无需重新编译所有内容即可更改参数。

    - 使用标准 C++ IO 管理来读取文件，对性能的影响最小。请参阅 [DReyeVRUtils.h](https://github.com/OpenHUTB/carla/blob/OpenHUTB/Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/DReyeVRUtils.h) 。

- 世界环境音频

    - 鸟鸣声、风声、烟雾声等（参见 [声音文档](interbehavior/Tutorials/Sounds.md) ）

- 非自我为中心的音频（非自主车辆的发动机转速）

- 同步重放并逐帧捕获以进行事后分析（参见 [使用文档](interbehavior/Usage.md) ）

- 记录器/重放器媒体功能

    - 添加了游戏内键盘命令播放/暂停/前进/后退/等。

- [用于自然导航的静态环境方向标志](interbehavior/Tutorials/Signs.md)

- 将天气信息添加到 Carla 记录器/重放器/查询中（参见此 [Carla PR](https://github.com/carla-simulator/carla/pull/5235) ）

- 自定义动态 3D 参与者，具有全面录制支持（例如方向的头显指示器、AR 边界框、视觉目标等）。有关更多信息，请参阅 [VR 驾驶中自定义参与者](interbehavior/Tutorials/CustomActor.md) 。

- （仅调试）注视点渲染可通过注视感知（或固定）可变速率着色来提高性能


## 安装/构建
查看 [安装文档](interbehavior/Install.md) :

- 在可运行的 `Carla` 存储库上安装并构建 `DReyeVR` 。

- 下载 `DReyeVR` 所需的插件，以实现以下精彩功能：

  - 眼动跟踪 (Sense Robot Anipal, SRanipal)

  - 方向盘/踏板 (Logitech)

- 为 DReyeVR PythonAPI 设置 `conda` 环境


## 操作系统兼容性

| 操作系统    | 虚拟现实               | 眼动跟踪 | 音频            | 键盘+鼠标         | 赛车方向盘 | 注视点渲染（编辑器）         |
|---------|--------------------|------|--------------------|--------------------| -- |--------------------|
| Windows | ✓                  | ✓    | ✓ | ✓ | ✓ | ✓ |
| Linux   | ✓ | × | ✓ | ✓ | × | ×                |
| MacOS   | ×                | ×  | ✓ | ✓ | × | ×                |

- 虽然建议使用 Windows（10）来优化虚拟现实支持，但除了眼动跟踪和硬件集成（它们仅依赖于 Windows）之外，我们所有的工作都转移到了 Linux 系统。 
  - 不幸的是，眼动追踪固件是专有的，无法在 Linux 上运行
    - 由于 [HTC SRanipal SDK](https://developer.vive.com/resources/knowledgebase/vive-sranipal-sdk/) 和 Tobii 的 SDK 之间存在一些专有依赖关系，因此目前仅支持 Windows。对 HTC Vive Pro 眼动追踪的 Linux 讨论感兴趣的人可以关注 [ 此处 (Vive)](https://forum.vive.com/topic/6994-eye-tracking-in-linux/) 、[此处 (Vive)](https://forum.vive.com/topic/7012-vive-pro-eye-on-ubuntu-16-or-18/) 和 [此处 (Tobii)](https://developer.tobii.com/community/forums/topic/vive-pro-eye-with-stream-engine/) 的主题。
  - 此外，我们使用的 [LogitechWheelPlugin](https://github.com/HARPLab/LogitechWheelPlugin) 目前仅支持 Windows。不过，根据 [Arch Wiki](https://wiki.archlinux.org/title/Logitech_Racing_Wheel) ，应该可以在 Linux 上使用 G923。
- 此外，尽管 Carla 并未正式支持 MacOS，但我们在 Apple Silicon 机器上进行了开发，并且拥有 Carla + UE4.26 的活跃分支，支持 MacOS 12+。请注意，这主要用于开发，因为它是迄今为止最受限制的系统。



## 文档 & 指南

使用方法：
直接启动：车辆控制（带声音）、带参数启动原始模式

- 请参阅 [安装步骤](interbehavior/Install.md) 来安装和构建 VR 驾驶
- 请参阅 [使用 VR 驾驶](interbehavior/Usage.md) 了解如何使用我们提供的 VR 驾驶功能
- 请参阅 [开发](interbehavior/Development.md) 以开始 VR 驾驶开发并添加新功能
- 请参阅多个 VR 驾驶教程，包括：[自定义参与者](./interbehavior/Tutorials/CustomActor.md)、[添加自己的 EgoVehicle](./interbehavior/Tutorials/CustomEgo.md) 、[细节级别模式](./interbehavior/Tutorials/LODs.md) 、[修改车辆模型](./interbehavior/Tutorials/Model.md) 、[设置VR模式](./interbehavior/Tutorials/SetupVR.md) 、[添加定制的标志](./interbehavior/Tutorials/Signs.md) 、[添加和使用声音](./interbehavior/Tutorials/Sounds.md)。
- [自定义自主车辆](interbehavior/Tutorials/CustomEgo.md)
- [配置可驾驶的 VR 玩家](./interbehavior/VRPlayer.md)
- [问题分析](interbehavior/implementation.md) 
- [模块分析](modules/DReyeVR.md)
- [常见问题](./interbehavior/FAQ.md)

### 切换为 Carla 模式

将 [Unreal\CarlaUE4\Config\DefaultEngine.ini](https://github.com/OpenHUTB/hutb/blob/hutb/Unreal/CarlaUE4/Config/DefaultEngine.ini) 中的 `VR mode` 注释掉，并打开 `Carla mode`。


## 引用

如果你想使用该工作，请参考对应的 [论文](https://arxiv.org/abs/2201.01931):

- 此 repo 包含来自 Hewlett-Packard Development Company, LP 的一些代码。请参阅 [nvidia.ph](Tools/Diagnostics/collectl/nvidia.ph) 。

