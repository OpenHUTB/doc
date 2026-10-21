# 常见问题

DReyeVR 安装和使用的大多数问题都列在这里。如果这份文档不是最新的，请查看我们的 [GitHub 问题](https://github.com/OpenHUTB/hutb/issues) 页面，如果你遇到新的问题，可以创建一个新问题。

***

## 什么是自车和自车传感器？

我们使用[自车](../tuto_G_retrieve_data.md#set-the-ego-vehicle)的概念来区分 AI 控制的车辆和玩家驾驶的车辆。当你第一次启动 VR 驾驶时，你会在世界中生成一辆车，这就是自车([EgoVehicle](https://github.com/OpenHUTB/hutb/blob/hutb/Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/EgoVehicle.cpp))。


除了“EgoVehicle”之外，我们还使用一种名为 [`EgoSensor`](https://github.com/OpenHUTB/hutb/blob/hutb/Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/EgoSensor.cpp) 的组件（即“DReyeVR-sensor”）；该组件继承自 [Carla 传感器](https://openhutb.github.io/doc/ref_sensors/) ，但具备专为 DReyeVR 设计的特性。EgoSensor 负责追踪多种数据，包括用户输入（键盘/鼠标/方向盘）、VR 头显（HMD）的朝向与位置（6 自由度）、第一人称视角的摄像机画面，以及眼动追踪传感器的数据。EgoSensor 所使用的底层数据结构定义在 [`DReyeVRData.h`](https://github.com/OpenHUTB/hutb/blob/hutb/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/DReyeVRData.h) 文件中，具体位于 [`DReyeVR::AggregateData`](https://github.com/OpenHUTB/hutb/blob/eb9aa2f12df647d74252de3176601ec70587a423/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Sensor/DReyeVRData.h#L149) 结构体内。


**EgoVehicle** 是由玩家控制的车辆，而 **EgoSensor** 是一个包含我们关注并需实时追踪的所有 DReyeVR 核心数据的传感器。

***



## DReyeVR 中支持哪些 Carla 功能？

由于 DReyeVR 的 EgoVehicle 继承自 [`ACarlaWheeledVehicle`](https://github.com/OpenHUTB/hutb/blob/hutb/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Vehicle/CarlaWheeledVehicle.h)，大多数标准的 Carla 车辆功能均可直接使用。我们需要修改记录与回放模块，以确保 `EgoSensor` 的各项功能（如头戴式显示器（Head-Mounted Display, HMD）位置/旋转、眼动追踪数据、用户输入等）都能被准确地记录和回放。


然而，VR 驾驶贯穿始终的一个主要假设是：**场景中同一时刻仅存在一辆“自车”（EgoVehicle）**。这是因为每辆自车都会占用 VR 头显（HMD）系统和眼动追踪器资源，且属于开销极大的参与者（例如涉及实时后视镜渲染）。因此，我们不允许通过 Python API 生成新的自车参与者；若需访问自车，我们已通过 [DReyeVR_utils.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/DReyeVR_utils.py) 提供了一种实现机制，具体如下：

```python
from DReyeVR_utils import find_ego_vehicle
...

world = client.get_world()
...

DReyeVR_vehicle = find_ego_vehicle(world)
```

支持的 Carla 功能汇总。

| 功能 | 是否支持 | 笔记 |
| --- | --- | --- |
| 键盘手动控制 | √ | |
| 方向盘手动控制 | ✓ | |
| 世界的记录/回放 | ✓ | |
| EgoSensor 的记录/回放 | ✓ | 专为 DReyeVR 设计 |
| EgoSensor PythonAPI 流式传输 | ✓ | 专为 DReyeVR 设计 |
| 在运行时切换地图 | ✓ | |
| 改变天气 | ✓ | |
| 生成自车（EgoVehicle） | × | 理应已在地图中生成。具备持久性。 |
| 销毁自车（EgoVehicle） | × | 在地图上应始终保持活跃。具备持久性。 |
| EgoVehicle Carla AI 自动驾驶 | ✓ | |
| ScenarioRunner `--route` | ✓ | 我们迄今为止使用 ScenarioRunner 的方式 |
| ScenarioRunner `--scenario` | × | 尚未实现 |
| ScenarioRunner `--agent` | × | 尚未实现 |


***

## 有哪些 Python API 脚本已在 DReyeVR 上进行了测试？

<!-- (:heavy_check_mark: = YES, :white_check_mark: = sort of, :grey_question: = Unsure, :x: = NO) -->
以下 Python API 脚本已通过测试，应能与 DReyeVR 配合使用：

| 脚本 | 是否支持 | 笔记 |
| --- | --- | --- |
| [DReyeVR_AI.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/DReyeVR_AI.py) | ✓ | 使用 DReyeVR 自动驾驶功能的示例 |
| [DReyeVR_logging.py`](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/DReyeVR_logging.py) | ✓ | 实时记录 VR 驾驶的 EgoSensor 数据 |
| [schematic_mode.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/schematic_mode.py) | ✓ | 类似于 [no_rendering_mode.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/no_rendering_mode.py)，但增加了眼动追踪（EyeTracker）可视化功能。 |
| `scenario_runner.py --route` | ✓ | |
| `scenario_runner.py --scenario` | × | 未实现 |
| `scenario_runner.py --agent` | × | 未实现 |
| [show_recorder_collisions.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/show_recorder_collisions.py) | ✓ | |
| [show_recorder_file_info.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/show_recorder_file_info.py) | ✓ | |
| [start_recording.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/start_recording.py) | ✓ | |
| [start_replaying.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/start_replaying.py) | ✓ | |
| [dynamic_weather.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/dynamic_weather.py) | ✓ | |
| [no_rendering_mode.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/no_rendering_mode.py) | 有点 | 应该改用 [schematic_mode.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/schematic_mode.py)，这是我们针对 [no_rendering_mode.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/no_rendering_mode.py) 封装的 DReyeVR 接口。  |
| [show_recorder_actors_blocked.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/show_recorder_actors_blocked.py) | 有点 | |
| [automatic_control.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/automatic_control.py) | × | 使用 [DReyeVR_AI.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/DReyeVR_AI.py) |
| [client_bounding_boxes.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/client_bounding_boxes.py) | 有点 | |
| [draw_skeleton.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/draw_skeleton.py) | 有点 | |
| [generate_traffic.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/generate_traffic.py) | 有点 | |
| [lidar_to_camera.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/lidar_to_camera.py) | 有点 | |
| [manual_control.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/manual_control.py) | × | 通常无需此操作，手动控制是通过服务器进行的。 |
| [manual_control_carsim.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/manual_control_carsim.py) | × | |
| [manual_control_chrono.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/manual_control_chrono.py) | × | |
| [manual_control_steeringwheel.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/manual_control_steeringwheel.py) | × | |
| [open3d_lidar.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/open3d_lidar.py) | 有点 | |
| [sensor_synchronization.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/sensor_synchronization.py) | 有点 | |
| [synchronous_mode.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/synchronous_mode.py) | 有点 | |
| [tutorial.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/tutorial.py) | × | 生成另一个自车（EgoVehicle） |
| [vehicle_gallery.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/vehicle_gallery.py) | × | |
| [vehicle_physics.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/vehicle_physics.py) | 有点 | |
| [visualize_multiple_sensors.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/visualize_multiple_sensors.py) | 有点 | |


***


## 如何更改自车（ego-vehicle）的网格？

目前，我们为自车（EgoVehicle）使用了 Carla 提供的 `BP_TeslaM3` 网格模型，因为该模型具有高度精细的内部细节，且比例非常适合我们的应用场景。


不过，自车（EgoVehicle）**并不非得是**特斯拉；事实上，它甚至不必是汽车，完全可以是摩托车手、消防车，或是其他继承自 [`ACarlaWheeledVehicle`](https://github.com/OpenHUTB/hutb/blob/hutb/Unreal/CarlaUE4/Plugins/Carla/Source/Carla/Vehicle/CarlaWheeledVehicle.h) 的“参与者”（Actor）。


目前我们还没有关于更换 EgoVehicle 网格的最新文档，但参考我们最初设计 EgoVehicle 并选定网格时的[早期配置可驾驶的 VR 玩家的指南](./VRPlayer.md) ，应该不难理解其中的操作。由于 `AEgoVehicle` 是一个基于 C++ 实现的蓝图类，因此任何 Carla 蓝图都可以通过更改父类（reparent）来适配该类，并继承其所有功能。

不过，您需要修改一些针对我们特定网格模型预先设定的默认参数。例如，驾驶员头部位置、方向盘、仪表盘、后视镜等的位置都是相对于网格模型的，因此您需要相应地进行调整。

!!! 笔记
    与之前的那些教程不同，您无需担心在蓝图中添加 UCameraComponent，因为这已由 `DReyeVR_Pawn` 处理。


***


## 安装 DReyeVR 后，如何修改其文件？


安装 DReyeVR 后（请参阅 [`make install`](https://github.com/HARPLab/DReyeVR/tree/main/Scripts#make-install)），相关文件将作为源代码存在于您的 Carla 目录中，并能与 Carla 及 UE4 良好兼容。


您可以查阅我们的 [对应关系文件](https://github.com/HARPLab/DReyeVR/tree/main/Scripts/Paths) ，了解 DReyeVR 仓库中的文件在 Carla 仓库中的具体存放位置。


例如，若要编辑 [EgoVehicle.cpp](https://github.com/OpenHUTB/hutb/blob/hutb/Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/EgoVehicle.cpp) 文件，应修改位于 [Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/EgoVehicle.cpp](https://github.com/OpenHUTB/hutb/blob/hutb/Unreal/CarlaUE4/Source/CarlaUE4/DReyeVR/EgoVehicle.cpp) 的文件。请忽略任何中间文件或生成的文件，因为它们本质上属于缓存内容，且会被重新生成。

对于包括 DReyeVR [参数](https://github.com/OpenHUTB/hutb/blob/hutb/Unreal/CarlaUE4/Config/DReyeVRConfig.ini) 、PythonAPI 文件、ScenarioRunner 等在内的所有文件，操作流程均相同。

另一种方法是直接修改 DReyeVR 仓库中的文件，然后再次运行 `make install` 以覆盖旧文件。

***



## 遇到罗技硬件问题？

首先，请确认您的罗技赛车硬件是否受我们使用的 [LogitechWheelPlugin](https://github.com/HARPLab/LogitechWheelPlugin) 支持（支持的设备列表请参见 README 文件）。

确认硬件兼容后，我们建议您使用 [Logitech G Hub](https://www.logitechg.com/en-us/innovation/g-hub.html) 并确保操作系统能够检测到您的硬件。

如果您的硬件在 DReyeVR 中出现异常（或完全没有反应），请尝试在 UE4 编辑器中启用 Logitech 详细日志记录模式。具体操作是，将 [配置文件](https://github.com/OpenHUTB/hutb/blob/hutb/Unreal/CarlaUE4/Config/DReyeVRConfig.ini)  `[Hardware]` 部分中的 `LogUpdates` 参数值设置为 `True`。

在启用详细日志记录的情况下，再次运行 `make launch` 以在 UE4 编辑器中启动 Carla。依次打开 `Window -> Developer Tools -> Output Log`，查看该关卡输出的所有日志。运行关卡，并确保打印出了以下字符串之一：
```
# is detected
Found a Logitech device (XYZ) connected on input 0

# not detected
Could not find Logitech device connected on input 0
```

建议您查看日志；现在，无论是否检测到状态变化（如按下按钮、旋转轴或踩下踏板），日志都会在每个节拍（更新周期​​）输出信息。如果系统能检测到这些操作却没有任何响应，请提交 Issue 告知我们 :)

***


## ModuleNotFoundError: No module named 'DReyeVR_utils'

当运行 DReyeVR 专用的 PythonAPI 脚本，且您的 Python 环境无法找到 [DReyeVR_utils.py](https://github.com/OpenHUTB/hutb/blob/hutb/PythonAPI/examples/DReyeVR_utils.py) 时，就会出现这种情况。


我们可以通过将 [PythonAPI/examples](https://github.com/OpenHUTB/hutb/tree/hutb/PythonAPI/examples) 添加到 PYTHONPATH 来解决这个问题，具体如下：

```bash
# 在 Linux/MacOS 上
export CARLA_ROOT=/PATH/TO/carla/
export SCENARIO_RUNNER_ROOT=/PATH/TO/scenario_runner/
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg                                           
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/agents
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/examples # <-- 确保包含示例
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI

# 在 Windows x64 Visual C++ Toolset
set CARLA_ROOT=C:PATH\TO\carla\
set SCENARIO_RUNNER_ROOT=C:PATH\TO\scenario_runner\
set PYTHONPATH=%PYTHONPATH%;%CARLA_ROOT%\PythonAPI\carla\dist\carla-0.9.13-py3.7-win-amd64.egg
set PYTHONPATH=%PYTHONPATH%;%CARLA_ROOT%\PythonAPI\carla\agents
set PYTHONPATH=%PYTHONPATH%;%CARLA_ROOT%\PythonAPI\examples # <-- 确保包含示例
set PYTHONPATH=%PYTHONPATH%;%CARLA_ROOT%\PythonAPI\carla
set PYTHONPATH=%PYTHONPATH%;%CARLA_ROOT%\PythonAPI
```

!!! 注意
    如果您使用 `conda`，将这些路径添加到 PYTHONPATH 的方式可能会有所不同。如果是这种情况，请参阅 [`Install.md#using-conda-for-pythonapi`](https://github.com/HARPLab/DReyeVR/blob/main/Docs/Install.md#optionalusing-conda-for-the-pythonapi) （相关问题：[#16](https://github.com/HARPLab/DReyeVR/issues/16)）。

***

## make: *** No rule to make target 'install'.  Stop.

如果您在 Carla 目录下运行 `make install` 命令，则很可能出现这种情况。

`make install` 命令仅在从 DReyeVR 目录调用时才有效。

相关问题：[#7](https://github.com/HARPLab/DReyeVR/issues/7)。

***


## Assertion failed: px != 0, file shared_ptr.hpp


如果在安装 DReyeVR 后运行 PythonAPI 脚本时未重新执行 `make PythonAPI` 命令，可能会出现这种情况。

将 DReyeVR 安装到 Carla 后，您还需要重新构建 PythonAPI（此过程也会重新构建 LibCarla），以确保 DReyeVR 与 PythonAPI 之间的兼容功能正常运作。

```bash
# 在 Carla 中安装 DReyeVR 之后
cd /PATH/TO/DReyeVR
make install CARLA=/PATH/TO/CARLA SR=/PATH/TO/SR

# 现在回到了 Carla，需要重新构建 PythonAPI 和 CarlaUE4
make PythonAPI && make launch
```

相关问题：[#12](https://github.com/HARPLab/DReyeVR/issues/12)  

***


## error: invalid command 'bdist_wheel'

当您构建 PythonAPI 且输出包含以下内容时，会出现这种情况：

```
error: invalid command 'bdist_wheel'

-[BuildPythonAPI]: Carla lib for python has been successfully installed in "..."!
```

虽然日志 `[BuildPythonAPI]` 显示"successfuly installed"，但这其实是 (carla) 的一个 bug，安装实际上失败了，错误信息如上所述。您应该检查构建日志中是否出现任何错误信息。

（感谢 [@SteadyBits](https://github.com/SteadyBits) 的解答！）您应该确保通过 `pip install wheel` 安装 `wheel` 包。您可以检查 `PYTHONPATH` 来确认 `wheel` 包是否已安装。

然后，重新构建 PythonAPI (`make PythonAPI`) 应该会成功，而不会出现`error: invalid command`的错误信息。


相关问题：[#19](https://github.com/HARPLab/DReyeVR/issues/19#issuecomment-1118695739)

***

