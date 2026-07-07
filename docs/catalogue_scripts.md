# 脚本目录

本文档概述了 OpenHUTB Python API 的可用示例 Python 脚本和实用程序。您可以使用这些脚本来学习 OpenHUTB 的 Python API、执行实用功能或进行测试，并以此为基础编写自己的脚本。以下示例脚本位于 HUTB 代码库或软件包的 [PythonAPI/examples](https://github.com/OpenHUTB/hutb/tree/hutb/PythonAPI/examples) 目录中。

* [手动控制](#manual-control)
* [自动控制](#automatic-control)
* [生成交通流](#generate-traffic)
* [逆 AI 交通流](#inverted-ai-traffic)
* [开始记录](#start-recording)
* [开始重放](#start-replaying)
* [Open3D LIDAR](#open3d-lidar)
* [边界框](#bounding-boxes)
* [非渲染模式](#no-rendering-mode)
* [动态天气](#dynamic-weather)
* [激光雷达数据投影到相机平面](#lidar-to-camera)
* [载具画廊](#vehicle-gallery)

---

## 手动控制

* 脚本文件名：[manual_control.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/manual_control.py)
* 示例使用：`python3 manual_control.py --res 800x600 --sync`

该脚本允许用户通过键盘在 OpenHUTB 地图上手动控制车辆，并在 Pygame 窗口中可视化显示传感器输出。对于初次接触 OpenHUTB 的用户而言，这是探索 OpenHUTB 地图以及理解车辆与传感器行为的首选入门脚本之一。此外，当 OpenHUTB 的核心功能（如渲染、物理模拟、交通系统或感知模块）发生变更，且这些变更可能影响外观、驾驶行为或传感器输出时，该脚本也是进行测试与调试的有力工具。

该脚本会在地图上随机选择的生成点处生成一辆载具（即“自车”），并允许用户通过方向键或 WASD 键对其进行手动控制。此外，还提供其他键盘快捷键，用于切换载具、换挡、更改传感器类型、开始录制以及执行多种其他功能。

您可以将手动控制与[生成交通流脚本](#generate-traffic)结合使用，以驾驶车辆穿梭于车流之中。请务必先启动“生成交通流”脚本，再启动手动控制。切勿尝试以同步模式同时运行这两个脚本；在同步模式下，应当仅有一个客户端在运行。默认情况下，手动控制以异步模式运行，而“生成交通流”脚本以同步模式运行，因此在默认的同步配置下，两者能够顺畅协作。


### 键盘命令

| 键 | 控制 |
|-----|---------|
| W, &uarr;    | 油门 |
| S, &darr;    | 刹车 |
| A/D, &larr;, &rarr; | 向左/向右转向 |
| Q            | 切换倒档 |
| Space        | 手刹 |
| P            | 切换自动驾驶 |
| M            | 切换手动变速箱 |
| ,/.          | 升档/降档 |
| CTRL + W     | 切换至 60 km/h 恒速模式 |
| L            | 切换至下一种灯光类型 |
| SHIFT + L    | 切换远光灯 |
| Z/X          | 切换右/左转向灯 |
| I            | 切换车内照明灯 |
| TAB          | 更改传感器位置 |
| ` or N       | 下一个传感器 |
| [1-9]        | 切换至传感器 [1-9] |
| G            | 切换雷达可视化 |
| C            | 更改天气（Shift+C 反向） |
| Backspace    | 更换车辆 |
| O            | 打开/关闭车辆所有车门 |
| T            | 切换车辆遥测数据 |
| V            | 选择下一个地图图层（Shift+V 反向） |
| B            | 加载当前选定的地图图层（按 Shift+B 卸载） |
| R            | 切换将图像录制到磁盘的功能 |
| CTRL + R     | 切换模拟录制（将覆盖之前的录制内容） |
| CTRL + P     | 开始回放上次记录的模拟 |
| CTRL + +     | 将回放的开始时间增加 1 秒（按住 SHIFT 键则增加 10 秒） |
| CTRL + -     | 将回放的开始时间减少 1 秒（按住 SHIFT 键则减少 10 秒） |
| F1           | 切换 HUD |
| H/?          | 切换帮助 |
| ESC          | 退出 |

### 命令行参数

该手动控制脚本包含多个用于配置的命令行参数：

| 参数 | 简写形式 | 默认值 | 描述 |
|----------|------------|---------|-------------|
| --verbose | -v | - | 打印调试信息 |
| --host | -h | 127.0.0.1 | 主机 IP 地址 |
| --port | -p | 2000 | 用于 Carla 客户端的 TCP 端口 |
| --autopilot | -a | 未激活 | 启用本车自动驾驶功能 |
| --res |  | 1280x720 | 所有摄像头传感器的像素分辨率 |
| --filter |  | vehicle.* | 按车型筛选 |
| --generation |  | 2 | 指定车型世代 |
| --rolename |  | hero | 分配给自车（ego vehicle）的角色名称 |
| --gamma |  | 2.2 | RGB 相机的伽马校正 |
| --sync |  | 未激活 | 以同步模式激活脚本 |

### 脚本变体

针对不同用途，有多种手动控制脚本版本。它们都使用相同的快捷键和大部分相同的命令行参数，有些版本还包含额外的命令行参数。

#### Chrono

* 脚本文件名：[manual_control_chrono.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/manual_control_chrono.py)

该脚本启动基于 Chrono 物理引擎的手动控制模式，并使用 OpenHUTB 仓库/软件包中 [Co-Simulation/Chrono/Vehicles](https://github.com/OpenHUTB/hutb/tree/hutb/Co-Simulation/Chrono/Vehicles) 目录下的轿车（Sedan）动力总成参数。

#### 鱼眼相机

* 脚本文件名：[manual_control_fisheye.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/manual_control_fisheye.py)

此脚本以手动控制的方式启动鱼眼相机模型。此脚本与[手动控制](#manual-control)脚本具有相同的快捷键和命令行参数。它还包含一些用于相机模型参数的额外命令行参数：

| 参数                | 简写形式 | 默认                                                                            | 描述                                                                  |
|-------------------|------------|-------------------------------------------------------------------------------|---------------------------------------------------------------------|
| --fov             |  | 90.0                                                                          | 相机视场角(field of view angle)                                          |
| --fov_mask        |  | 未激活                                                                    | 视场之外的掩膜像素                                                           |
| --fov_fade_size   |  | 0.0                                                                           | 视场边缘的衰减，给定增宽因子                                                      |
| --model           |  | perspective                                                                   | 相机模型: <br>透视投影 <br>等距投影 <br>等积投影 <br>正射投影 <br>立体投影 <br>kannala-brandt |
| --k0              |  | 0.0831                                                                        | k0 Kannala-Brandt 参数                                                |
| --k1              |  | 0.0111                                                                        | k1 Kannala-Brandt 参数                                         |
| --k2              |  | 0.00858                                                                       | k2 Kannala-Brandt 参数                                         |
| --k3              |  | 0.000854                                                                      | k3 Kannala-Brandt 参数                                         |
| --equirectangular |  | 未激活                                                                    | 等距柱状投影                                          |
| --perspective     |  | 未激活                                                                    | 透视投影                                              |
| --longitude_shift | 0.0 | 将等距柱状投影模型的视角中心移动一定角度 |

#### 方向盘

* 脚本名：[manual_control_steeringwheel.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/manual_control_steeringwheel.py)

该脚本演示了如何通过 Pygame 的 Joystick 模块，利用外部方向盘来控制 OpenHUTB。

---

## 自动控制

* 脚本文件名：`automatic_control.py`
* 示例使用：`python3 automatic_control.py --agent Basic --loop`

自动控制功能利用 Carla Agents 库，实现车辆在 OpenHUTB 地图上的自动驾驶。Carla Agents 库包含多种用于演示目的的简单驾驶智能体实现。Pygame 窗口用于可视化展示车辆的摄像机画面。

| 参数 | 简写形式 | 默认值 | 描述 |
|----------|------------|---------|-------------|
| --verbose | -v |  | 打印调试信息 |
| --host | -h | 127.0.0.1 | 主机 IP 地址 |
| --port | -p | 2000 | 用于 Carla 客户端的 TCP 端口 |
| --res |  | 1280x720 | 所有摄像头传感器的像素分辨率 |
| --filter |  | vehicle.* | 按车型筛选 |
| --generation |  | 2 | 指定车型世代 |
| --sync |  | 未激活 | 以同步模式激活脚本 |
| --loop | -l | 未激活 | 到达上一个目的地后，设定一个新的随机目的地。 |
| --agent | -a | | 代理类型, "Behavior", "Basic" 或 "Constant" |
| --behavior | -b | | 代理行为, "cautious", "normal" 或 "aggressive" |
| --seed| -s |  | 用于重复执行的种子值 |

---

## 生成交通流

* 脚本文件名：[generate_traffic.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/generate_traffic.py)
* 示例使用：`python3 generate_traffic.py -n 100`

该脚本会在选定的 OpenHUTB 地图上生成不同密度的交通流，同时也会生成行人。交通流和行人的密度可以通过命令行参数进行选择。该交通流生成脚本可以与手动控制结合使用，使车辆能够在已生成交通流的地图上行驶。

### 命令行参数

| 参数 | 简写形式 | 默认 | 描述 |
|----------|------------|---------|-------------|
| --number-of-vehicles | -n | 30 | 要生成的车辆数量 |
| --number-of-walkers | -w | 10 | 要生成的行人数量 |
| --host | -h | 127.0.0.1 | 主机 IP 地址 |
| --port | -p | 2000 | 用于 Carla 客户端的 TCP 端口 |
| --safe |  |  | 不要生成容易引发事故的载具 |
| --filterv |  | vehicle.* | 按字符串筛选车型 |
| --filterw |  | walker.pedestrian.* | 按字符串筛选行人模型 |
| --generationv |  | All | 指定车辆世代：“1”、“2”或“All”（全部） |
| --generationw |  | All | 指定行人生成世代，“1”、“2”或“全部” |
| --tm-port |  | 8000 | 指定交通管理器的 TCP 端口 |
| --asynch |  | 未激活 | 以同步模式运行脚本 |
| --hybrid |  | 未激活 | 为交通管理器激活混合模式 |
| --seed | -s |  | 用于随机生成的整数种子（激活交通管理器的确定性模式） |
| --seedw |  |  | 行人模块的整数种子 |
| --car-lights-on | | False | 启用由交通管理器进行的自动交通灯管理 |
| --hero | | False | 提名一款英雄载具 |
| --respawn | | False | 在大地图上自动重置处于休眠状态的载具 |
| --no-rendering | | 未激活 | 为 Carla 服务器启用无渲染模式 |

---

## 逆 AI 交通流

* 脚本文件名：[invertedai_traffic.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/invertedai_traffic.py)
* 示例使用：`python3 invertedai_traffic.py -iai-key <token> --record`

该脚本演示了如何启动由 [Inverted AI](https://www.inverted.ai/home) 的 AI 交通引擎驱动的 Carla 交通仿真。您需要提供 Inverted AI API 密钥；请前往其官网[注册](https://www.inverted.ai/portal/login)以获取密钥。


### 命令行参数

| 参数 | 简写形式 | 默认值 | 描述 |
|----------|------------|---------|-------------|
| --number-of-vehicles | -n | 30 | 要生成的车辆数量 |
| --number-of-walkers | -w | 10 | 要生成的行人数量 |
| --host | -h | 127.0.0.1 | 主机 IP 地址 |
| --port | -p | 2000 | 用于 Carla 客户端的 TCP 端口 |
| --safe |  |  | 不要生成容易引发事故的载具。 |
| --filterv |  | vehicle.* | 按字符串筛选车型 |
| --filterw |  | walker.pedestrian.* | 按字符串筛选行人模型 |
| --generationv |  | All | 指定载具的世代：“1”、“2”或“All”（全部） |
| --generationw |  | All | 指定行人的世代：“1”、“2”或“All”（全部） |
| --seed | -s |  | 用于随机生成的整数种子（激活交通管理器的确定性模式） |
| --hero |  | 未激活 | 将其中一辆载具设为英雄单位。 |
| --iai-key | | | Inverted AI API 密钥 |
| --record | | 未激活 | 使用 Carla 记录器记录仿真过程。 |
| --sim-length | | 60 | 模拟时长（秒） |
| --location | | carla:Town10HD | 用于模拟仿真的 IAI 格式地图  |
| --capacity | | 100 | 四叉树叶节点分裂阈值 |
| --width | | 250 | 初始化交通的区域宽度 |
| --height | | 250 | 触发交通流初始化的区域高度 |
| --map-center | | -50,20 | 待初始化的区域中心 |
| --iai-async | | 未激活 | 异步调用 IAI DRIVE |
| --api-model | | bI5p | IAI API 模型版本 |
| --iai-log | | 未激活 | 存储联合模拟的日志文件 |
| --iai-waypoint-distance | | 15 | IAI 智能体距离下一个航点的距离 |
| --iai-waypoint-detection-threshold | | 2 | 视为已完成的航点距离 |
| --iai-max-distance-away | | 20 | 为代理设置新航点前的最大距离 |

---

## 开始记录

* 脚本文件名：[start_recording.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/start_recording.py)
* 示例使用：`python3 start_recording.py`

该脚本演示了如何使用 Carla 记录器。脚本会生成一些交通流，并利用[Carla 记录器](foundations.md#recorder)将车辆的移动情况记录为日志。

| 参数 | 简写形式 | 默认值 | 描述 |
|----------|------------|---------|-------------|
| --host | -h | 127.0.0.1 | 主机 IP 地址 |
| --port | -p | 2000 | 用于 Carla 客户端的 TCP 端口 |
| --number-of-vehicles | -n | 30 | 要生成的载具数量 |
| --delay | -d | 2.0 | 两次生成之间的延迟时间（秒） |
| --safe |  |  | 不要生成容易引发事故的载具。 |
| --recorder_filename | -f | test1.log | 记录日志的文件名 |
| --recorder_time | -t | 0 | 记录时长 |

---

## 开始重放

* 脚本文件名：[start_replaying.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/start_replaying.py)
* 示例使用：`python3 start_replaying.py -f carla.log` 

该脚本演示了如何使用 Carla 重放器。  

| 参数 | 简写形式 | 默认值 | 描述 |
|----------|------------|---------|-------------|
| --host | -h | 127.0.0.1 | 主机 IP 地址 |
| --port | -p | 2000 | 用于 Carla 客户端的 TCP 端口 |
| --duration | -d | 0.0 | Duration to replay |
| --recorder_filename | -f | test1.log | 记录日志的文件名 |
| --camera | -c | 0 | 摄像机跟随具有指定整数 ID 的参与者。 |
| --time-factor | -x | 1.0 | 播放时间倍率，例如 2.0 表示双倍速度 |
| --ignore-hero | -i | 未激活 | 忽略英雄载具 |
| --move-spectator |  | 未激活 | 移动观察者相机 |
| --top-view |  | 未激活 | 激活俯视鸟瞰视图 |
| --spawn-sensors | | 未激活 | 在重放模拟中生成传感器 |
| --map-override | -m | | 用于替换日志文件中 OpenDRIVE 名称的地图名称 |

---

## Open3D LIDAR

* 脚本文件名：`open3d_lidar.py`
* 示例使用： `python3 open3d_lidar.py --semantic --points-per-second 100000` 

该脚本演示了由 Carla 的激光雷达（LIDAR）传感器和语义激光雷达传感器生成的点云数据的可视化效果。可视化过程使用了 [Open3D 库](https://www.open3d.org)，该库因其高效的点云可视化性能而受到 Carla 开发团队的推荐。

### 命令行参数

| 参数 | 简写形式 | 默认值 | 描述 |
|----------|------------|---------|-------------|
| --host | -h | 127.0.0.1 | 主机 IP 地址 |
| --port | -p | 2000 | 用于 Carla 客户端的 TCP 端口 |
| --no-rendering |  |  | 启用无渲染模式 |
| --semantic |  | 未激活 | 使用语义激光雷达 |
| --no-noise |  | 未激活 | 不要增加噪音和丢弃 |
| --no-autopilot |  | 未激活 | 禁用自动驾驶功能，车辆保持静止。 |
| --show-axis |  | 未激活 | 显示笛卡尔坐标轴 |
| --filter |  | vehicle.* | 按字符串筛选车型 |
| --upper-fov |  | 15.0 | 激光雷达的上方视场角（以度为单位） |
| --lower-fov |  | -25.0 | 激光雷达视场角（以度为单位）的下限值 |
| --channels |  | 64.0 | 激光雷达通道数 |
| --range |  | 100.0 | 激光雷达的最大量程（单位：米） |
| --points-per-second |  | 500000 | 每秒激光雷达点数 |
| -x |  | 0.0 | 激光雷达传感器的 X 轴偏移量 |
| -y |  | 0.0 | 激光雷达传感器的 Y 轴偏移量 |
| -z |  | 0.0 | 激光雷达传感器的 Z 轴偏移量 |

---

## 边界框

* 脚本文件名：[bounding_boxes.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/bounding_boxes.py)
* 示例使用：`python3 bounding_boxes.py -d 100` 

该脚本演示了如何通过 Python API 获取 3D 和 2D 边界框，并将其投影到相机视图平面上进行可视化。此外，该脚本还支持将 3D 和 2D 边界框信息以 JSON 格式保存，并同步记录 PNG 格式的相机帧图像。边界框在 Pygame 窗口中进行可视化显示；用户可以通过数字键“2”和“3”在 3D 和 2D 边界框视图之间进行切换。脚本允许通过命令行参数设置距离阈值，超出该阈值的边界框将不会被可视化或记录。

* **3D 边界框**: 3D 边界框的坐标是在车辆局部坐标系下给出的，以车辆边界框的中心为原点。为了进行可视化，利用相机的内参将 3D 边界框投影到相机平面上。这些坐标是根据每个参与者（actor）的 `bounding_box` 属性推导出来的。 

* **2D 边界框**: 2D 边界框以相机视平面的像素级图像坐标表示。这些 2D 边界框由实例分割图像得出。 

### 快捷键

| 键 | 控制 |
|-----|---------|
| R   | 开始记录边界框和摄像机帧  |
| 3 | 可视化 3D 边界框 |
| 2 | 可视化 2D 边界框 |
| ESC | 退出 |

### 命令行参数

| 参数 | 简写形式 | 默认值 | 描述 |
|----------|------------|---------|-------------|
| --host | -h | 127.0.0.1 | 主机 IP 地址 |
| --port | -p | 2000 | 用于 Carla 客户端的 TCP 端口 |
| --distance | -d | 50 | 边界框的距离阈值 |
| --res |  | 1280x720 | 相机传感器的像素分辨率（包括实例分割相机） |

---

## 非渲染模式

* 脚本文件名：[no_rendering_mode.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/no_rendering_mode.py)
* 示例使用：`python3 no_rendering_mode.py --res 800x600 --filter lincoln_mkz_2020`

为了有效地使用此脚本，您应该按如下方式以无渲染模式启动 Carla 服务器：

```sh
./CarlaUE4.sh --no-rendering
```

该脚本演示了如何在 Carla 的“无渲染模式”（no-rendering mode）下可视化地图与载具。该模式会禁用观察者视图（spectator view），从而使 Carla 能够以高性能配置运行，实现 100 FPS 或更高的帧率。脚本利用 Pygame 窗口，通过简单的边界框和二维路面来呈现场景的俯视二维视图。当在不使用传感器的情况下进行交通仿真，或利用第三方渲染器进行渲染时，这种方式非常实用。


### 快捷键

| 键 | 控制 |
|-----|---------|
| TAB          | 切换英雄模式 |
| 鼠标滚轮  | 放大 / 缩小 |
| 鼠标拖动   | 移动地图（仅限地图模式） |
| W, &uarr;    | 油门 |
| S, &darr;    | 刹车 |
| A/D, &larr;, &rarr; | 向左/向右转向 |
| Q            | 切换倒车 |
| 空格        | 手刹 |
| P            | 切换自动驾驶 |
| M            | 切换手动变速箱 |
| ,/.          | 升档/降档 |
| F1           | 切换 HUD |
| I            | 切换参与者 ID |
| H/?          | 切换帮助 |
| ESC          | 退出 |

### 命令行参数

| 参数 | 简写形式 | 默认值 | 描述 |
|----------|------------|---------|-------------|
| --verbose | -v |  | 打印调试信息 |
| --host | -h | 127.0.0.1 | 主机 IP 地址 |
| --port | -p | 2000 | 用于 Carla 客户端的 TCP 端口 |
| --res |  | 1280x720 | 显示窗口的像素分辨率 |
| --filter |  | vehicle.* | 按字符串筛选载具 |
| --map |  | None | 在指定地图上开始新的轮次 |
| --no-rendering |  | 未激活 | 关闭服务器端渲染 |
| --show-triggers |  | 未激活 | 显示交通信号灯的触发区域 |
| --show-connections |  | 未激活 | 显示航点连接 |
| --show-spawn-points |  | 未激活 | 显示推荐生成点 |

---

## 动态天气

* 脚本文件名：[dynamic_weather.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/dynamic_weather.py)
* 示例使用：`python3 no_rendering_mode.py --res 800x600 --filter lincoln_mkz_2020`

该脚本演示了如何在 Carla 运行时修改天气设置，从而实现在模拟过程中改变天气状况。


### 命令行参数

| 参数 | 简写形式 | 默认值 | 描述 |
|----------|------------|---------|-------------|
| --host | -h | 127.0.0.1 | 主机 IP 地址 |
| --port | -p | 2000 | 用于 Carla 客户端的 TCP 端口 |
| --speed |  | 1.0 | 天气变化速率 |

---

## 激光雷达数据投影到相机平面

* 脚本文件名：[lidar_to_camera.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/lidar_to_camera.py)
* 示例使用：`python3 lidar_to_camera.py --res 800x600 --points-per-second 50000`

该脚本演示了如何将激光雷达（LiDAR）点云投影到相机平面上。脚本会将包含投影点云的相机帧保存到运行该脚本的终端所在根目录下的 `_out` 文件夹中。


### 命令行参数

| 参数 | 简写形式 | 默认值 | 描述 |
|----------|------------|---------|-------------|
| --verbose | -v |  | 打印调试信息 |
| --host | -h | 127.0.0.1 | 主机 IP 地址 |
| --port | -p | 2000 | 用于 Carla 客户端的 TCP 端口 |
| --res |  | 1280x720 | 显示窗口的像素分辨率 |
| --frames |  | 500 | 要录制的帧数 |
| --dot-extent |  | 2 | 以像素为单位的激光雷达点范围 |
| --no-noise |  | 未激活 | 不要添加噪音和丢弃 |
| --upper-fov |  | 15.0 | 激光雷达视场角（以度为单位）的上限值 |
| --lower-fov |  | -25.0 | 激光雷达视场角（以度为单位）的下限值 |
| --channels |  | 64.0 | 激光雷达通道数 |
| --range |  | 100.0 | 激光雷达的最大量程（单位：米） |
| --points-per-second |  | 100000 | 每秒激光雷达点数 |

---

## 载具画廊

* 脚本文件名：[vehicle_gallery.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/vehicle_gallery.py)
* 示例使用：`python3 vehicle_gallery.py`

该脚本按顺序展示所有 OpenHUTB 车辆的 360 度视图。

