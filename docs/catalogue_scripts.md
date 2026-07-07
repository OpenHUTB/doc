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
* [LIDAR to camera](#lidar-to-camera)
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
| --seedw |  |  | Integer seed for the pedestrian module |
| --car-lights-on | | False | Enable automatic light managment by the TM |
| --hero | | False | Nominate a hero vehicle |
| --respawn | | False | Automatically respawn dormant vehicles in large maps |
| --no-rendering | | 未激活 | Activate no-rendering mode for the CARLA server |

---

## 逆 AI 交通流

* Script filename: `invertedai_traffic.py`
* Example usage: `python3 invertedai_traffic.py -iai-key <token> --record`

This script demonstrates how to launch a traffic simulation in CARLA driven by [Inverted AI's](https://www.inverted.ai/home) AI traffic engine. You will need to provide an Inverted AI API key, please [register](https://www.inverted.ai/portal/login) on the website to obtain one. 

### Command line arguments 

| Argument | Short form | Default | Description |
|----------|------------|---------|-------------|
| --number-of-vehicles | -n | 30 | Number of vehicles to spawn |
| --number-of-walkers | -w | 10 | Number of pedestrians to spawn |
| --host | -h | 127.0.0.1 | Host IP address |
| --port | -p | 2000 | TCP port for CARLA client |
| --safe |  |  | Don't spawn vehicles prone to accidents |
| --filterv |  | vehicle.* | Filter vehicle models with string |
| --filterw |  | walker.pedestrian.* | Filter pedestrian models with string |
| --generationv |  | All | Specify vehicle generation, "1", "2" or "All" |
| --generationw |  | All | Specify pedestrian generation, "1", "2" or "All" |
| --seed | -s |  | Integer seed for random generation (activates the deterministic mode for the TM) |
| --hero |  | 未激活 | Set one of the vehicles as a hero |
| --iai-key | | | Inverted AI API key |
| --record | | 未激活 | Record the simulation using the CARLA recorder |
| --sim-length | | 60 | Simulation length in seconds |
| --location | | carla:Town10HD | IAI formatted map for simulation  |
| --capacity | | 100 | Quadtree leaf split threshold |
| --width | | 250 | Width of area to initialize traffic |
| --height | | 250 | Height of area to initialize traffic |
| --map-center | | -50,20 | Center of the area to initialize |
| --iai-async | | 未激活 | Call IAI DRIVE asynchronously |
| --api-model | | bI5p | IAI API model version |
| --iai-log | | 未激活 | Store a log file for the co-simulation |
| --iai-waypoint-distance | | 15 | Distance to next waypoint for IAI agents |
| --iai-waypoint-detection-threshold | | 2 | Distance from waypoint to consider as completed |
| --iai-max-distance-away | | 20 | Max distance away before a new waypoint is set for an agent |

---

## 开始记录

* Script filename: `start_recording.py`
* Example usage: `python3 start_recording.py`

This script demonstrates how to use the CARLA recorder. Some traffic is spawned and the movement is recorded as a log by the [CARLA recorder](foundations.md#recorder). 

| Argument | Short form | Default | Description |
|----------|------------|---------|-------------|
| --host | -h | 127.0.0.1 | Host IP address |
| --port | -p | 2000 | TCP port for CARLA client |
| --number-of-vehicles | -n | 30 | Number of vehicles to spawn |
| --delay | -d | 2.0 | Delay in seconds between spawns |
| --safe |  |  | Don't spawn vehicles prone to accidents |
| --recorder_filename | -f | test1.log | Filename of recorded log |
| --recorder_time | -t | 0 | Recording duration |

---

## 开始重放

* Script filename: `start_recording.py`
* Example usage: `python3 start_recording.py -f carla.log` 

This script demonstrates how to use the CARLA replayer.  

| Argument | Short form | Default | Description |
|----------|------------|---------|-------------|
| --host | -h | 127.0.0.1 | Host IP address |
| --port | -p | 2000 | TCP port for CARLA client |
| --duration | -d | 0.0 | Duration to replay |
| --recorder_filename | -f | test1.log | Filename of recorded log |
| --camera | -c | 0 | Camera follows actor with given integer ID |
| --time-factor | -x | 1.0 | Time multiplier for playback, e.g. 2.0 for double speed |
| --ignore-hero | -i | 未激活 | Ignore the hero vehicle |
| --move-spectator |  | 未激活 | Move spectator camera |
| --top-view |  | 未激活 | Activate top-down birdseye view |
| --spawn-sensors | | 未激活 | Spawn sensors in the replaying simulation |
| --map-override | -m | | Map name to replace OpenDRIVE in log file |

---

## Open3D LIDAR

* Script filename: `open3d_lidar.py`
* Example usage: `python3 open3d_lidar.py --semantic --points-per-second 100000` 

This script demonstrates the visualization of LIDAR point clouds generated by the CARLA LIDAR sensor and semantic LIDAR sensor. The [Open3D library](https://www.open3d.org) is used for visualization and is recommended by the CARLA development team for performant point-cloud visualization. 

### Command line arguments

| Argument | Short form | Default | Description |
|----------|------------|---------|-------------|
| --host | -h | 127.0.0.1 | Host IP address |
| --port | -p | 2000 | TCP port for CARLA client |
| --no-rendering |  |  | Activate no-rendering mode |
| --semantic |  | 未激活 | Use semantic LIDAR |
| --no-noise |  | 未激活 | Don't add noise and dropoff |
| --no-autopilot |  | 未激活 | Disable's autopilot, vehicle remains motionless |
| --show-axis |  | 未激活 | Show the Cartesian axes |
| --filter |  | vehicle.* | Filter vehicle models with string |
| --upper-fov |  | 15.0 | LIDAR's upper field of view in degrees |
| --lower-fov |  | -25.0 | LIDAR's lower field of view in degrees |
| --channels |  | 64.0 | Number of LIDAR channels |
| --range |  | 100.0 | LIDAR's max range in meters |
| --points-per-second |  | 500000 | LIDAR points per second |
| -x |  | 0.0 | X-offset of LIDAR sensor |
| -y |  | 0.0 | Y-offset of LIDAR sensor |
| -z |  | 0.0 | Z-offset of LIDAR sensor |

---

## 边界框

* Script filename: `bounding_boxes.py`
* Example usage: `python3 bounding_boxes.py -d 100` 

This script demonstrates how to derive 3D and 2D bounding boxes through the Python API and visualize them projected into a camera viewplane. The script also has the facitlity to record both 3D and 2D bounding boxes in JSON format alongside camera frames in PNG. The bounding boxes are visualized in a Pygame window. The visualization can be switched between the 3D and 2D bounding boxes using the *2* and *3* number keys. A distance threshold can be set as a command line argument, bounding boxes beyond this threshold will not be visualized or recorded.

* **3D bounding boxes**: The 3D bounding box coordinates are given in the vehicle's local coordinate system, centered on the center of the vehicle's bounding box. For visualization the 3D bounding boxes are projected into the camera plane using the camera's intrinsic parameters. They are derived from each actor's `bounding_box` attribute.

* **2D bounding boxes**: The 2D bounding boxes are given in pixel-based image coordinates of the camera's viewplane. The 2D bounding boxes are derived from the instance segmentation image.

### Key commands 

| Key | Control |
|-----|---------|
| R   | Start recording bounding boxes and camera frames  |
| 3 | Visualize 3D bounding boxes |
| 2 | Visualize 2D bounding boxes |
| ESC | Quit |

### Command line arguments

| Argument | Short form | Default | Description |
|----------|------------|---------|-------------|
| --host | -h | 127.0.0.1 | Host IP address |
| --port | -p | 2000 | TCP port for CARLA client |
| --distance | -d | 50 | Distance threshold for bounding boxes |
| --res |  | 1280x720 | Pixel resolution of the camera sensor (including the instance segmentation camera) |

---

## 非渲染模式

* Script filename: `no_rendering_mode.py`
* Example usage: `python3 no_rendering_mode.py --res 800x600 --filter lincoln_mkz_2020`

To use this script effectively, you should launch the CARLA server in no-rendering mode like so:

```sh
./CarlaUE4.sh --no-rendering
```

This script demonstrates how to visualize the map and vehicles when using the no-rendering mode of CARLA, which disables the spectator view, allowing CARLA to run in a higher performance configuration. This enables frame rates at or above 100 FPS. A Pygame window visualizes a top-down 2D representation of the scene with simple bounding boxes and 2D road surfaces. This is useful when using CARLA without sensors for traffic simulation or driving 3rd party renderers.

### Key commands 

| Key | Control |
|-----|---------|
| TAB          | Toggle hero mode |
| Mouse Wheel  | Zoom in / zoom out |
| Mouse Drag   | Move map (map mode only) |
| W, &uarr;    | Throttle |
| S, &darr;    | Brake |
| A/D, &larr;, &rarr; | Steer left/right |
| Q            | Toggle reverse |
| Space        | Hand-brake |
| P            | Toggle autopilot |
| M            | Toggle manual transmission |
| ,/.          | Gear up/down |
| F1           | Toggle HUD |
| I            | Toggle actor ids |
| H/?          | Toggle help |
| ESC          | Quit |

### Command line arguments

| Argument | Short form | Default | Description |
|----------|------------|---------|-------------|
| --verbose | -v |  | Print debug info |
| --host | -h | 127.0.0.1 | Host IP address |
| --port | -p | 2000 | TCP port for CARLA client |
| --res |  | 1280x720 | Pixel resolution of the display window |
| --filter |  | vehicle.* | Filter vehicle models with string |
| --map |  | None | Start a new episode in a given map |
| --no-rendering |  | 未激活 | Switch off server rendering |
| --show-triggers |  | 未激活 | Show trigger boxes for traffic lights |
| --show-connections |  | 未激活 | Show waypoint connections |
| --show-spawn-points |  | 未激活 | Show recommended spawn points |

---

## 动态天气

* Script filename: `dynamic_weather.py`
* Example usage: `python3 no_rendering_mode.py --res 800x600 --filter lincoln_mkz_2020`

This script demonstrates how to modify the weather settings in CARLA during runtime, enabling changing weather conditions within a simulation. 

### Command line arguments

| Argument | Short form | Default | Description |
|----------|------------|---------|-------------|
| --host | -h | 127.0.0.1 | Host IP address |
| --port | -p | 2000 | TCP port for CARLA client |
| --speed |  | 1.0 | Rate of weather changes |

---

## LIDAR to camera

* Script filename: `lidar_to_camera.py`
* Example usage: `python3 lidar_to_camera.py --res 800x600 --points-per-second 50000`

This script demonstrates how to project a LIDAR pointcloud into the camera plane. The script stores camera frames with the projected LIDAR points in a directory named `_out` in the root directory of the terminal used to run the script.

### Command line arguments

| Argument | Short form | Default | Description |
|----------|------------|---------|-------------|
| --verbose | -v |  | Print debug info |
| --host | -h | 127.0.0.1 | Host IP address |
| --port | -p | 2000 | TCP port for CARLA client |
| --res |  | 1280x720 | Pixel resolution of the display window |
| --frames |  | 500 | Number of frames to record |
| --dot-extent |  | 2 | LIDAR point extent in pixels |
| --no-noise |  | 未激活 | Don't add noise and dropoff |
| --upper-fov |  | 15.0 | LIDAR's upper field of view in degrees |
| --lower-fov |  | -25.0 | LIDAR's lower field of view in degrees |
| --channels |  | 64.0 | Number of LIDAR channels |
| --range |  | 100.0 | LIDAR's max range in meters |
| --points-per-second |  | 100000 | LIDAR points per second |

---

## 载具画廊

* Script filename: `vehicle_gallery.py`
* Example usage: `python3 vehicle_gallery.py` 

This script gives 360 degree views of all CARLA vehicles in sequence.

